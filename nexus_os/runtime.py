"""Runtime d'agents : boucle d'exécution, cycle de vie, orchestration.

Le cycle (inspiré ECC) : ``plan → research → implement → review → verify →
remember → improve``. Chaque agent n'en garde que les phases qui le concernent.

Deux moteurs de décision :

* **live** — le modèle renvoie des appels d'outils (function calling) ;
* **offline** — `OfflinePlanner` choisit l'outil de la phase de façon
  déterministe. Les outils sont *réellement exécutés* dans les deux cas : seule
  la génération de texte change.

Architecture : `_run_impl()` est une fonction ordinaire qui pousse ses
événements dans un callback ; `run()` est le générateur public qui exécute
`_run_impl` dans un thread et **cède** les événements au fur et à mesure
(indispensable au streaming SSE, et à la délégation récursive entre agents).
"""
from __future__ import annotations

import queue
import re
import threading
import time
import traceback
from dataclasses import dataclass, field
from typing import Any, Callable, Generator, Sequence

from nexus_os import config
from nexus_os.agents import AgentSpec, registry as agent_registry
from nexus_os.db import store as db_store
from nexus_os.llm import Completion, complete, router as llm_router
from nexus_os.memory import memory
from nexus_os.providers import MODEL_INDEX, ModelRequest
from nexus_os.skills import library as skill_library
from nexus_os.tools import META_TOOLS, ToolContext, ToolError, ToolRegistry

PHASE_TITLES = {
    "plan": "Planification",
    "research": "Recherche",
    "implement": "Implémentation",
    "review": "Revue",
    "verify": "Vérification",
    "remember": "Mémorisation",
    "improve": "Amélioration",
}

Event = dict[str, Any]
STOP_WORDS = {"pour", "avec", "dans", "sur", "les", "des", "une", "que", "qui", "est", "par",
              "nexus", "agent", "faire", "tout", "plus", "sans", "mon", "mes", "notre"}


@dataclass
class RunResult:
    run_id: str
    agent_id: str
    status: str = "done"
    result: str = ""
    events: list[Event] = field(default_factory=list)
    steps: int = 0
    tokens: int = 0
    duration_ms: int = 0
    models: list[str] = field(default_factory=list)
    modes: list[str] = field(default_factory=list)
    artifacts: list[str] = field(default_factory=list)
    depth: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id, "agent_id": self.agent_id, "status": self.status,
            "result": self.result, "steps": self.steps, "tokens": self.tokens,
            "duration_ms": self.duration_ms, "models": self.models, "modes": self.modes,
            "artifacts": self.artifacts, "depth": self.depth, "events": self.events,
        }


@dataclass
class _Done:
    result: Any = None


# --------------------------------------------------------------------------- #
# Planificateur hors-ligne
# --------------------------------------------------------------------------- #
class OfflinePlanner:
    """Décide de l'action d'une phase sans modèle de langue (déterministe)."""

    def plan_for(self, phase: str, task: str, agent: AgentSpec,
                 observations: Sequence[str]) -> tuple[str | None, dict[str, Any]]:
        """Renvoie (outil, arguments) — ou (None, {}) si la phase n'agit pas."""
        tools = set(agent.tools)
        kw = _keywords(task)

        if phase == "research":
            if "web_search" in tools and config.ALLOW_NETWORK:
                return "web_search", {"query": " ".join(kw[:6]) or task[:80], "limit": 5}
            if "grep" in tools and kw:
                return "grep", {"pattern": kw[0], "limit": 20}
            if "list_dir" in tools:
                return "list_dir", {"path": ""}
            if "read_file" in tools:
                return "read_file", {"path": "README.md"}
        if phase == "implement":
            if "diagram" in tools:
                edges = "; ".join(f"{kw[i]}-->{kw[i+1]}" for i in range(min(5, len(kw) - 1)))
                return "diagram", {
                    "title": _slug(task) or "architecture",
                    "nodes": ", ".join(kw[:6]) or "Entrée, Traitement, Sortie",
                    **({"edges": edges} if edges else {}),
                }
            if "compose_html" in tools:
                body = "".join(f"<li>{o[:300]}</li>" for o in observations[:5]) or \
                    "<li>Aucune donnée collectée.</li>"
                return "compose_html", {"title": _slug(task) or "rapport",
                                        "html_body": f"<h1>{task[:120]}</h1><ul>{body}</ul>"}
            if "write_file" in tools:
                content = "\n".join(
                    [f"# {task.strip()}", "", "## Constats",
                     *(f"- {o[:400]}" for o in observations[:6]), "",
                     "_Généré par NEXUS·OS (mode hors-ligne)._"])
                return "write_file", {"path": f"{_slug(task) or 'livrable'}.md",
                                      "content": content}
        if phase == "review":
            if observations and "read_file" in tools:
                target = _first_workspace_path(observations[-1])
                if target:
                    return "read_file", {"path": target, "max_chars": 4000}
            if "grep" in tools and kw:
                return "grep", {"pattern": kw[-1], "limit": 10}
        if phase == "verify":
            if "python_exec" in tools:
                return "python_exec", {"code": "print('vérification : environnement Python OK')"}
            if "shell" in tools:
                return "shell", {"command": "ls -1 | head -20"}
        if phase == "remember":
            if "memory_remember" in tools:
                return "memory_remember", {
                    "content": f"[{agent.name}] {task[:160]} → {len(observations)} étape(s) exécutée(s)",
                    "kind": "lesson", "tags": ",".join(kw[:4])}
        return None, {}


def _keywords(text: str) -> list[str]:
    words = re.findall(r"[A-Za-zÀ-ÿ0-9][A-Za-zÀ-ÿ0-9_./-]{2,}", text or "")
    out: list[str] = []
    for w in words:
        if w.lower() in STOP_WORDS or w in out:
            continue
        out.append(w)
    return out[:10]


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", (text or "").lower()).strip("-")[:40]


def _first_workspace_path(text: str) -> str | None:
    """Chemin lisible par `read_file` pour un artefact annoncé par un outil.

    `read_file` est raciné sur le dépôt : si la sandbox vit ailleurs
    (NEXUS_HOME déplacé), l'artefact n'est pas relisible et on renvoie None
    plutôt qu'un chemin inventé.
    """
    m = re.search(r"workspace/([\w./-]+)", text or "")
    if not m:
        return None
    try:
        return str((config.WORKSPACE_DIR / m.group(1)).relative_to(config.READ_ROOT))
    except ValueError:
        return None


# --------------------------------------------------------------------------- #
# Runtime
# --------------------------------------------------------------------------- #
class Runtime:
    def __init__(self, *, agents=None, skills=None, tools: ToolRegistry | None = None,
                 planner: OfflinePlanner | None = None) -> None:
        self.agents = agents or agent_registry()
        self.skills = skills or skill_library()
        self.tools = tools or ToolRegistry()
        self.planner = planner or OfflinePlanner()
        self.db = db_store()

    # --- informations -------------------------------------------------------
    def status(self) -> dict[str, Any]:
        r = llm_router()
        return {
            "mode": "live" if r.is_live() else "offline",
            "agents": len(self.agents.all()),
            "skills": len(self.skills.all()),
            "tools": len(self.tools.names()),
            "models_ready": sum(1 for m in r.catalog() if m["ready"]),
            "models_total": len(r.catalog()),
            "memory_items": memory().count(),
            "db": self.db.stats(),
        }

    def route(self, task: str, limit: int = 5) -> list[dict[str, Any]]:
        """Qui doit traiter cette tâche ? (score d'affinité)"""
        return self.agents.ranking(task, limit=limit)

    # --- API publique (générateurs) -----------------------------------------
    def run(self, task: str, agent_id: str = "orchestrator", *,
            session_id: str | None = None, max_steps: int | None = None) -> Generator[Event, None, RunResult]:
        """Exécute un agent et **cède** chaque événement (streaming)."""
        q: queue.Queue = queue.Queue()

        def worker() -> None:
            try:
                res = self._run_impl(task, agent_id, session_id=session_id,
                                     max_steps=max_steps, depth=0, context="",
                                     emit=q.put)
                q.put(_Done(res))
            except Exception as e:  # le flux ne doit jamais mourir en silence
                q.put({"type": "error", "message": f"{type(e).__name__}: {e}\n"
                                                   f"{traceback.format_exc()[-600:]}"})
                q.put(_Done(RunResult(run_id="", agent_id=agent_id, status="error",
                                      result=f"échec : {e}")))

        threading.Thread(target=worker, daemon=True).start()
        while True:
            item = q.get()
            if isinstance(item, _Done):
                return item.result
            yield item

    def run_pipeline(self, task: str, agent_ids: Sequence[str], *,
                     session_id: str | None = None,
                     emit: Callable[[Event], None] | None = None) -> list[RunResult]:
        """Chaîne d'agents : la sortie de l'un devient le contexte du suivant."""
        unknown = [a for a in agent_ids if not self.agents.get(a)]
        if unknown:
            raise KeyError(f"agents inconnus : {', '.join(unknown)}")
        if not agent_ids:
            raise ValueError("chaîne vide")
        sink = emit or (lambda e: None)
        results: list[RunResult] = []
        context = ""
        for i, aid in enumerate(agent_ids, 1):
            sink({"type": "pipeline_step", "index": i, "total": len(agent_ids), "agent_id": aid})
            sub = self._run_impl(task, aid, session_id=session_id, max_steps=None, depth=0,
                                 context=context, emit=sink)
            results.append(sub)
            context = f"## Résultat de l'étape précédente ({aid})\n{sub.result[:3000]}"
        return results

    def stream_pipeline(self, task: str, agent_ids: Sequence[str], *,
                        session_id: str | None = None) -> Generator[Event, None, list[RunResult]]:
        """Version streamée de `run_pipeline`."""
        q: queue.Queue = queue.Queue()

        def worker() -> None:
            try:
                out = self.run_pipeline(task, agent_ids, session_id=session_id, emit=q.put)
                q.put(_Done(out))
            except Exception as e:
                q.put({"type": "error", "message": f"{type(e).__name__}: {e}"})
                q.put(_Done([]))

        threading.Thread(target=worker, daemon=True).start()
        while True:
            item = q.get()
            if isinstance(item, _Done):
                return item.result
            yield item

    # --- implémentation (fonction ordinaire, récursive) ---------------------
    def _run_impl(self, task: str, agent_id: str, *, session_id: str | None,
                  max_steps: int | None, depth: int, context: str,
                  emit: Callable[[Event], None]) -> RunResult:
        started = time.time()
        agent = self.agents.get(agent_id) or self.agents.require("orchestrator")
        run_id = self.db.start_run(agent.id, task, session_id)
        result = RunResult(run_id=run_id, agent_id=agent.id)
        result.depth = depth

        def ev(e: Event) -> None:
            result.events.append(e)
            emit(e)

        ev({"type": "run_start", "run_id": run_id, "agent": _agent_card(agent), "task": task,
            "mode": "live" if llm_router().is_live() else "offline",
            "phases": agent.lifecycle, "depth": depth})
        if session_id:
            self.db.add_message(session_id, "user", task, {"agent_id": agent.id})

        # --- routage (orchestrateur, niveau 0 uniquement) -------------------
        if agent.id == "orchestrator" and depth == 0:
            ranking = self.agents.ranking(task, limit=5)
            best = next((c for c in ranking
                         if c["agent_id"] != "orchestrator" and c["score"] > 1.5), None)
            ev({"type": "routing", "candidates": ranking, "chosen": best})
            if best:
                ev({"type": "handoff", "to": best["agent_id"], "task": task[:200]})
                sub = self._run_impl(task, best["agent_id"], session_id=None,
                                     max_steps=max_steps, depth=depth + 1, context="",
                                     emit=emit)
                _merge(result, sub)
                ev({"type": "consolidation", "from": best["agent_id"],
                    "text": sub.result[:1500]})
                result.result = _consolidate(task, best, sub.result)
                ev({"type": "message", "text": result.result, "model": "nexus-router",
                    "provider": "router", "mode": "router", "depth": depth,
                    "final": True})
                self._finish(result, started, ev, session_id)
                return result

        # --- boucle par phases ----------------------------------------------
        observations: list[str] = []
        steps = max_steps or agent.max_steps
        skill_objs = list({s.name: s for s in
                           (self.skills.select(agent.skills) + self.skills.match(task, limit=2))
                           }.values())
        system_prompt = agent.base_prompt(self.skills.render(skill_objs),
                                          memory().render(task, limit=4))
        tool_specs = self.tools.specs(agent.tools)
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": (context + "\n\n" if context else "") + task},
        ]

        for idx, phase in enumerate(agent.lifecycle[:steps]):
            ev({"type": "phase", "phase": phase, "title": PHASE_TITLES.get(phase, phase),
                "index": idx + 1, "total": min(steps, len(agent.lifecycle))})
            result.steps += 1

            comp: Completion = complete(
                messages,
                request=ModelRequest(preferred=agent.model or None, need_tools=bool(tool_specs)),
                tools=tool_specs, temperature=agent.temperature, max_tokens=900)
            result.models.append(comp.model)
            result.modes.append(comp.mode)
            result.tokens += comp.tokens
            ev({"type": "thinking", "phase": phase, "text": comp.text[:1200],
                "model": comp.model, "provider": comp.provider, "mode": comp.mode})

            calls = [(c.name, c.arguments) for c in comp.tool_calls]
            if not calls and comp.mode != "live":
                name, args = self.planner.plan_for(phase, task, agent, observations)
                if name:
                    calls = [(name, args)]

            for name, args in calls[:2]:
                if name == "handoff":
                    obs = self._delegate(str(args.get("agent_id", "")),
                                         str(args.get("task") or task), ev, depth, result)
                elif name == "create_agent":
                    obs = self._create_agent(args, ev)
                else:
                    obs = self._exec_tool(name, args, agent.id, ev, result)
                if obs:
                    observations.append(obs)
                    messages.append({"role": "tool", "name": name, "content": obs[:4000]})

        # --- synthèse finale --------------------------------------------------
        final_comp = complete(
            messages + [{"role": "user",
                         "content": "Produis maintenant la réponse finale, au format imposé."}],
            request=ModelRequest(preferred=agent.model or None),
            temperature=agent.temperature, max_tokens=1200)
        result.models.append(final_comp.model)
        result.modes.append(final_comp.mode)
        result.tokens += final_comp.tokens
        result.result = (final_comp.text if final_comp.mode == "live"
                         else _compose_offline(task, agent, skill_objs, observations))
        ev({"type": "message", "text": result.result, "model": final_comp.model,
            "provider": final_comp.provider, "mode": final_comp.mode,
            "usage": final_comp.usage, "depth": depth, "final": depth == 0})
        self._finish(result, started, ev, session_id)
        return result

    # --- outillage -----------------------------------------------------------
    def _exec_tool(self, name: str, args: dict[str, Any], agent_id: str,
                   emit: Callable[[Event], None], result: RunResult) -> str:
        emit({"type": "tool_call", "name": name, "args": args})
        if name in META_TOOLS:
            emit({"type": "tool_result", "name": name, "ok": False,
                  "result": "outil méta : à traiter par le runtime, pas par le registre"})
            return "outil méta non exécutable ici"
        ctx = ToolContext(agent_id=agent_id, emit=emit)
        try:
            out, ok = self.tools.execute(name, args or {}, ctx), True
        except ToolError as e:
            out, ok = f"refusé : {e}", False
        except Exception as e:  # un outil ne doit jamais tuer un run
            out, ok = f"erreur {type(e).__name__}: {e}", False
        emit({"type": "tool_result", "name": name, "ok": ok,
              "result": out[:config.MAX_TOOL_RESULT_CHARS]})
        for m in re.finditer(r"workspace/([\w./-]+)", out):
            art = f"workspace/{m.group(1)}"
            if art not in result.artifacts:
                result.artifacts.append(art)
                emit({"type": "artifact", "path": art})
        return out

    def _delegate(self, agent_id: str, task: str, emit: Callable[[Event], None],
                  depth: int, result: RunResult) -> str:
        if not self.agents.get(agent_id):
            return f"agent inconnu : {agent_id}"
        if depth >= 2:
            emit({"type": "log", "message": f"profondeur max atteinte, {agent_id} non délégué"})
            return "profondeur de délégation maximale atteinte"
        emit({"type": "handoff", "to": agent_id, "task": task[:200]})
        sub = self._run_impl(task, agent_id, session_id=None, max_steps=None,
                             depth=depth + 1, context="", emit=emit)
        _merge(result, sub)
        return sub.result

    def _create_agent(self, args: dict[str, Any], emit: Callable[[Event], None]) -> str:
        """Outil méta : l'OS crée un nouvel agent spécialisé (auto-construction)."""
        from nexus_os.creator import create_and_save

        emit({"type": "tool_call", "name": "create_agent", "args": args})
        try:
            res = create_and_save(str(args.get("description", "")),
                                  name=str(args.get("name", "")), use_llm=False)
        except Exception as e:
            msg = f"création impossible : {e}"
            emit({"type": "tool_result", "name": "create_agent", "ok": False, "result": msg})
            return msg
        emit({"type": "agent_created", "agent": _agent_card(res.spec), "rationale": res.rationale})
        msg = f"agent créé : {res.spec.id} ({res.spec.name}) — {len(res.spec.tools)} outils"
        emit({"type": "tool_result", "name": "create_agent", "ok": True, "result": msg})
        return msg

    def _finish(self, result: RunResult, started: float, emit: Callable[[Event], None],
                session_id: str | None) -> None:
        result.duration_ms = int((time.time() - started) * 1000)
        model = result.models[-1] if result.models else None
        provider = MODEL_INDEX[model][0].id if model in MODEL_INDEX else "local"
        modes = set(result.modes)
        mode = "live" if modes == {"live"} else ("mixed" if modes else "offline")
        self.db.finish_run(
            result.run_id, status=result.status, result=result.result,
            phases=[e.get("phase") for e in result.events if e.get("type") == "phase"],
            model=model, provider=provider, mode=mode, tokens=result.tokens,
            steps=result.steps, duration_ms=result.duration_ms)
        if session_id:
            self.db.add_message(session_id, "assistant", result.result,
                                {"run_id": result.run_id, "model": model,
                                 "artifacts": result.artifacts})
        emit({"type": "run_end", "run_id": result.run_id, "status": result.status,
              "depth": result.depth,
              "tokens": result.tokens, "steps": result.steps,
              "duration_ms": result.duration_ms, "artifacts": result.artifacts,
              "model": model, "mode": mode})


def _merge(target: RunResult, sub: RunResult) -> None:
    target.tokens += sub.tokens
    target.steps += sub.steps
    target.artifacts += [a for a in sub.artifacts if a not in target.artifacts]
    target.models += sub.models
    target.modes += sub.modes


def _agent_card(a: AgentSpec) -> dict[str, Any]:
    return {"id": a.id, "name": a.name, "emoji": a.emoji, "role": a.role, "skills": a.skills,
            "tools": a.tools, "lifecycle": a.lifecycle, "source": a.source,
            "autonomy": a.autonomy, "model": a.model}


def _consolidate(task: str, best: dict[str, Any], sub_result: str) -> str:
    return (f"**Prochaine action** — la tâche « {task[:100]} » relève de "
            f"{best['name']} (score {best['score']}).\n\n" + sub_result.strip())


def _compose_offline(task: str, agent: AgentSpec, skills: Sequence[Any],
                     observations: Sequence[str]) -> str:
    from nexus_os.llm import _synthesize

    return _synthesize(task, agent_name=agent.name, role=agent.role,
                       skills=[s.name for s in skills], observations=observations)
