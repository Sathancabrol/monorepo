"""Registre d'outils des agents — exécution réelle, sandbox stricte.

Règles de sécurité appliquées à tous les outils :

* écriture **uniquement** sous `.nexus/workspace/` (sandbox de l'OS) ;
* lecture autorisée dans le dépôt, sauf secrets (`.env`, `secrets.env`, clés) ;
* shell/python désactivés par défaut (`NEXUS_ALLOW_SHELL=1` pour activer),
  toujours avec timeout et cwd = sandbox ;
* réseau sortant contrôlé par `NEXUS_ALLOW_NETWORK`.
"""
from __future__ import annotations

import html
import json
import re
import subprocess
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from nexus_os import config
from nexus_os.memory import memory

SECRET_PATTERNS = (".env", "secrets.env", "id_rsa", "id_ed25519", ".netrc", "credentials",
                   ".git/config", ".npmrc")
SHELL_DENY = re.compile(
    r"(rm\s+-rf\s+/|mkfs|dd\s+if=|:\(\)\s*\{|shutdown|reboot|git\s+push|curl\s+.*\|\s*sh|"
    r"wget\s+.*\|\s*sh|chmod\s+-R\s+777\s+/)",
    re.I,
)


class ToolError(Exception):
    pass


@dataclass
class ToolContext:
    """Ce que voit un outil pendant une exécution."""

    workspace: Path = config.WORKSPACE_DIR
    read_root: Path = config.READ_ROOT
    agent_id: str = ""
    emit: Callable[[dict[str, Any]], None] | None = None

    def log(self, msg: str) -> None:
        if self.emit:
            self.emit({"type": "log", "message": msg})


@dataclass
class Tool:
    name: str
    description: str
    parameters: dict[str, Any]
    handler: Callable[..., str]
    risky: bool = False
    tags: list[str] = field(default_factory=list)

    def spec(self) -> dict[str, Any]:
        return {"name": self.name, "description": self.description, "parameters": self.parameters}


# --------------------------------------------------------------------------- #
# Helpers de sécurité
# --------------------------------------------------------------------------- #
def _rel_to_root(root: Path, path: str) -> Path:
    p = (root / path.lstrip("/")) if not Path(path).is_absolute() else Path(path)
    resolved = p.resolve()
    root_resolved = root.resolve()
    if resolved != root_resolved and root_resolved not in resolved.parents:
        raise ToolError(f"chemin hors limite autorisée : {path}")
    return resolved


def _safe_read_path(path: str) -> Path:
    target = _rel_to_root(config.READ_ROOT, path)
    low = str(target).lower().replace("\\", "/")
    for pat in SECRET_PATTERNS:
        if pat in low:
            raise ToolError(f"lecture bloquée (secret potentiel) : {path}")
    if not target.exists():
        raise ToolError(f"introuvable : {path}")
    return target


def _safe_write_path(path: str) -> Path:
    target = _rel_to_root(config.WORKSPACE_DIR, path)
    if target.is_dir():
        raise ToolError(f"cible est un dossier : {path}")
    target.parent.mkdir(parents=True, exist_ok=True)
    return target


def _clip(s: str, n: int | None = None) -> str:
    n = n or config.MAX_TOOL_RESULT_CHARS
    s = s if isinstance(s, str) else json.dumps(s, ensure_ascii=False, default=str)
    return s if len(s) <= n else s[:n] + f"\n… [tronqué, {len(s)} caractères au total]"


# --------------------------------------------------------------------------- #
# Outils : système de fichiers
# --------------------------------------------------------------------------- #
def t_list_dir(ctx: ToolContext, path: str = "") -> str:
    target = _rel_to_root(config.READ_ROOT, path or ".")
    if not target.is_dir():
        raise ToolError(f"pas un dossier : {path}")
    rows = []
    for child in sorted(target.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))[:200]:
        if child.name in {".git", "node_modules", "__pycache__", ".venv"}:
            continue
        rows.append(
            f"{'d' if child.is_dir() else 'f'} {child.relative_to(config.READ_ROOT)}"
            + ("" if child.is_dir() else f"  ({child.stat().st_size} o)")
        )
    return "\n".join(rows) or "(dossier vide)"


def t_read_file(ctx: ToolContext, path: str = "", max_chars: int = 0) -> str:
    target = _safe_read_path(path)
    if target.is_dir():
        raise ToolError(f"c'est un dossier, utilise list_dir : {path}")
    limit = max_chars or config.MAX_READ_BYTES
    raw = target.read_bytes()[:limit]
    text = raw.decode("utf-8", errors="replace")
    return _clip(f"# {path}\n{text}")


def t_write_file(ctx: ToolContext, path: str = "", content: str = "") -> str:
    if not path:
        raise ToolError("paramètre `path` requis")
    data = (content or "").encode("utf-8")
    if len(data) > config.MAX_WRITE_BYTES:
        raise ToolError("contenu trop volumineux")
    target = _safe_write_path(path)
    target.write_bytes(data)
    ctx.log(f"écrit {target.relative_to(config.WORKSPACE_DIR)} ({len(data)} o)")
    return f"écrit : workspace/{path} ({len(data)} octets)"


def t_grep(ctx: ToolContext, pattern: str = "", path: str = "", limit: int = 40) -> str:
    if not pattern:
        raise ToolError("paramètre `pattern` requis")
    root = _rel_to_root(config.READ_ROOT, path or ".")
    rx = re.compile(pattern, re.I)
    hits: list[str] = []
    skip = {".git", "node_modules", "__pycache__", ".venv", "dist", ".nexus"}
    files = [root] if root.is_file() else [
        p for p in root.rglob("*")
        if p.is_file() and not (skip & set(p.relative_to(config.READ_ROOT).parts))
        and p.stat().st_size < 2_000_000
    ]
    for f in files:
        try:
            for i, line in enumerate(f.read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                if rx.search(line):
                    hits.append(f"{f.relative_to(config.READ_ROOT)}:{i}: {line.strip()[:180]}")
                    if len(hits) >= limit:
                        return _clip("\n".join(hits) + f"\n… (limite {limit} atteinte)")
        except OSError:
            continue
    return _clip("\n".join(hits)) if hits else f"aucune correspondance pour /{pattern}/"


# --------------------------------------------------------------------------- #
# Outils : exécution (opt-in)
# --------------------------------------------------------------------------- #
def t_shell(ctx: ToolContext, command: str = "", timeout: int = 0) -> str:
    if not config.ALLOW_SHELL:
        raise ToolError("shell désactivé — démarre le serveur avec NEXUS_ALLOW_SHELL=1")
    if not command.strip():
        raise ToolError("commande vide")
    if SHELL_DENY.search(command):
        raise ToolError("commande refusée par la liste de sécurité")
    try:
        res = subprocess.run(
            command, shell=True, cwd=str(config.WORKSPACE_DIR), capture_output=True, text=True,
            timeout=timeout or config.SHELL_TIMEOUT,
        )
    except subprocess.TimeoutExpired:
        raise ToolError(f"timeout après {timeout or config.SHELL_TIMEOUT}s")
    out = (res.stdout or "") + (("\n[stderr]\n" + res.stderr) if res.stderr else "")
    return _clip(f"exit={res.returncode}\n{out.strip()}")


def t_python_exec(ctx: ToolContext, code: str = "", timeout: int = 0) -> str:
    if not config.ALLOW_SHELL:
        raise ToolError("exécution python désactivée — NEXUS_ALLOW_SHELL=1")
    script = config.WORKSPACE_DIR / "_nexus_exec.py"
    script.write_text(code or "", encoding="utf-8")
    return t_shell(ctx, "python3 _nexus_exec.py", timeout=timeout or 60)


# --------------------------------------------------------------------------- #
# Outils : réseau
# --------------------------------------------------------------------------- #
def t_http_get(ctx: ToolContext, url: str = "", timeout: int = 0) -> str:
    if not config.ALLOW_NETWORK:
        raise ToolError("réseau désactivé (NEXUS_ALLOW_NETWORK=0)")
    if not re.match(r"^https?://", url or ""):
        raise ToolError("URL invalide (http/https uniquement)")
    req = urllib.request.Request(url, headers={"User-Agent": "NexusOS/1.0"})
    with urllib.request.urlopen(req, timeout=timeout or 20) as resp:  # nosec - URL fournie par l'agent
        body = resp.read(200_000).decode("utf-8", errors="replace")
        return _clip(f"HTTP {resp.status} {url}\n{body}")


def t_web_search(ctx: ToolContext, query: str = "", limit: int = 6) -> str:
    if not config.ALLOW_NETWORK:
        raise ToolError("réseau désactivé (NEXUS_ALLOW_NETWORK=0)")
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote_plus(query or "")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 NexusOS/1.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:  # nosec
        page = resp.read(400_000).decode("utf-8", errors="replace")
    results = re.findall(
        r'<a[^>]+class="result__a"[^>]+href="([^"]+)"[^>]*>(.*?)</a>', page, re.S
    )[:limit]
    if not results:
        return f"aucun résultat parseable pour « {query} »"
    out = []
    for i, (href, title) in enumerate(results, 1):
        clean = html.unescape(re.sub(r"<[^>]+>", "", title)).strip()
        out.append(f"{i}. {clean}\n   {html.unescape(href)[:200]}")
    return _clip("\n".join(out))


# --------------------------------------------------------------------------- #
# Outils : mémoire
# --------------------------------------------------------------------------- #
def t_memory_remember(ctx: ToolContext, content: str = "", kind: str = "fact",
                      tags: str = "") -> str:
    if not content.strip():
        raise ToolError("contenu vide")
    item = memory().remember(content, kind=kind, agent=ctx.agent_id,
                            tags=[t.strip() for t in tags.split(",") if t.strip()])
    return f"mémorisé ({item['kind']}) id={item['id']}"


def t_memory_recall(ctx: ToolContext, query: str = "", kind: str = "", limit: int = 5) -> str:
    items = memory().recall(query, kind=kind or None, limit=limit)
    if not items:
        return "mémoire vide pour cette requête"
    return "\n".join(f"- [{i['kind']}] {i['content']}" for i in items)


# --------------------------------------------------------------------------- #
# Outils : production (diagrammes façon diagram-design, HTML façon hyperframes)
# --------------------------------------------------------------------------- #
def t_diagram(ctx: ToolContext, title: str = "", mermaid: str = "",
              nodes: str = "", edges: str = "", kind: str = "flowchart") -> str:
    """Écrit un diagramme Mermaid + une page HTML auto-portante de prévisualisation."""
    title = (title or "diagramme").strip()
    body = (mermaid or "").strip()
    if not body:
        ns = [n.strip() for n in (nodes or "").split(",") if n.strip()]
        es = [e.strip() for e in (edges or "").split(";") if e.strip()]
        if not ns:
            raise ToolError("fournis `mermaid`, ou `nodes` (+ `edges`)")
        lines = [f"{kind} TD"]
        lines += [f'  {re.sub(r"[^A-Za-z0-9_]", "_", n)}["{n}"]' for n in ns]
        for e in es:
            if "-->" in e:
                a, _, b = e.partition("-->")
                lines.append(f"  {a.strip()} --> {b.strip()}")
        body = "\n".join(lines)
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-") or "diagramme"
    md = _safe_write_path(f"diagrams/{slug}.mmd")
    md.write_text(body, encoding="utf-8")
    page = _safe_write_path(f"diagrams/{slug}.html")
    page.write_text(
        "<!doctype html><html lang='fr'><head><meta charset='utf-8'>"
        f"<title>{html.escape(title)}</title>"
        "<script src='https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js'></script>"
        "<style>body{margin:0;padding:24px;background:#0b0f17;color:#e6edf3;"
        "font:14px/1.5 system-ui,sans-serif}h1{font-size:18px;font-weight:600}"
        "pre{background:#111726;padding:16px;border-radius:10px;overflow:auto}</style>"
        f"</head><body><h1>{html.escape(title)}</h1>"
        f"<pre class='mermaid'>{html.escape(body)}</pre>"
        "<script>mermaid.initialize({theme:'dark'})</script></body></html>",
        encoding="utf-8",
    )
    return (f"diagramme créé : workspace/diagrams/{slug}.mmd + {slug}.html "
            f"(aperçu : /os/workspace/diagrams/{slug}.html)")


def t_compose_html(ctx: ToolContext, title: str = "", html_body: str = "",
                   css: str = "") -> str:
    """Compose une page HTML autonome (même esprit que hyperframes : HTML d'abord)."""
    if not html_body.strip():
        raise ToolError("`html_body` requis")
    slug = re.sub(r"[^a-z0-9]+", "-", (title or "composition").lower()).strip("-") or "composition"
    path = _safe_write_path(f"compositions/{slug}.html")
    path.write_text(
        f"<!doctype html><html lang='fr'><head><meta charset='utf-8'>"
        f"<title>{html.escape(title or slug)}</title>"
        f"<style>{css or 'body{font:15px/1.6 system-ui,sans-serif;margin:40px auto;max-width:820px}'}"
        "</style></head><body>" + html_body + "</body></html>",
        encoding="utf-8",
    )
    return f"composition créée : workspace/compositions/{slug}.html"


# --------------------------------------------------------------------------- #
# Outils : méta (routage inter-agents, création d'agent)
# --------------------------------------------------------------------------- #
def t_handoff(ctx: ToolContext, agent_id: str = "", task: str = "") -> str:
    """Marqueur : le runtime intercepte cet outil pour déléguer à un autre agent."""
    if not agent_id or not task:
        raise ToolError("`agent_id` et `task` requis")
    return f"handoff→{agent_id}: {task[:200]}"


def t_create_agent(ctx: ToolContext, description: str = "", name: str = "") -> str:
    """Marqueur : le runtime intercepte pour appeler le créateur d'agents."""
    if not description:
        raise ToolError("`description` requise")
    return f"create_agent: {description[:200]}"


# --------------------------------------------------------------------------- #
# Registre
# --------------------------------------------------------------------------- #
_OBJ = {"type": "object", "properties": {}, "required": []}


def _params(props: dict[str, Any], required: list[str] | None = None) -> dict[str, Any]:
    return {"type": "object", "properties": props, "required": required or []}


_STR = {"type": "string"}
_INT = {"type": "integer"}

BUILTIN_TOOLS: list[Tool] = [
    Tool("list_dir", "Liste le contenu d'un dossier du dépôt (lecture seule).",
         _params({"path": {**_STR, "description": "chemin relatif à la racine du dépôt"}}),
         t_list_dir, tags=["fs"]),
    Tool("read_file", "Lit un fichier texte du dépôt (jamais les secrets).",
         _params({"path": {**_STR, "description": "chemin relatif"},
                  "max_chars": _INT}, ["path"]),
         t_read_file, tags=["fs"]),
    Tool("write_file", "Écrit un fichier dans l'espace de travail sandboxé de l'OS.",
         _params({"path": {**_STR, "description": "chemin relatif à workspace/"},
                  "content": _STR}, ["path", "content"]),
         t_write_file, tags=["fs", "write"]),
    Tool("grep", "Recherche une expression régulière dans les fichiers du dépôt.",
         _params({"pattern": _STR, "path": _STR, "limit": _INT}, ["pattern"]),
         t_grep, tags=["fs", "search"]),
    Tool("web_search", "Recherche web (DuckDuckGo HTML). Nécessite un accès sortant.",
         _params({"query": _STR, "limit": _INT}, ["query"]),
         t_web_search, tags=["net"]),
    Tool("http_get", "Récupère le contenu d'une URL http(s).",
         _params({"url": _STR, "timeout": _INT}, ["url"]),
         t_http_get, tags=["net"]),
    Tool("shell", "Exécute une commande shell dans la sandbox (opt-in NEXUS_ALLOW_SHELL).",
         _params({"command": _STR, "timeout": _INT}, ["command"]),
         t_shell, risky=True, tags=["exec"]),
    Tool("python_exec", "Exécute du code Python dans la sandbox (opt-in NEXUS_ALLOW_SHELL).",
         _params({"code": _STR, "timeout": _INT}, ["code"]),
         t_python_exec, risky=True, tags=["exec"]),
    Tool("memory_remember", "Enregistre un fait, une décision ou une leçon en mémoire persistante.",
         _params({"content": _STR,
                  "kind": {"type": "string", "enum": ["fact", "decision", "lesson"]},
                  "tags": {**_STR, "description": "séparés par des virgules"}}, ["content"]),
         t_memory_remember, tags=["memory"]),
    Tool("memory_recall", "Rappelle les souvenirs pertinents pour une requête.",
         _params({"query": _STR, "kind": _STR, "limit": _INT}),
         t_memory_recall, tags=["memory"]),
    Tool("diagram", "Génère un diagramme Mermaid + page HTML de prévisualisation.",
         _params({"title": _STR, "mermaid": _STR,
                  "nodes": {**_STR, "description": "A, B, C"},
                  "edges": {**_STR, "description": "A-->B; B-->C"},
                  "kind": {**_STR, "description": "flowchart|graph|sequence"}}, ["title"]),
         t_diagram, tags=["produce", "diagram"]),
    Tool("compose_html", "Compose une page HTML autonome (rapport, landing, slide).",
         _params({"title": _STR, "html_body": _STR, "css": _STR}, ["title", "html_body"]),
         t_compose_html, tags=["produce", "html"]),
    Tool("handoff", "Délègue une sous-tâche à un autre agent de l'OS.",
         _params({"agent_id": _STR, "task": _STR}, ["agent_id", "task"]),
         t_handoff, tags=["meta"]),
    Tool("create_agent", "Crée un nouvel agent spécialisé via le créateur intégré.",
         _params({"description": _STR, "name": _STR}, ["description"]),
         t_create_agent, tags=["meta"]),
]

TOOL_BY_NAME: dict[str, Tool] = {t.name: t for t in BUILTIN_TOOLS}
META_TOOLS = {"handoff", "create_agent"}  # interceptés par le runtime


class ToolRegistry:
    def __init__(self, extra: list[Tool] | None = None) -> None:
        self.tools: dict[str, Tool] = dict(TOOL_BY_NAME)
        for t in extra or []:
            self.tools[t.name] = t

    def register(self, tool: Tool) -> None:
        self.tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self.tools.get(name)

    def names(self) -> list[str]:
        return sorted(self.tools)

    def select(self, names: list[str]) -> list[Tool]:
        return [self.tools[n] for n in names if n in self.tools]

    def specs(self, names: list[str]) -> list[dict[str, Any]]:
        return [t.spec() for t in self.select(names)]

    def execute(self, name: str, args: dict[str, Any], ctx: ToolContext | None = None) -> str:
        tool = self.tools.get(name)
        if not tool:
            raise ToolError(f"outil inconnu : {name}")
        ctx = ctx or ToolContext()
        args = {k: v for k, v in (args or {}).items() if k in tool.parameters.get("properties", {})}
        return tool.handler(ctx, **args)
