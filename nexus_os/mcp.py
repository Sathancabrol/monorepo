"""Client MCP — Model Context Protocol, révision **2026-07-28** (cœur stateless).

Pourquoi ce module : MCP est devenu la couche d'interopérabilité par défaut des
agents (97 M+ téléchargements SDK/mois, 10 000+ serveurs publics). Un agent
NEXUS·OS qui ne sait pas parler MCP ne peut pas réutiliser cet écosystème.

Ce qui a changé avec la révision 2026-07-28, et que ce client implémente :

===============================  =================================================
Évolution                        Implémentation ici
===============================  =================================================
Cœur **stateless**               Aucun handshake `initialize`, aucun
                                 `Mcp-Session-Id`. Chaque requête se décrit.
`_meta` sur chaque requête       `protocolVersion`, `clientCapabilities`,
                                 `clientInfo` inline dans `params._meta`.
En-têtes de routage              `MCP-Protocol-Version`, `Mcp-Method`,
                                 `Mcp-Name` — routables sans lire le corps.
`server/discover`                `discover()` apprend versions + capacités.
**Server Cards**                 `fetch_card()` lit `.well-known/mcp.json`.
Résultats référencés             Le contenu est tronqué/référencé par
                                 `nexus_os.context` avant d'entrer en contexte.
===============================  =================================================

Aucune dépendance tierce : `urllib` seulement, comme le reste de l'OS.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from nexus_os import config

#: Révision du protocole implémentée (cœur stateless, MCP Apps en extension).
PROTOCOL_VERSION = "2026-07-28"
CLIENT_INFO = {"name": "nexus-os", "version": "1.0"}
CLIENT_CAPABILITIES: dict[str, Any] = {"tools": {"listChanged": False}}

#: Emplacement standard de la Server Card (découverte sans connexion).
CARD_PATH = ".well-known/mcp.json"

REGISTRY_FILE = config.NEXUS_HOME / "mcp.json"
#: Un serveur MCP lent ne doit pas bloquer une exécution : plafond court.
TIMEOUT = min(config.REQUEST_TIMEOUT, 30)


class MCPError(RuntimeError):
    """Erreur de protocole ou de transport MCP."""


# -------------------------------------------------------------------------- #
# Configuration des serveurs
# -------------------------------------------------------------------------- #
@dataclass
class ServerConfig:
    name: str
    url: str
    description: str = ""
    #: Nom de la variable d'environnement / entrée secrets.env portant le jeton.
    auth_env: str = ""
    headers: dict[str, str] = field(default_factory=dict)
    enabled: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "url": self.url, "description": self.description,
                "auth_env": self.auth_env, "headers": self.headers,
                "enabled": self.enabled}

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "ServerConfig":
        return cls(name=str(d.get("name") or "").strip(),
                   url=str(d.get("url") or "").strip(),
                   description=str(d.get("description") or ""),
                   auth_env=str(d.get("auth_env") or ""),
                   headers={str(k): str(v) for k, v in (d.get("headers") or {}).items()},
                   enabled=bool(d.get("enabled", True)))


def _load_registry() -> list[ServerConfig]:
    if not REGISTRY_FILE.exists():
        return []
    try:
        raw = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []
    return [ServerConfig.from_dict(x) for x in raw if isinstance(x, dict) and x.get("url")]


def _save_registry(servers: list[ServerConfig]) -> None:
    REGISTRY_FILE.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_FILE.write_text(
        json.dumps([s.to_dict() for s in servers], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")


def list_servers() -> list[ServerConfig]:
    return _load_registry()


def add_server(name: str, url: str, *, description: str = "", auth_env: str = "",
               headers: dict[str, str] | None = None, enabled: bool = True) -> ServerConfig:
    name = (name or "").strip()
    url = (url or "").strip()
    if not name:
        raise ValueError("nom de serveur requis")
    if not url.startswith(("http://", "https://")):
        raise ValueError("url invalide : http(s):// attendu")
    servers = [s for s in _load_registry() if s.name != name]
    srv = ServerConfig(name, url, description, auth_env, dict(headers or {}), enabled)
    servers.append(srv)
    _save_registry(servers)
    return srv


def remove_server(name: str) -> bool:
    before = _load_registry()
    kept = [s for s in before if s.name != name]
    if len(kept) == len(before):
        return False
    _save_registry(kept)
    return True


def get_server(name: str) -> ServerConfig | None:
    return next((s for s in _load_registry() if s.name == name), None)


# -------------------------------------------------------------------------- #
# Transport : une requête = un message JSON-RPC auto-descriptif
# -------------------------------------------------------------------------- #
def _headers_for(cfg: ServerConfig, method: str, tool: str = "") -> dict[str, str]:
    h = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        # En-têtes de routage : un proxy peut router sans inspecter le corps.
        "MCP-Protocol-Version": PROTOCOL_VERSION,
        "Mcp-Method": method,
    }
    if tool:
        h["Mcp-Name"] = tool
    h.update(cfg.headers)
    if cfg.auth_env:
        token = config.secret(cfg.auth_env)
        if token:
            h["Authorization"] = f"Bearer {token}"
    return h


def _meta() -> dict[str, Any]:
    """Bloc `_meta` : remplace l'ancien handshake `initialize`."""
    return {
        "io.modelcontextprotocol/protocolVersion": PROTOCOL_VERSION,
        "io.modelcontextprotocol/clientCapabilities": CLIENT_CAPABILITIES,
        "io.modelcontextprotocol/clientInfo": CLIENT_INFO,
    }


def rpc(cfg: ServerConfig, method: str, params: dict[str, Any] | None = None,
        *, tool: str = "") -> Any:
    """Appel JSON-RPC unique, sans session. Renvoie `result` ou lève MCPError."""
    if not config.ALLOW_NETWORK:
        raise MCPError("réseau désactivé (NEXUS_ALLOW_NETWORK=0)")
    body = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": method,
        "params": {**(params or {}), "_meta": _meta()},
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(cfg.url, data=data,
                                 headers=_headers_for(cfg, method, tool), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        raise MCPError(f"{cfg.name} : HTTP {e.code} {e.reason}") from e
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        raise MCPError(f"{cfg.name} : injoignable ({getattr(e, 'reason', e)})") from e

    try:
        msg = json.loads(raw)
    except json.JSONDecodeError as e:
        raise MCPError(f"{cfg.name} : réponse non-JSON ({raw[:120]!r})") from e
    if isinstance(msg, dict) and msg.get("error"):
        err = msg["error"]
        raise MCPError(f"{cfg.name} : {err.get('code')} {err.get('message')}")
    return msg.get("result") if isinstance(msg, dict) else msg


# -------------------------------------------------------------------------- #
# Découverte
# -------------------------------------------------------------------------- #
def card_url(url: str) -> str:
    """`.well-known/mcp.json` relatif à l'origine du serveur."""
    scheme, _, rest = url.partition("://")
    host = rest.split("/", 1)[0]
    return f"{scheme}://{host}/{CARD_PATH}"


def fetch_card(cfg: ServerConfig) -> dict[str, Any]:
    """Server Card : capacités annoncées sans ouvrir de connexion MCP."""
    if not config.ALLOW_NETWORK:
        raise MCPError("réseau désactivé (NEXUS_ALLOW_NETWORK=0)")
    req = urllib.request.Request(card_url(cfg.url),
                                 headers={"Accept": "application/json", **cfg.headers})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8", errors="replace"))
    except urllib.error.HTTPError as e:
        raise MCPError(f"{cfg.name} : pas de Server Card (HTTP {e.code})") from e
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as e:
        raise MCPError(f"{cfg.name} : Server Card illisible ({e})") from e


def discover(cfg: ServerConfig) -> dict[str, Any]:
    """`server/discover` : versions et capacités, à la place du handshake."""
    out = rpc(cfg, "server/discover")
    if not isinstance(out, dict):
        raise MCPError(f"{cfg.name} : server/discover invalide")
    return {
        "protocol_version": out.get("protocolVersion", ""),
        "server_info": out.get("serverInfo", {}),
        "capabilities": out.get("capabilities", {}),
        "instructions": out.get("instructions", ""),
    }


def list_tools(cfg: ServerConfig) -> list[dict[str, Any]]:
    out = rpc(cfg, "tools/list") or {}
    tools = out.get("tools", []) if isinstance(out, dict) else []
    return [t for t in tools if isinstance(t, dict) and t.get("name")]


def _try_json(text: str) -> Any:
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return text


def call_tool(cfg: ServerConfig, name: str, arguments: dict[str, Any] | None = None) -> str:
    """`tools/call` : renvoie le contenu texte concaténé (content[] + structuredContent)."""
    out = rpc(cfg, "tools/call", {"name": name, "arguments": arguments or {}}, tool=name)
    if not isinstance(out, dict):
        return str(out or "")
    parts: list[str] = []
    for block in out.get("content", []) or []:
        if not isinstance(block, dict):
            continue
        kind = block.get("type", "text")
        if kind == "text":
            parts.append(str(block.get("text", "")))
        elif kind in {"image", "audio"}:
            parts.append(f"[{kind} {block.get('mimeType', '')} "
                         f"{len(str(block.get('data', '')))} octets base64]")
        elif kind == "resource_link":
            parts.append(f"[ressource {block.get('uri', '')}]")
        else:
            parts.append(f"[{kind}] {json.dumps(block, ensure_ascii=False)[:400]}")
    structured = out.get("structuredContent")
    if structured is not None:
        blob = json.dumps(structured, ensure_ascii=False, indent=2)
        # Ne pas doubler : si le serveur a déjà mis le même contenu en texte,
        # le répéter coûte du contexte pour rien.
        joined = "\n".join(parts)
        if blob.strip() not in joined and not any(
                json.dumps(structured, ensure_ascii=False, sort_keys=True)
                in json.dumps(_try_json(p), ensure_ascii=False, sort_keys=True)
                for p in parts if p):
            parts.append("```json\n" + blob + "\n```")
    text = "\n".join(p for p in parts if p).strip()
    if out.get("isError"):
        raise MCPError(f"{cfg.name}/{name} : {text or 'erreur sans message'}")
    return text or "(réponse vide)"


# -------------------------------------------------------------------------- #
# Intégration au registre d'outils de NEXUS·OS
# -------------------------------------------------------------------------- #
def tool_name(server: str, tool: str) -> str:
    """`mcp__<serveur>__<outil>` — namespacing recommandé pour éviter l'écrasement."""
    safe = lambda s: "".join(c if c.isalnum() or c == "-" else "_" for c in s).strip("_")
    return f"mcp__{safe(server)}__{safe(tool)}"


def split_tool_name(name: str) -> tuple[str, str] | None:
    parts = name.split("__")
    return (parts[1], parts[2]) if len(parts) == 3 and parts[0] == "mcp" else None


def probe(cfg: ServerConfig) -> dict[str, Any]:
    """État complet d'un serveur : carte, découverte, outils. Ne lève pas."""
    info: dict[str, Any] = {"name": cfg.name, "url": cfg.url, "enabled": cfg.enabled,
                            "card": None, "discover": None, "tools": [], "error": ""}
    try:
        try:
            card = fetch_card(cfg)
            info["card"] = {"name": card.get("name"), "description": card.get("description"),
                            "version": card.get("version"),
                            "capabilities": card.get("capabilities", {})}
        except MCPError as e:
            info["card"] = {"error": str(e)}
        info["discover"] = discover(cfg)
        info["tools"] = [{"name": t["name"],
                          "description": (t.get("description") or "")[:200]}
                         for t in list_tools(cfg)]
    except MCPError as e:
        info["error"] = str(e)
    info["status"] = "ok" if not info["error"] else "erreur"
    return info


#: Cache des outils distants : relire le registre à chaque exécution coûterait
#: un appel réseau par run. Invalidation par empreinte du fichier + TTL.
_TOOLS_CACHE: dict[str, Any] = {"key": None, "at": 0.0, "tools": []}
_TOOLS_TTL = 60.0


def _registry_key() -> tuple[Any, ...]:
    try:
        stamp = REGISTRY_FILE.stat().st_mtime if REGISTRY_FILE.exists() else 0
    except OSError:
        stamp = 0
    return (str(REGISTRY_FILE), stamp)


def registry_tools(force: bool = False) -> list[Any]:
    """Outils MCP exposés au runtime, sous forme d'objets `Tool` différés.

    L'appel réseau n'a lieu qu'à l'exécution : déclarer un serveur injoignable
    ne casse pas le démarrage de l'OS.
    """
    import time as _time

    key = _registry_key()
    if (not force and _TOOLS_CACHE["key"] == key
            and _time.time() - _TOOLS_CACHE["at"] < _TOOLS_TTL):
        return _TOOLS_CACHE["tools"]

    from nexus_os.tools import Tool, ToolError, _params

    out = []
    for cfg in _load_registry():
        if not cfg.enabled:
            continue
        try:
            remote = list_tools(cfg)
        except MCPError:
            continue          # serveur hors ligne : on l'ignore silencieusement
        for t in remote:
            schema = t.get("inputSchema") or {"type": "object", "properties": {}}
            props = schema.get("properties", {}) if isinstance(schema, dict) else {}

            def handler(ctx, _cfg=cfg, _tool=t["name"], _props=props, **kwargs):
                from nexus_os.context import reference

                try:
                    text = call_tool(_cfg, _tool, {k: v for k, v in kwargs.items()
                                                   if v not in (None, "")})
                except MCPError as e:
                    raise ToolError(str(e)) from e
                # Résultat référencé : un gros payload ne sature pas le contexte.
                return reference(ctx, text, kind=f"mcp:{_cfg.name}/{_tool}")

            out.append(Tool(
                name=tool_name(cfg.name, t["name"]),
                description=f"[MCP {cfg.name}] {(t.get('description') or t['name'])[:300]}",
                parameters=_params(props, schema.get("required", [])),
                handler=handler,
                risky=False,
                tags=["mcp", cfg.name],
            ))
    _TOOLS_CACHE.update(key=key, at=_time.time(), tools=out)
    return out


def summarize() -> dict[str, Any]:
    servers = _load_registry()
    return {
        "protocol_version": PROTOCOL_VERSION,
        "card_path": CARD_PATH,
        "stateless": True,
        "registry_file": str(REGISTRY_FILE),
        "servers": [s.to_dict() for s in servers],
        "count": len(servers),
        "enabled": sum(1 for s in servers if s.enabled),
    }
