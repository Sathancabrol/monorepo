"""Évaluations — un barème reproductible pour les agents.

Pourquoi : un agent qui « a l'air de marcher » n'est pas un agent qui marche.
Sans barème, chaque modification du prompt, du planificateur ou d'un outil se
juge à l'œil, et la régression arrive en production.

Chaque cas est une **attente vérifiable hors-ligne** sur une exécution réelle :
artéfact produit ou non, outil en échec ou non, confiance annoncée, outils
effectivement appelés, étapes minimales, mentions obligatoires dans la réponse.
Aucun appel LLM : le barème est déterministe et tourne dans les tests.

    python -m nexus_os evals            # tout le barème
    python -m nexus_os evals coder      # un seul agent
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from nexus_os import config

EVALS_FILE = config.NEXUS_HOME / "evals.json"


@dataclass
class Case:
    id: str
    agent_id: str
    task: str
    #: Attentes — toutes doivent tenir pour que le cas passe.
    produces_artifact: bool | None = None
    no_tool_failure: bool = True
    confidence: str | None = None            # "confiant" | "à vérifier" | None = indifférent
    min_steps: int = 0
    tools_used: tuple[str, ...] = ()         # au moins un de ces outils doit être appelé
    mentions: tuple[str, ...] = ()           # sous-chaînes attendues dans la réponse
    forbidden: tuple[str, ...] = ()          # sous-chaînes interdites

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "agent_id": self.agent_id, "task": self.task,
                "produces_artifact": self.produces_artifact,
                "no_tool_failure": self.no_tool_failure, "confidence": self.confidence,
                "min_steps": self.min_steps, "tools_used": list(self.tools_used),
                "mentions": list(self.mentions), "forbidden": list(self.forbidden)}


#: Le barème intégré. Un cas par capacité que l'OS promet.
SUITE: tuple[Case, ...] = (
    Case("coder-ecrit-un-livrable", "coder",
         "Implémente une fonction qui calcule la médiane d'une liste et documente-la",
         produces_artifact=True, tools_used=("write_file",), min_steps=1),
    Case("architecte-dessine", "architect",
         "Conçois l'architecture de NEXUS·OS et produis un diagramme",
         produces_artifact=True, tools_used=("diagram",)),
    Case("chercheur-cite", "researcher",
         "Fais l'état de l'art des routeurs de modèles multi-fournisseurs",
         min_steps=1, forbidden=("je ne peux pas",)),
    Case("relecteur-audite", "reviewer",
         "Fais la revue de sécurité de nexus_os/tools.py",
         tools_used=("grep", "read_file", "list_dir"), min_steps=1),
    Case("analyste-chiffre", "analyst",
         "Analyse la consommation de tokens du jour et produis un graphique",
         produces_artifact=True, tools_used=("render_chart", "python_exec", "read_file")),
    Case("redacteur-structure", "writer",
         "Rédige la page d'accueil de NEXUS·OS : promesse, preuve, mécanisme, objection, action",
         min_steps=1),
    Case("juriste-cite-la-source", "jurist",
         "Relis cette clause de résiliation et liste les risques",
         min_steps=1),
    Case("testeur-verifie", "qa",
         "Écris les cas de test de la fonction slugify du créateur d'agent",
         min_steps=1),
    Case("orchestrateur-delegue", "orchestrator",
         "Audite la structure du dépôt et produis un rapport détaillé",
         min_steps=1),
    Case("devops-prepare", "devops",
         "Prépare la procédure de déploiement de l'API FastAPI de ce dépôt",
         min_steps=1),
)


@dataclass
class CaseResult:
    id: str
    agent_id: str
    passed: bool
    checks: list[dict[str, Any]] = field(default_factory=list)
    duration_ms: int = 0
    error: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "agent_id": self.agent_id, "passed": self.passed,
                "checks": self.checks, "duration_ms": self.duration_ms, "error": self.error}


def _check(label: str, ok: bool, detail: str = "") -> dict[str, Any]:
    return {"check": label, "ok": bool(ok), "detail": detail}


def run_case(case: Case) -> CaseResult:
    """Exécute réellement l'agent et confronte le résultat aux attentes."""
    from nexus_os.runtime import Runtime

    started = time.time()
    try:
        gen = Runtime().run(case.task, case.agent_id, approval="off")
        events: list[dict[str, Any]] = []
        try:
            while True:
                events.append(next(gen))
        except StopIteration as stop:
            res = stop.value
    except Exception as e:
        return CaseResult(case.id, case.agent_id, False,
                          duration_ms=int((time.time() - started) * 1000),
                          error=f"{type(e).__name__}: {e}")

    checks: list[dict[str, Any]] = []
    text = (res.result or "").lower()
    tools = {e.get("name") for e in res.events if e.get("type") == "tool_call"}

    if case.produces_artifact is not None:
        checks.append(_check("artéfact", bool(res.artifacts) is case.produces_artifact,
                             ", ".join(res.artifacts) or "aucun"))
    if case.no_tool_failure:
        checks.append(_check("aucun outil en échec", res.tool_failures == 0,
                             f"{res.tool_failures} échec(s)"))
    if case.confidence:
        checks.append(_check("confiance", res.confidence == case.confidence, res.confidence))
    if case.min_steps:
        checks.append(_check("étapes", res.steps >= case.min_steps, f"{res.steps} étape(s)"))
    if case.tools_used:
        hit = sorted(tools & set(case.tools_used))
        checks.append(_check("outils", bool(hit),
                             ", ".join(hit) or f"aucun de {', '.join(case.tools_used)}"))
    for m in case.mentions:
        checks.append(_check(f"mentionne « {m} »", m.lower() in text))
    for f in case.forbidden:
        checks.append(_check(f"n'écrit pas « {f} »", f.lower() not in text))

    passed = all(c["ok"] for c in checks) and res.status == "done"
    return CaseResult(case.id, case.agent_id, passed, checks,
                      int((time.time() - started) * 1000))


def run_suite(agent_id: str | None = None, *, cases: tuple[Case, ...] = SUITE,
              save: bool = True) -> dict[str, Any]:
    """Barème complet. `agent_id` restreint à un agent."""
    selected = [c for c in cases if not agent_id or c.agent_id == agent_id]
    if not selected:
        raise KeyError(f"aucun cas d'évaluation pour : {agent_id}")
    results = [run_case(c) for c in selected]
    passed = sum(1 for r in results if r.passed)
    scorecard = {
        "agent_id": agent_id or "*",
        "cases": len(results),
        "passed": passed,
        "failed": len(results) - passed,
        "score": round(passed / len(results), 3),
        "duration_ms": sum(r.duration_ms for r in results),
        "results": [r.to_dict() for r in results],
        "run_at": time.time(),
    }
    if save:
        EVALS_FILE.parent.mkdir(parents=True, exist_ok=True)
        EVALS_FILE.write_text(json.dumps(scorecard, ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")
    return scorecard


def last() -> dict[str, Any] | None:
    if not EVALS_FILE.exists():
        return None
    try:
        return json.loads(EVALS_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def suite() -> list[dict[str, Any]]:
    return [c.to_dict() for c in SUITE]


def render(scorecard: dict[str, Any]) -> str:
    lines = [f"Barème {scorecard['agent_id']} — {scorecard['passed']}/{scorecard['cases']} "
             f"({scorecard['score'] * 100:.0f} %) en {scorecard['duration_ms']} ms"]
    for r in scorecard["results"]:
        mark = "✓" if r["passed"] else "✗"
        lines.append(f"{mark} {r['id']} ({r['agent_id']}, {r['duration_ms']} ms)")
        for c in r["checks"]:
            if not c["ok"]:
                lines.append(f"    · échec : {c['check']} — {c['detail'] or 'non vérifié'}")
        if r["error"]:
            lines.append(f"    · erreur : {r['error']}")
    return "\n".join(lines)
