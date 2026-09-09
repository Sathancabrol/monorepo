"""Tests du runtime : la boucle d'exécution, les outils réels, l'orchestration."""
from __future__ import annotations

import pytest

from nexus_os.agents import AgentSpec, registry
from nexus_os.db import store
from nexus_os.runtime import OfflinePlanner, Runtime, RunResult
from nexus_os.tools import ToolRegistry


def collect(gen):
    """Consomme un générateur d'événements et renvoie (événements, valeur de retour)."""
    events = []
    try:
        while True:
            events.append(next(gen))
    except StopIteration as stop:
        return events, stop.value


def types(events):
    return [e["type"] for e in events]


# -------------------------------------------------------------------------- #
# Planificateur hors-ligne
# -------------------------------------------------------------------------- #
def test_planner_phase_par_phase(monkeypatch):
    from nexus_os import config

    monkeypatch.setattr(config, "ALLOW_NETWORK", True)
    p = OfflinePlanner()
    agent = AgentSpec(id="a", name="A",
                      tools=["web_search", "grep", "write_file", "read_file",
                             "python_exec", "memory_remember"])
    task = "audite la sécurité du routeur de modèles"
    assert p.plan_for("plan", task, agent, [])[0] is None
    assert p.plan_for("research", task, agent, [])[0] == "web_search"
    assert p.plan_for("implement", task, agent, ["x"])[0] == "write_file"
    assert p.plan_for("verify", task, agent, [])[0] == "python_exec"
    assert p.plan_for("remember", task, agent, ["x"])[0] == "memory_remember"


def test_planner_sans_reseau_tombe_sur_grep(monkeypatch):
    from nexus_os import config

    monkeypatch.setattr(config, "ALLOW_NETWORK", False)
    p = OfflinePlanner()
    agent = AgentSpec(id="a", name="A", tools=["web_search", "grep"])
    name, args = p.plan_for("research", "vérifie le parseur", agent, [])
    assert name == "grep" and args["pattern"]


def test_planner_choisit_diagram_pour_un_architecte():
    p = OfflinePlanner()
    agent = registry().require("architect")
    name, _ = p.plan_for("implement", "cartographie les flux de données", agent, ["a"])
    assert name == "diagram"


# -------------------------------------------------------------------------- #
# Boucle d'exécution
# -------------------------------------------------------------------------- #
def test_run_execute_des_outils_reels(isolated_workspace):
    rt = Runtime()
    events, res = collect(rt.run("écris une note sur la structure du dépôt", "coder"))
    assert isinstance(res, RunResult)
    assert res.status == "done" and res.result
    tt = types(events)
    assert "run_start" in tt and "phase" in tt and "message" in tt and "run_end" in tt
    called = [e["name"] for e in events if e["type"] == "tool_call"]
    assert called, "aucun outil exécuté"
    assert any(e["type"] == "tool_result" and e["ok"] for e in events), "aucun outil réussi"
    assert res.steps > 0 and res.tokens > 0
    assert res.models and res.modes


def test_livrable_ecrit_dans_la_sandbox(isolated_workspace):
    rt = Runtime()
    events, res = collect(rt.run("produis un rapport sur les compétences", "coder"))
    assert res.artifacts, "aucun artefact produit"
    for art in res.artifacts:
        rel = art.split("workspace/", 1)[1]
        assert (isolated_workspace / rel).exists(), f"artefact annoncé absent : {art}"


def test_architect_produit_un_diagram_reel(isolated_workspace):
    rt = Runtime()
    _, res = collect(rt.run("dessine le diagramme des composants du routeur", "architect"))
    mmd = list(isolated_workspace.rglob("*.mmd"))
    assert mmd, "aucun fichier .mmd produit"
    assert "-->" in mmd[0].read_text()


def test_run_enregistre_en_base(isolated_workspace):
    rt = Runtime()
    _, res = collect(rt.run("tâche de test journalisée", "coach"))
    runs = store().list_runs(limit=5)
    assert any(r["id"] == res.run_id for r in runs)
    saved = next(r for r in runs if r["id"] == res.run_id)
    assert saved["agent_id"] == "coach" and saved["status"] == "done"
    assert saved["phases"], "phases non journalisées"


def test_session_et_messages_persistes(isolated_workspace):
    rt = Runtime()
    sid = store().create_session("coach", "test")["id"]
    collect(rt.run("par où commencer sur ce projet ?", "coach", session_id=sid))
    msgs = store().messages(sid)
    roles = {m["role"] for m in msgs}
    assert roles == {"user", "assistant"}


# -------------------------------------------------------------------------- #
# Orchestration
# -------------------------------------------------------------------------- #
def test_route_classe_les_agents():
    rt = Runtime()
    ranking = rt.route("rédige un email de lancement", limit=4)
    assert ranking and ranking[0]["score"] >= ranking[-1]["score"]
    assert ranking[0]["agent_id"] in {"writer", "orchestrator"}


def test_orchestrateur_delegue_au_specialiste(isolated_workspace):
    rt = Runtime()
    events, res = collect(rt.run("rédige une landing page qui convertit pour un outil de dev",
                                 "orchestrator"))
    assert any(e["type"] == "routing" for e in events), "pas d'événement de routage"
    assert any(e["type"] == "handoff" for e in events), "pas de délégation"
    delegate = next(e for e in events if e["type"] == "handoff")
    assert delegate["to"] == "writer"


def test_profondeur_de_delegation_bornee(isolated_workspace):
    rt = Runtime()
    events = []
    res = rt._run_impl("rédige un slogan puis délègue encore", "orchestrator", session_id=None,
                       max_steps=None, depth=1, context="", emit=events.append)
    # au niveau 1 l'orchestrateur ne re-route pas : pas de second niveau de délégation
    assert not any(e["type"] == "routing" for e in events)
    seen = []
    out = rt._delegate("coder", "sous-tâche", seen.append, 2, res)
    assert "profondeur" in out
    assert not any(e["type"] == "handoff" for e in seen)


def test_pipeline_enchaine_les_agents(isolated_workspace):
    rt = Runtime()
    events, results = collect(rt.stream_pipeline("décris puis illustre le routeur",
                                                 ["researcher", "architect"]))
    assert isinstance(results, list) and len(results) == 2
    assert [r.agent_id for r in results] == ["researcher", "architect"]
    assert any(e["type"] == "pipeline_step" for e in events)
    assert all(r.result for r in results)


def test_pipeline_agent_inconnu_refuse():
    rt = Runtime()
    with pytest.raises(KeyError):
        rt.run_pipeline("x", ["agent-qui-n-existe-pas"])
    with pytest.raises(ValueError):
        rt.run_pipeline("x", [])


# -------------------------------------------------------------------------- #
# Outil méta : auto-construction
# -------------------------------------------------------------------------- #
def test_create_agent_depuis_le_runtime(isolated_workspace, tmp_path, monkeypatch):
    from nexus_os import config

    user_dir = tmp_path / "agents"
    monkeypatch.setattr(config, "USER_AGENTS_DIR", user_dir)
    reg = registry()
    reg.user_dir = user_dir
    reg.load(force=True)

    rt = Runtime(agents=reg)
    out = rt._create_agent(
        {"description": "un agent qui relit les contrats et extrait les clauses risquées"},
        lambda e: None,
    )
    assert out.startswith("agent créé")
    files = list(user_dir.glob("*.json"))
    assert len(files) == 1
    spec = reg.load(force=True)[files[0].stem]
    assert spec.source == "user" and spec.system_prompt


def test_statut_du_runtime(isolated_workspace):
    st = Runtime().status()
    assert st["agents"] >= 10 and st["skills"] == 14 and st["tools"] >= 14
    assert st["mode"] in {"live", "offline"}


def test_outils_meta_refuses_dans_le_registre(isolated_workspace):
    rt = Runtime()
    seen = []
    out = rt._exec_tool("handoff", {"agent_id": "coder", "task": "x"}, "coder",
                        seen.append, RunResult(run_id="r", agent_id="coder"))
    assert "outil méta" in out
    results = [e for e in seen if e["type"] == "tool_result"]
    assert results and results[0]["ok"] is False
