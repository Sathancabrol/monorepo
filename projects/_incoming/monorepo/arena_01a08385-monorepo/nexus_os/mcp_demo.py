"""Serveur MCP de référence — pour brancher NEXUS·OS sur du MCP sans internet.

Conforme à la révision **2026-07-28** : cœur stateless (pas de `initialize`, pas
de `Mcp-Session-Id`), `_meta` auto-descriptif sur chaque requête, `server/discover`,
Server Card servie en `.well-known/mcp.json`.

    .venv/bin/python -m nexus_os.mcp_demo --port 8125

Puis dans l'OS, vue « Serveurs MCP » : nom `demo`, url `http://127.0.0.1:8125/mcp`.
Les trois outils apparaissent dans le runtime sous `mcp__demo__*`.

C'est aussi un gabarit : remplace `_TOOLS` par les tiens.
"""
from __future__ import annotations

import argparse
import time
from typing import Any, Callable

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from nexus_os import mcp
from nexus_os.db import store as db_store

PROTOCOL = mcp.PROTOCOL_VERSION
SERVER_INFO = {"name": "nexus-demo-mcp", "version": "1.0.0"}


# -------------------------------------------------------------------------- #
# Outils exposés
# -------------------------------------------------------------------------- #
def _tool_repo_stats(_args: dict[str, Any]) -> dict[str, Any]:
    st = db_store().stats()
    return {"executions": st["runs"], "terminees": st["runs_ok"],
            "tokens": st["tokens_total"], "messages": st["messages"]}


def _tool_runs(_args: dict[str, Any]) -> dict[str, Any]:
    limit = int(_args.get("limit", 5))
    rows = db_store().list_runs(limit=limit)
    return {"count": len(rows),
            "runs": [{"agent": r["agent_id"], "tâche": r["task"][:120],
                      "statut": r["status"], "tokens": r["tokens"]} for r in rows]}


def _tool_uptime(_args: dict[str, Any]) -> dict[str, Any]:
    return {"heure_serveur": time.strftime("%Y-%m-%d %H:%M:%S"),
            "protocole": PROTOCOL}


_TOOLS: dict[str, dict[str, Any]] = {
    "repo_stats": {
        "description": "Statistiques d'usage de NEXUS·OS (exécutions, tokens, messages).",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": _tool_repo_stats,
    },
    "runs": {
        "description": "Dernières exécutions enregistrées, avec agent et consommation.",
        "inputSchema": {"type": "object",
                        "properties": {"limit": {"type": "integer", "minimum": 1,
                                                  "maximum": 50,
                                                  "description": "nombre d'exécutions"}},
                        "required": []},
        "handler": _tool_runs,
    },
    "uptime": {
        "description": "Heure du serveur et version du protocole MCP parlée.",
        "inputSchema": {"type": "object", "properties": {}},
        "handler": _tool_uptime,
    },
}


# -------------------------------------------------------------------------- #
# Application
# -------------------------------------------------------------------------- #
def create_app(name: str = "NEXUS·OS démo", description: str = "") -> FastAPI:
    app = FastAPI(title=name)

    @app.get(f"/{mcp.CARD_PATH}")
    def card() -> dict[str, Any]:
        """Server Card : découverte sans ouvrir de connexion MCP."""
        return {"name": name,
                "description": description or "Serveur MCP de démonstration NEXUS·OS",
                "version": "1.0.0", "url": "/mcp",
                "capabilities": {"tools": {"listChanged": False}},
                "securitySchemes": {}}

    @app.post("/mcp")
    async def rpc(request: Request):
        body = await request.json()
        rid = body.get("id")
        params = body.get("params") or {}
        meta = params.get("_meta") or {}

        # Cœur stateless : la requête doit se décrire elle-même.
        if meta.get("io.modelcontextprotocol/protocolVersion") != PROTOCOL:
            return _err(rid, -32602,
                        "_meta.io.modelcontextprotocol/protocolVersion requis "
                        f"(attendu {PROTOCOL})")

        method = body.get("method")
        if method == "server/discover":
            return _ok(rid, {"protocolVersion": PROTOCOL, "serverInfo": SERVER_INFO,
                             "capabilities": {"tools": {"listChanged": False}},
                             "instructions": "Trois outils de lecture sur l'état de NEXUS·OS."})
        if method == "tools/list":
            return _ok(rid, {"tools": [
                {"name": n, "description": t["description"], "inputSchema": t["inputSchema"]}
                for n, t in _TOOLS.items()]})
        if method == "tools/call":
            tool = _TOOLS.get(params.get("name", ""))
            if not tool:
                return _err(rid, -32601, f"outil inconnu : {params.get('name')}")
            try:
                payload = tool["handler"](params.get("arguments") or {})
            except Exception as e:
                return _ok(rid, {"content": [{"type": "text",
                                              "text": f"{type(e).__name__}: {e}"}],
                                 "isError": True})
            import json as _json

            return _ok(rid, {"content": [{"type": "text",
                                          "text": _json.dumps(payload, ensure_ascii=False,
                                                              indent=2)}],
                             "structuredContent": payload, "isError": False})
        return _err(rid, -32601, f"méthode inconnue : {method}")

    return app


def _ok(rid: Any, result: Any) -> dict[str, Any]:
    return {"jsonrpc": "2.0", "id": rid, "result": result}


def _err(rid: Any, code: int, message: str) -> JSONResponse:
    return JSONResponse({"jsonrpc": "2.0", "id": rid, "error": {"code": code,
                                                                "message": message}})


def main() -> None:
    import uvicorn

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8125)
    args = ap.parse_args()
    print(f"serveur MCP {PROTOCOL} sur http://{args.host}:{args.port}/mcp "
          f"(carte : http://{args.host}:{args.port}/{mcp.CARD_PATH})")
    uvicorn.run(create_app(), host=args.host, port=args.port, log_level="info")


if __name__ == "__main__":
    main()
