#!/usr/bin/env python3
"""Chronos local model router: small, dependency-free OpenAI-compatible failover.

Runs on the main Windows desktop; listens on 127.0.0.1 by default.
No cloud API or paid route is used. Phone models are restricted to light tasks.
"""
import argparse
import copy
import http.client
import json
import logging
import os
import socket
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen

LOG = logging.getLogger("cronos-fleet")
MAX_BODY = 2_000_000
ALLOWED_ROUTES = {"cronos-local", "cronos-light"}
TRANSIENT = {408, 409, 425, 429, 500, 502, 503, 504}


def load_nodes(path):
    with open(path, encoding="utf-8") as f:
        cfg = json.load(f)
    if cfg.get("version") != 1 or not isinstance(cfg.get("nodes"), list):
        raise ValueError("fleet.json needs version=1 and nodes=[...]")
    names = set()
    for n in cfg["nodes"]:
        if not isinstance(n, dict) or not isinstance(n.get("name"), str):
            raise ValueError("Each node must have a name")
        if n["name"] in names:
            raise ValueError("Duplicate node name")
        names.add(n["name"])
        if not n.get("enabled", False):
            continue
        url = str(n.get("url", ""))
        parsed = urlsplit(url)
        if parsed.scheme != "http" or not parsed.hostname or not parsed.path.endswith("/v1"):
            raise ValueError(f"{n['name']}: url must be http://HOST:PORT/v1 (private LAN / VPN only)")
        if not n.get("model") or n.get("tier") not in ("agent", "light"):
            raise ValueError(f"{n['name']}: model and tier=agent|light required")
        if parsed.hostname not in ("127.0.0.1", "localhost", "::1") and not n.get("private_network_confirmed", False):
            raise ValueError(f"{n['name']}: confirm private LAN/VPN first")
    return cfg


def eligible_nodes(cfg, route, needs_tools):
    nodes = [n for n in cfg["nodes"] if n.get("enabled", False)]
    if route == "cronos-local":
        nodes = [n for n in nodes if n["tier"] == "agent"]
    elif route == "cronos-light":
        nodes = sorted(nodes, key=lambda n: (n["tier"] != "light", int(n.get("priority", 100))))
    if needs_tools:
        nodes = [n for n in nodes if n.get("supports_tools", False)]
    if route == "cronos-local":
        nodes = sorted(nodes, key=lambda n: int(n.get("priority", 100)))
    return nodes


def node_headers(node):
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    env = node.get("api_key_env")
    if env:
        secret = os.environ.get(env)
        if not secret:
            raise ValueError(f"Missing environment variable {env} for {node['name']}")
        headers["Authorization"] = "Bearer " + secret
    return headers


def probe(node, timeout=2.0):
    try:
        req = Request(node["url"].rstrip("/") + "/models", headers=node_headers(node))
        with urlopen(req, timeout=timeout) as resp:
            return 200 <= resp.status < 300
    except (OSError, ValueError, HTTPError, URLError):
        return False


class RouterHandler(BaseHTTPRequestHandler):
    server_version = "CronosFleet/0.1"
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        LOG.info("%s " + fmt, self.client_address[0], *args)

    def json_reply(self, code, obj):
        data = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/v1/models":
            return self.json_reply(200, {"object": "list", "data": [
                {"id": x, "object": "model", "owned_by": "cronos-fleet"} for x in sorted(ALLOWED_ROUTES)]})
        if self.path == "/health":
            return self.json_reply(200, {"service": "cronos-fleet", "nodes": [
                {"name": n["name"], "enabled": bool(n.get("enabled")),
                 "tier": n.get("tier"), "ready": probe(n) if n.get("enabled") else False}
                for n in self.server.nodes["nodes"]]})
        return self.json_reply(404, {"error": {"message": "Not found"}})

    def do_POST(self):
        if self.path != "/v1/chat/completions":
            return self.json_reply(404, {"error": {"message": "Only chat completions are supported"}})
        try:
            n = int(self.headers.get("Content-Length", "0"))
            if n <= 0 or n > MAX_BODY:
                return self.json_reply(413, {"error": {"message": "Invalid request size"}})
            payload = json.loads(self.rfile.read(n))
            if not isinstance(payload, dict) or not isinstance(payload.get("messages"), list):
                return self.json_reply(400, {"error": {"message": "messages must be an array"}})
            route = payload.get("model", "cronos-local")
            if route not in ALLOWED_ROUTES:
                return self.json_reply(400, {"error": {"message": "Unknown route"}})
            needs_tools = bool(payload.get("tools"))
            candidates = eligible_nodes(self.server.nodes, route, needs_tools)
            if not candidates:
                return self.json_reply(503, {"error": {"message": "No eligible local node; no cloud fallback performed"}})
        except (ValueError, TypeError, json.JSONDecodeError):
            return self.json_reply(400, {"error": {"message": "Invalid JSON"}})
        failures = []
        for node in candidates:
            req_body = copy.deepcopy(payload)
            req_body["model"] = node["model"]
            endpoint = node["url"].rstrip("/") + "/chat/completions"
            try:
                req = Request(endpoint, data=json.dumps(req_body).encode(), headers=node_headers(node), method="POST")
                with urlopen(req, timeout=float(node.get("timeout", 90))) as r:
                    if payload.get("stream", False):
                        self.send_response(200)
                        self.send_header("Content-Type", "text/event-stream")
                        self.send_header("Cache-Control", "no-cache")
                        self.send_header("Connection", "close")
                        self.send_header("X-Cronos-Node", node["name"])
                        self.end_headers()
                        self.close_connection = True
                        try:
                            while True:
                                block = r.readline()  # SSE: do not wait for 4096 bytes
                                if not block:
                                    break
                                self.wfile.write(block)
                                self.wfile.flush()
                        except (BrokenPipeError, ConnectionResetError, TimeoutError, OSError) as e:
                            LOG.warning("stream interrupted on %s: %s (cannot safely switch mid-stream)", node["name"], type(e).__name__)
                        return
                    data = r.read(MAX_BODY + 1)
                    if len(data) > MAX_BODY:
                        failures.append(f"{node['name']}: oversized response")
                        continue
                    try:
                        obj = json.loads(data)
                    except ValueError:
                        failures.append(f"{node['name']}: invalid JSON")
                        continue
                    if not obj.get("choices"):
                        failures.append(f"{node['name']}: no choices")
                        continue
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.send_header("Content-Length", str(len(data)))
                    self.send_header("X-Cronos-Node", node["name"])
                    self.end_headers()
                    self.wfile.write(data)
                    LOG.info("request served by %s", node["name"])
                    return
            except HTTPError as e:
                LOG.warning("%s upstream status %s", node["name"], e.code)
                failures.append(f"{node['name']}: HTTP {e.code}")
                if e.code not in TRANSIENT and e.code not in (401, 403, 404):
                    return self.json_reply(502, {"error": {"message": "Upstream rejected request", "node": node["name"], "code": e.code}})
            except (OSError, URLError, TimeoutError, ValueError) as e:
                LOG.warning("%s unavailable: %s", node["name"], type(e).__name__)
                failures.append(f"{node['name']}: {type(e).__name__}")
        self.json_reply(503, {"error": {"message": "All eligible local nodes failed", "attempts": failures}})


def main(argv=None):
    ap = argparse.ArgumentParser(description="Zero-cost local node router for Hermes")
    ap.add_argument("--config", default=os.path.join(os.path.dirname(__file__), "fleet.json"))
    ap.add_argument("--host", default="127.0.0.1", help="Keep loopback unless a secure deployment is planned")
    ap.add_argument("--port", default=18888, type=int)
    args = ap.parse_args(argv)
    if args.host not in ("127.0.0.1", "::1", "localhost"):
        ap.error("Only loopback host allowed: use a protected reverse proxy for external access")
    cfg = load_nodes(args.config)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    srv = ThreadingHTTPServer((args.host, args.port), RouterHandler)
    srv.nodes = cfg
    LOG.info("Cronos router on http://%s:%s/v1 | %d enabled nodes", args.host, args.port, sum(bool(n.get("enabled")) for n in cfg["nodes"]))
    try:
        srv.serve_forever(poll_interval=0.3)
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()


if __name__ == "__main__":
    main()