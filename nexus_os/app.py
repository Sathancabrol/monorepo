"""Interface HTTP de NEXUS·OS : API JSON + flux SSE + UI « bureau ».

Montable dans le monorepo (`app.mount("/os", nexus_app)`) ou lançable seul :

    uvicorn nexus_os.app:app --host 0.0.0.0 --port 8124
"""
from __future__ import annotations

import json
import mimetypes
import time
from pathlib import Path
from typing import Any

from fastapi import Body, FastAPI, HTTPException, Query, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from nexus_os import __version__, config
from nexus_os.agents import AgentSpec, registry as agent_registry
from nexus_os.creator import create_and_save, draft
from nexus_os import context as context_mod
from nexus_os import harness as harness_mod
from nexus_os import mcp as mcp_mod
from nexus_os.instincts import book as instincts
from nexus_os.db import store as db_store
from nexus_os.llm import router as llm_router, system_mode
from nexus_os.memory import memory
from nexus_os.runtime import Runtime
from nexus_os.skills import library as skill_library
from nexus_os.tools import ToolRegistry

app = FastAPI(title="NEXUS·OS — Agentic Operating System", version=__version__)
templates = Jinja2Templates(directory=str(config.TEMPLATES_DIR))
app.mount("/static", StaticFiles(directory=str(config.STATIC_DIR)), name="static")

rt = Runtime()
agents = agent_registry()
skills = skill_library()
tools = ToolRegistry()


# --------------------------------------------------------------------------- #
# Pages
# --------------------------------------------------------------------------- #
@app.get("/", response_class=HTMLResponse)
@app.get("/os", response_class=HTMLResponse)
@app.get("/os/", response_class=HTMLResponse)
def desktop(request: Request) -> HTMLResponse:
    """Le bureau de l'OS.

    Servi à la racine *et* sous ``/os`` : l'application est conçue pour être
    montée dans le monorepo (`app.mount("/os", nexus_app)`) comme pour tourner
    seule. L'UI n'utilise que des URLs relatives, les deux cas fonctionnent.
    """
    return templates.TemplateResponse(request, "os.html", {
        "version": __version__,
        "mode": system_mode()["mode"],
    })


@app.get("/health")
def health() -> dict[str, Any]:
    return {"ok": True, "version": __version__, **rt.status()}


# --------------------------------------------------------------------------- #
#État du système : routeur, modèles, fournisseurs
# --------------------------------------------------------------------------- #
@app.get("/api/status")
def api_status() -> dict[str, Any]:
    return {
        "version": __version__,
        "runtime": rt.status(),
        "mode_info": system_mode(),
        "flags": {
            "shell": config.ALLOW_SHELL,
            "network": config.ALLOW_NETWORK,
            "max_steps": config.MAX_AGENT_STEPS,
            "workspace": str(config.WORKSPACE_DIR),
        },
    }


@app.get("/api/providers")
def api_providers() -> list[dict[str, Any]]:
    return llm_router().providers_status()


@app.get("/api/models")
def api_models() -> list[dict[str, Any]]:
    return llm_router().catalog()


# --------------------------------------------------------------------------- #
# Agents
# --------------------------------------------------------------------------- #
@app.get("/api/agents")
def api_agents() -> list[dict[str, Any]]:
    return [a.to_dict() for a in agents.all()]


@app.get("/api/agents/{agent_id}")
def api_agent(agent_id: str) -> dict[str, Any]:
    a = agents.get(agent_id)
    if not a:
        raise HTTPException(404, f"agent inconnu : {agent_id}")
    return {"spec": a.to_dict(), "markdown": agents.export_markdown(a)}


@app.post("/api/agents")
def api_agent_save(spec: dict[str, Any] = Body(...)) -> dict[str, Any]:
    try:
        a = AgentSpec.from_dict(spec)
    except TypeError as e:
        raise HTTPException(400, f"spec invalide : {e}")
    if not a.id or not a.name:
        raise HTTPException(400, "`id` et `name` requis")
    unknown = [t for t in a.tools if t not in tools.names()]
    if unknown:
        raise HTTPException(400, f"outils inconnus : {', '.join(unknown)}")
    saved = agents.save(a)
    return {"ok": True, "agent": saved.to_dict()}


@app.delete("/api/agents/{agent_id}")
def api_agent_delete(agent_id: str) -> dict[str, Any]:
    if not agents.delete(agent_id):
        raise HTTPException(404, "agent intégré ou introuvable : suppression refusée")
    return {"ok": True}


@app.post("/api/agents/draft")
def api_agent_draft(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    """Génère une spec sans l'enregistrer (aperçu du créateur)."""
    try:
        res = draft(str(payload.get("description", "")), name=str(payload.get("name", "")),
                    model=str(payload.get("model", "")),
                    autonomy=str(payload.get("autonomy", "assisté")),
                    use_llm=bool(payload.get("use_llm", True)))
    except ValueError as e:
        raise HTTPException(400, str(e))
    return res.to_dict()


@app.post("/api/agents/create")
def api_agent_create(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    try:
        res = create_and_save(str(payload.get("description", "")),
                              name=str(payload.get("name", "")),
                              model=str(payload.get("model", "")),
                              autonomy=str(payload.get("autonomy", "assisté")),
                              use_llm=bool(payload.get("use_llm", True)))
    except ValueError as e:
        raise HTTPException(400, str(e))
    return res.to_dict()


@app.get("/api/agents/{agent_id}/export", response_class=FileResponse)
def api_agent_export(agent_id: str) -> FileResponse:
    a = agents.get(agent_id)
    if not a:
        raise HTTPException(404, f"agent inconnu : {agent_id}")
    out = config.WORKSPACE_DIR / f"agent-{a.id}.md"
    out.write_text(agents.export_markdown(a), encoding="utf-8")
    return FileResponse(str(out), media_type="text/markdown", filename=out.name)


# --------------------------------------------------------------------------- #
# Portabilité vers les autres harness (Claude Code, Codex, Cline, Hermes…)
# --------------------------------------------------------------------------- #
@app.get("/api/harnesses")
def api_harnesses() -> list[dict[str, Any]]:
    return harness_mod.list_targets()


@app.get("/api/agents/{agent_id}/harness")
def api_agent_harness_overview(agent_id: str) -> dict[str, Any]:
    a = agents.get(agent_id)
    if not a:
        raise HTTPException(404, f"agent inconnu : {agent_id}")
    return harness_mod.summarize(a)


@app.get("/api/agents/{agent_id}/harness/{target}")
def api_agent_harness(agent_id: str, target: str, save: bool = Query(False)) -> dict[str, Any]:
    a = agents.get(agent_id)
    if not a:
        raise HTTPException(404, f"agent inconnu : {agent_id}")
    try:
        content = harness_mod.export_spec(a, target)
        filename = harness_mod.filename_for(target, a)
    except KeyError as e:
        raise HTTPException(400, str(e))
    saved_to = None
    if save:
        out = config.WORKSPACE_DIR / "harness" / target / filename
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(content, encoding="utf-8")
        saved_to = f"workspace/harness/{target}/{filename}"
    return {"agent_id": agent_id, "target": target, "filename": filename,
            "content": content, "saved_to": saved_to,
            "bytes": len(content.encode("utf-8"))}


# --------------------------------------------------------------------------- #
# Compétences & outils
# --------------------------------------------------------------------------- #
# --------------------------------------------------------------------------- #
# MCP — Model Context Protocol (révision 2026-07-28, cœur stateless)
# --------------------------------------------------------------------------- #
@app.get("/api/mcp")
def api_mcp() -> dict[str, Any]:
    return mcp_mod.summarize()


@app.post("/api/mcp")
def api_mcp_add(payload: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    try:
        srv = mcp_mod.add_server(str(payload.get("name", "")), str(payload.get("url", "")),
                                 description=str(payload.get("description", "")),
                                 auth_env=str(payload.get("auth_env", "")),
                                 headers=payload.get("headers") or {})
    except ValueError as e:
        raise HTTPException(400, str(e)) from e
    rt.tools.refresh_mcp()      # les outils du serveur sont utilisables aussitôt
    return {"ok": True, "server": srv.to_dict(), "status": api_status()["runtime"],
            "mcp_tools": [t.name for t in rt.tools.select(
                [n for n in rt.tools.names() if n.startswith("mcp__")])]}


@app.delete("/api/mcp/{name}")
def api_mcp_remove(name: str) -> dict[str, Any]:
    if not mcp_mod.remove_server(name):
        raise HTTPException(404, f"serveur inconnu : {name}")
    rt.tools.refresh_mcp()
    return {"ok": True, "removed": name}


@app.get("/api/mcp/{name}/probe")
def api_mcp_probe(name: str) -> dict[str, Any]:
    cfg = mcp_mod.get_server(name)
    if not cfg:
        raise HTTPException(404, f"serveur inconnu : {name}")
    return mcp_mod.probe(cfg)


# --------------------------------------------------------------------------- #
# Instincts (couche d'apprentissage) & contexte référencé
# --------------------------------------------------------------------------- #
@app.get("/api/instincts")
def api_instincts(task: str = Query(""), agent: str = Query("")) -> dict[str, Any]:
    rows = instincts().for_task(task, agent) if task else instincts().all()
    return {"count": instincts().count(),
            "injected": len(rows),
            "items": [i.to_dict() for i in (rows or instincts().all())]}


@app.post("/api/instincts")
def api_instinct_add(payload: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    try:
        inst = instincts().add(
            str(payload.get("rule", "")),
            triggers=[t.strip() for t in str(payload.get("triggers", "")).split(",") if t.strip()],
            agent_id=str(payload.get("agent_id", "")), source="manuel")
    except ValueError as e:
        raise HTTPException(400, str(e)) from e
    return {"ok": True, "instinct": inst.to_dict(), "count": instincts().count()}


@app.delete("/api/instincts/{instinct_id}")
def api_instinct_forget(instinct_id: str) -> dict[str, Any]:
    if not instincts().forget(instinct_id):
        raise HTTPException(404, f"instinct inconnu : {instinct_id}")
    return {"ok": True, "forgotten": instinct_id}


@app.get("/api/context")
def api_context() -> dict[str, Any]:
    return context_mod.stats()


@app.delete("/api/context")
def api_context_clear() -> dict[str, Any]:
    return {"ok": True, "cleared": context_mod.clear()}


# --------------------------------------------------------------------------- #
# A2A — un agent NEXUS·OS délégable depuis un autre agent
# --------------------------------------------------------------------------- #
@app.get("/api/a2a/{agent_id}/card")
def api_a2a_card(agent_id: str) -> dict[str, Any]:
    import json as _json

    spec = agents.get(agent_id)
    if not spec:
        raise HTTPException(404, f"agent inconnu : {agent_id}")
    return _json.loads(harness_mod.export_spec(spec, "a2a"))


@app.post("/api/a2a/{agent_id}")
def api_a2a_send(agent_id: str, payload: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    """`message/send` A2A : un agent externe délègue et reçoit une tâche A2A."""
    spec = agents.get(agent_id)
    if not spec:
        raise HTTPException(404, f"agent inconnu : {agent_id}")
    if payload.get("method") not in {None, "message/send"}:
        raise HTTPException(400, f"méthode non prise en charge : {payload.get('method')}")
    parts = (((payload.get("params") or {}).get("message") or {}).get("parts") or [])
    text = " ".join(str(p.get("text", "")) for p in parts if isinstance(p, dict)).strip()
    if not text:
        raise HTTPException(400, "params.message.parts[].text est requis")

    events, result = _collect(rt.run(text, agent_id))
    return {
        "jsonrpc": "2.0", "id": payload.get("id", 1),
        "result": {
            "kind": "task", "id": result.run_id,
            "contextId": f"nexus-{agent_id}",
            "status": {"state": "completed" if result.status == "done" else "failed",
                       "timestamp": int(time.time() * 1000)},
            "artifacts": [{
                "artifactId": f"a{i}", "name": a.split("/")[-1],
                "parts": [{"kind": "text", "text": a}],
            } for i, a in enumerate(result.artifacts)],
            "history": [{"kind": "message", "role": "agent", "messageId": result.run_id,
                         "parts": [{"kind": "text", "text": result.result}]}],
            "metadata": {"agent": agent_id, "steps": result.steps,
                         "tokens": result.tokens, "confidence": result.confidence,
                         "events": len(events)},
        },
    }


@app.get("/api/skills")
def api_skills() -> list[dict[str, Any]]:
    return [s.to_dict() for s in skills.all()]


@app.get("/api/skills/{name}")
def api_skill(name: str) -> dict[str, Any]:
    s = skills.get(name)
    if not s:
        raise HTTPException(404, f"compétence inconnue : {name}")
    return s.to_dict(with_body=True)


# --------------------------------------------------------------------------- #
# Routage & exécution
# --------------------------------------------------------------------------- #
@app.post("/api/route")
def api_route(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    task = str(payload.get("task", "")).strip()
    if not task:
        raise HTTPException(400, "`task` requis")
    ranking = rt.route(task, limit=6)
    best = next((c for c in ranking if c["agent_id"] != "orchestrator" and c["score"] > 1.5), None)
    return {"ranking": ranking, "suggested": best or (ranking[0] if ranking else None)}


def _sse(payload: dict[str, Any]) -> str:
    return f"data: {json.dumps(payload, ensure_ascii=False, default=str)}\n\n"


def _collect(gen: Any) -> tuple[list[dict[str, Any]], Any]:
    """Consomme un générateur d'événements et rend (événements, RunResult)."""
    events: list[dict[str, Any]] = []
    try:
        while True:
            events.append(next(gen))
    except StopIteration as stop:
        return events, stop.value


def _stream(gen) -> StreamingResponse:
    def body():
        yield _sse({"type": "stream_open"})
        try:
            while True:
                ev = next(gen)
                yield _sse(ev)
        except StopIteration as stop:
            value = stop.value
            if isinstance(value, list):
                yield _sse({"type": "result", "runs": [r.to_dict() for r in value]})
            elif value is not None:
                yield _sse({"type": "result", **value.to_dict()})
        except Exception as e:  # jamais de flux muet
            yield _sse({"type": "error", "message": f"{type(e).__name__}: {e}"})
        finally:
            yield _sse({"type": "stream_close"})

    return StreamingResponse(body(), media_type="text/event-stream", headers={
        "Cache-Control": "no-cache", "X-Accel-Buffering": "no", "Connection": "keep-alive",
    })


@app.get("/api/run")
def api_run(task: str = Query(..., min_length=1), agent: str = Query("orchestrator"),
            session_id: str | None = Query(None),
            approval: str = Query("smart", pattern="^(off|manuel|smart)$"),
            approve: str = Query("", description="outils pré-autorisés, séparés par virgules"),
            max_steps: int | None = Query(None, ge=1, le=20)) -> StreamingResponse:
    if not agents.get(agent):
        raise HTTPException(404, f"agent inconnu : {agent}")
    return _stream(rt.run(task, agent, session_id=session_id, approval=approval,
                          approved_tools=[t for t in approve.split(",") if t.strip()],
                          max_steps=max_steps))


@app.get("/api/pipeline")
def api_pipeline(task: str = Query(..., min_length=1),
                 agents_chain: str = Query(..., description="ids séparés par des virgules"),
                 session_id: str | None = Query(None),
                 approval: str = Query("smart", pattern="^(off|manuel|smart)$"),
                 approve: str = Query("")) -> StreamingResponse:
    chain = [a.strip() for a in agents_chain.split(",") if a.strip()]
    unknown = [a for a in chain if not agents.get(a)]
    if unknown:
        raise HTTPException(404, f"agents inconnus : {', '.join(unknown)}")
    if not chain:
        raise HTTPException(400, "chaîne vide")
    return _stream(rt.stream_pipeline(task, chain, session_id=session_id, approval=approval,
                                      approved_tools=[t for t in approve.split(",") if t.strip()]))


@app.get("/api/parallel")
def api_parallel(task: str = Query(..., min_length=1),
                 agents_list: str = Query(..., description="ids séparés par des virgules"),
                 session_id: str | None = Query(None),
                 approval: str = Query("smart", pattern="^(off|manuel|smart)$"),
                 approve: str = Query("")) -> StreamingResponse:
    """Flotte : plusieurs agents travaillent en même temps sur la même tâche."""
    crew = [a.strip() for a in agents_list.split(",") if a.strip()]
    unknown = [a for a in crew if not agents.get(a)]
    if unknown:
        raise HTTPException(404, f"agents inconnus : {', '.join(unknown)}")
    if len(crew) < 2:
        raise HTTPException(400, "au moins 2 agents pour une exécution parallèle")
    return _stream(rt.stream_parallel(task, crew, session_id=session_id, approval=approval,
                                      approved_tools=[t for t in approve.split(",") if t.strip()]))


@app.get("/api/board")
def api_board() -> dict[str, Any]:
    from nexus_os.tools import BOARD_COLUMNS, _board_load

    items = _board_load()
    return {"columns": list(BOARD_COLUMNS), "count": len(items), "items": items}


@app.post("/api/board")
def api_board_change(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    from nexus_os.tools import BOARD_COLUMNS, ToolContext, ToolRegistry, t_task_board

    action = str(payload.get("action", "add"))
    if action not in {"list", "add", "move", "done", "remove"}:
        raise HTTPException(400, f"action inconnue : {action}")
    column = str(payload.get("column", ""))
    if action in {"add", "move"} and column not in BOARD_COLUMNS:
        raise HTTPException(400, f"colonne parmi : {', '.join(BOARD_COLUMNS)}")
    try:
        out = t_task_board(ToolContext(), action=action, title=str(payload.get("title", "")),
                           agent=str(payload.get("agent", "")), column=column,
                           task_id=str(payload.get("task_id", "")))
    except Exception as e:
        raise HTTPException(400, str(e))
    return {"ok": True, "message": out}


@app.get("/api/tools")
def api_tools() -> list[dict[str, Any]]:
    out = []
    for t in tools.tools.values():
        out.append({**t.spec(), "risky": t.risky, "tags": t.tags})
    return sorted(out, key=lambda x: x["name"])


@app.get("/api/runs")
def api_runs(limit: int = 40) -> list[dict[str, Any]]:
    return db_store().list_runs(limit=limit)


@app.get("/api/usage")
def api_usage() -> dict[str, Any]:
    return {"today": db_store().usage_today(), "stats": db_store().stats()}


# --------------------------------------------------------------------------- #
# Sessions & mémoire
# --------------------------------------------------------------------------- #
@app.get("/api/sessions")
def api_sessions() -> list[dict[str, Any]]:
    return db_store().list_sessions()


@app.post("/api/sessions")
def api_session_create(payload: dict[str, Any] = Body(default={})) -> dict[str, Any]:
    agent_id = str(payload.get("agent_id", "orchestrator"))
    if not agents.get(agent_id):
        raise HTTPException(404, f"agent inconnu : {agent_id}")
    return db_store().create_session(agent_id, str(payload.get("title", "")))


@app.get("/api/sessions/{session_id}/messages")
def api_session_messages(session_id: str) -> list[dict[str, Any]]:
    return db_store().messages(session_id)


@app.get("/api/memory")
def api_memory(q: str = "", limit: int = 30) -> dict[str, Any]:
    items = memory().recall(q, limit=limit) if q else memory().recent(limit=limit)
    return {"count": memory().count(), "items": items}


@app.post("/api/memory")
def api_memory_add(payload: dict[str, Any] = Body(...)) -> dict[str, Any]:
    content = str(payload.get("content", "")).strip()
    if not content:
        raise HTTPException(400, "`content` requis")
    return memory().remember(content, kind=str(payload.get("kind", "fact")),
                             tags=[t for t in str(payload.get("tags", "")).split(",") if t.strip()])


@app.delete("/api/memory/{item_id}")
def api_memory_delete(item_id: str) -> dict[str, Any]:
    if not memory().forget(item_id):
        raise HTTPException(404, "souvenir introuvable")
    return {"ok": True}


# --------------------------------------------------------------------------- #
# Espace de travail (artefacts produits par les agents)
# --------------------------------------------------------------------------- #
@app.get("/workspace/{path:path}")
def workspace_file(path: str):
    root = config.WORKSPACE_DIR.resolve()
    target = (root / path).resolve()
    if root not in target.parents and target != root:
        raise HTTPException(400, "chemin invalide")
    if not target.exists():
        raise HTTPException(404, "fichier introuvable")
    if target.is_dir():
        return JSONResponse([
            {"name": p.name, "path": str(p.relative_to(root)), "is_dir": p.is_dir()}
            for p in sorted(target.iterdir())
        ])
    return FileResponse(str(target), media_type=mimetypes.guess_type(str(target))[0]
                        or "application/octet-stream")


@app.get("/workspace")
def workspace_root() -> JSONResponse:
    return workspace_file("")


if __name__ == "__main__":  # pragma: no cover
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8124)
