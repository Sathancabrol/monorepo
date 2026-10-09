"""Serveur HTTP minimal, bibliothèque standard uniquement.

Pourquoi ne pas utiliser FastAPI/Flask : l'application doit s'installer sur un
poste Windows sans rien télécharger d'autre que Python, et démarrer en une
seconde. Le routage tient en ~180 lignes et couvre ce dont on a besoin :
routes typées, paramètres nommés, fichiers statiques, JSON, SSE.
"""

from __future__ import annotations

import json
import mimetypes
import re
import threading
import time
import urllib.parse
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("image/svg+xml", ".svg")
mimetypes.add_type("application/json", ".json")
mimetypes.add_type("application/wasm", ".wasm")

_PARAM = re.compile(r":([A-Za-z_][A-Za-z0-9_]*)")


def _compile(pattern: str) -> re.Pattern:
    rx = _PARAM.sub(lambda m: f"(?P<{m.group(1)}>[^/]+)", pattern)
    # '*' est capturant : sans cela le fourre-tout avalerait tout sans rien transmettre.
    # On ne remplace qu'une fois — sinon le '*' du groupe serait mangé à son tour.
    if "*" in rx:
        tete, _, queue = rx.partition("*")
        rx = tete + "(?P<rest>.*)" + queue.replace("*", ".*")
    return re.compile("^" + rx.rstrip("/") + "/?$")


class Request:
    def __init__(self, method, path, query, headers, body: bytes, client=None):
        self.method = method
        self.path = path
        self.query = query
        self.headers = headers
        self.body = body
        self.client = client

    def q(self, name, default=None):
        v = self.query.get(name, [default])
        return v[0] if isinstance(v, list) else v

    def json(self, default=None):
        if not self.body:
            return default if default is not None else {}
        try:
            return json.loads(self.body.decode("utf-8"))
        except Exception:
            return default if default is not None else {}

    @property
    def text(self) -> str:
        return self.body.decode("utf-8", errors="replace")


class Response:
    def __init__(self, status=200, body=b"", content_type="text/plain; charset=utf-8",
                 headers=None):
        self.status = status
        self.body = body if isinstance(body, (bytes, bytearray)) else str(body).encode("utf-8")
        self.content_type = content_type
        self.headers = dict(headers or {})

    @classmethod
    def json(cls, data, status=200):
        return cls(status, json.dumps(data, ensure_ascii=False),
                   "application/json; charset=utf-8")

    @classmethod
    def text(cls, s: str, status=200):
        return cls(status, s, "text/plain; charset=utf-8")

    @classmethod
    def html(cls, s: str, status=200):
        return cls(status, s, "text/html; charset=utf-8")

    @classmethod
    def file(cls, path, download_name: str | None = None, inline=True):
        p = Path(path)
        data = p.read_bytes()
        ctype = mimetypes.guess_type(p.name)[0] or "application/octet-stream"
        headers = {}
        if download_name:
            disp = "inline" if inline else "attachment"
            headers["Content-Disposition"] = f"{disp}; filename*=UTF-8''{urllib.parse.quote(download_name)}"
        return cls(200, data, ctype, headers)

    @classmethod
    def redirect(cls, url, permanent=False):
        return cls(301 if permanent else 302, b"", "text/plain", {"Location": url})

    @classmethod
    def error(cls, message: str, status=400):
        return cls.json({"erreur": message, "statut": status}, status)

    @classmethod
    def not_found(cls, message="introuvable"):
        return cls.error(message, 404)


class Router:
    """Routes : '/api/meeting/:id' avec paramètres nommés ; '*' fourre-tout."""

    def __init__(self):
        self._routes: list[tuple[str, re.Pattern, callable, bool]] = []

    def add(self, method: str, pattern: str, handler, stream=False):
        self._routes.append((method.upper(), _compile(pattern), handler, stream))
        return handler

    def get(self, pattern, **kw):
        return lambda fn: (self.add("GET", pattern, fn, kw.get("stream", False)), fn)[1]

    def post(self, pattern, **kw):
        return lambda fn: (self.add("POST", pattern, fn, kw.get("stream", False)), fn)[1]

    def put(self, pattern, **kw):
        return lambda fn: (self.add("PUT", pattern, fn, kw.get("stream", False)), fn)[1]

    def delete(self, pattern, **kw):
        return lambda fn: (self.add("DELETE", pattern, fn, kw.get("stream", False)), fn)[1]

    def resolve(self, method, path):
        for m, rx, handler, stream in self._routes:
            if m != method:
                continue
            mo = rx.match(path)
            if mo:
                return handler, mo.groupdict(), stream
        return None, {}, False

    def static(self, prefix: str, directory: Path | str, index="index.html", spa=False):
        base = Path(directory)

        def handler(req, rest="", **_):
            rel = (rest or "").lstrip("/")
            if not rel:
                rel = index
            target = (base / rel).resolve()
            try:
                target.relative_to(base.resolve())
            except ValueError:
                return Response.not_found("chemin refusé")
            if target.is_dir():
                target = target / index
            if not target.exists():
                if spa:
                    target = base / index
                else:
                    return Response.not_found(rel)
            r = Response.file(target)
            # pas de cache en développement : on recharge toujours le frais
            r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            return r

        self.add("GET", f"{prefix.rstrip('/')}/*", handler)


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "CarreDAs/0.1"
    router: Router = None  # injecté par make_server

    # ---------- bruit de log ----------
    def log_message(self, fmt, *args):
        try:
            import carredas.log as _log
            _log.debug("http", fmt % args)
        except Exception:
            pass

    # ---------- lecture ----------
    def _read_body(self) -> bytes:
        length = int(self.headers.get("Content-Length") or 0)
        if length:
            return self.rfile.read(length)
        if self.headers.get("Transfer-Encoding", "").lower() == "chunked":
            chunks = []
            while True:
                line = self.rfile.readline().strip()
                if not line:
                    break
                size = int(line, 16)
                if size == 0:
                    self.rfile.readline()
                    break
                chunks.append(self.rfile.read(size))
                self.rfile.readline()
            return b"".join(chunks)
        return b""

    def _request(self) -> Request:
        parsed = urllib.parse.urlparse(self.path)
        return Request(
            method=self.command,
            path=urllib.parse.unquote(parsed.path),
            query=urllib.parse.parse_qs(parsed.query),
            headers=self.headers,
            body=self._read_body(),
            client=self.client_address[0],
        )

    # ---------- écriture ----------
    def _send(self, resp: Response, head_only=False):
        body = resp.body if not head_only else b""
        self.send_response(resp.status)
        self.send_header("Content-Type", resp.content_type)
        self.send_header("Content-Length", str(len(body)))
        for k, v in resp.headers.items():
            self.send_header(k, v)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", resp.headers.get("Cache-Control", "no-store"))
        self.end_headers()
        if body:
            self.wfile.write(body)

    def _sse(self, handler, params):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache, no-store")
        self.send_header("Connection", "keep-alive")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

        alive = {"on": True}

        def emit(event: str, data):
            if not alive["on"]:
                return False
            try:
                payload = data if isinstance(data, str) else json.dumps(data, ensure_ascii=False)
                chunk = ""
                for line in payload.splitlines() or [""]:
                    chunk += f"data: {line}\n"
                self.wfile.write(f"event: {event}\n{chunk}\n".encode("utf-8"))
                self.wfile.flush()
                return True
            except Exception:
                alive["on"] = False
                return False

        try:
            handler(self._request_without_body(), emit, **params)
        except (BrokenPipeError, ConnectionResetError):
            pass
        except Exception:
            import traceback
            traceback.print_exc()
        finally:
            alive["on"] = False

    def _request_without_body(self) -> Request:
        parsed = urllib.parse.urlparse(self.path)
        return Request(self.command, urllib.parse.unquote(parsed.path),
                       urllib.parse.parse_qs(parsed.query), self.headers, b"",
                       self.client_address[0])

    # ---------- dispatch ----------
    def _dispatch(self, head_only=False):
        req = self._request()
        handler, params, stream = self.router.resolve(req.method, req.path)
        if handler is None:
            self._send(Response.not_found(req.path), head_only)
            return
        if stream:
            self._sse(handler, params)
            return
        try:
            out = handler(req, **params)
        except Exception as exc:  # une erreur ne doit jamais tuer le serveur
            import traceback
            traceback.print_exc()
            out = Response.error(f"{type(exc).__name__}: {exc}", 500)
        if isinstance(out, Response):
            self._send(out, head_only)
        elif isinstance(out, (dict, list)):
            self._send(Response.json(out), head_only)
        elif isinstance(out, tuple) and len(out) == 2:
            self._send(Response.json(out[0], out[1]), head_only)
        elif out is None:
            self._send(Response.json({"ok": True}), head_only)
        else:
            self._send(Response.text(str(out)), head_only)

    def do_GET(self):
        self._dispatch()

    def do_HEAD(self):
        self._dispatch(head_only=True)

    def do_POST(self):
        self._dispatch()

    def do_PUT(self):
        self._dispatch()

    def do_PATCH(self):
        self._dispatch()

    def do_DELETE(self):
        self._dispatch()

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Allow", "GET, HEAD, POST, PUT, PATCH, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS")
        self.send_header("Content-Length", "0")
        self.end_headers()


def make_server(router: Router, host="127.0.0.1", port=0):
    """Crée le serveur (port 0 = port libre choisi par l'OS)."""
    cls = type("BoundHandler", (Handler,), {"router": router})
    ThreadingHTTPServer.allow_reuse_address = True
    ThreadingHTTPServer.daemon_threads = True
    srv = ThreadingHTTPServer((host, port), cls)
    return srv


def serve(router: Router, host="127.0.0.1", port=0, ready=None, block=True):
    srv = make_server(router, host, port)
    real = srv.server_address[1]
    if ready:
        ready(real)
    t = threading.Thread(target=srv.serve_forever, daemon=True)
    t.start()
    if block:
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            srv.shutdown()
    return srv, real
