"""Tests des options ajoutées : harness, approbation, flotte, nouveaux outils, kanban."""
from __future__ import annotations

import re

import pytest
from fastapi.testclient import TestClient

from nexus_os.agents import registry
from nexus_os.app import app
from nexus_os.harness import TARGETS, export_all, export_spec, filename_for, summarize
from nexus_os.runtime import APPROVAL_MODES, Runtime
from nexus_os.tools import ToolContext, ToolError, ToolRegistry


def collect(gen):
    events = []
    try:
        while True:
            events.append(next(gen))
    except StopIteration as stop:
        return events, stop.value


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


# -------------------------------------------------------------------------- #
# Portabilité multi-harness
# -------------------------------------------------------------------------- #
def test_12_harness_cibles():
    assert len(TARGETS) == 12
    assert {"claude-code", "codex", "opencode", "cline", "cursor", "goose", "gemini",
            "qwen", "hermes", "agentskills", "a2a", "nexus"} == set(TARGETS)


def test_export_pour_chaque_harness():
    spec = registry().require("coder")
    for target in TARGETS:
        content = export_spec(spec, target)
        assert content.strip(), f"export vide pour {target}"
        assert "coder" in content, f"{target} : l'agent n'est pas identifiable"
        assert filename_for(target, spec), target


def test_export_claude_code_a_un_frontmatter_valide():
    out = export_spec(registry().require("writer"), "claude-code")
    assert out.startswith("---\nname: writer\n")
    head = out.split("---")[1]
    assert "description:" in head and "tools:" in head and "model:" in head


def test_export_hermes_et_agentskills_sont_des_skill_md():
    spec = registry().require("researcher")
    for target in ("hermes", "agentskills"):
        out = export_spec(spec, target)
        assert out.startswith("---\nname: researcher\n")
        assert "triggers:" in out and "tags:" in out
        assert filename_for(target, spec) == "skills/researcher/SKILL.md"


def test_export_nexus_est_reimportable():
    import json

    from nexus_os.agents import AgentSpec

    spec = registry().require("analyst")
    data = json.loads(export_spec(spec, "nexus"))
    rebuilt = AgentSpec.from_dict(data)
    assert rebuilt.id == spec.id and rebuilt.skills == spec.skills
    assert rebuilt.tools == spec.tools and rebuilt.lifecycle == spec.lifecycle


def test_harness_inconnu_refuse():
    with pytest.raises(KeyError):
        export_spec(registry().require("coder"), "harness-qui-n-existe-pas")


def test_summarize_indique_les_pertes():
    s = summarize(registry().require("coder"))
    assert s["agent_id"] == "coder" and len(s["targets"]) == 12
    nexus = next(t for t in s["targets"] if t["id"] == "nexus")
    assert nexus["loses"] == ["rien — export sans perte"]
    codex = next(t for t in s["targets"] if t["id"] == "codex")
    assert any("outils" in x for x in codex["loses"])


def test_export_all_couvre_tout():
    out = export_all(registry().require("pm"))
    assert set(out) == set(TARGETS)
    assert all(v["content"] and v["filename"] for v in out.values())


def test_api_harness(client):
    assert len(client.get("/api/harnesses").json()) == 12
    r = client.get("/api/agents/coder/harness/claude-code")
    assert r.status_code == 200
    body = r.json()
    assert body["filename"] == ".claude/agents/coder.md" and body["bytes"] > 100
    saved = client.get("/api/agents/coder/harness/hermes?save=true").json()
    assert saved["saved_to"].endswith("skills/coder/SKILL.md")
    assert client.get("/api/agents/coder/harness/nope").status_code == 400
    assert client.get("/api/agents/inexistant/harness/codex").status_code == 404


# -------------------------------------------------------------------------- #
# Modes d'approbation
# -------------------------------------------------------------------------- #
def test_modes_disponibles():
    assert APPROVAL_MODES == ("off", "manuel", "smart")


def test_smart_bloque_les_outils_sensibles(isolated_workspace):
    rt = Runtime()
    ctx = ToolContext()
    res = rt._run_impl("lance une commande shell", "coder", session_id=None, max_steps=None,
                       depth=0, context="", emit=lambda e: None, approval="smart")
    assert res.pending_approvals, "un outil sensible aurait dû attendre une autorisation"
    assert res.confidence == "à vérifier"


def test_off_autorise_mais_le_shell_reste_desactive_par_config(isolated_workspace):
    rt = Runtime()
    seen = []
    from nexus_os.runtime import RunResult

    out = rt._exec_tool("shell", {"command": "echo x"}, "coder", seen.append,
                        RunResult(run_id="r", agent_id="coder"), approval="off")
    assert "NEXUS_ALLOW_SHELL" in out  # refusé par la config, pas par l'approbation
    assert not any(e["type"] == "approval_required" for e in seen)


def test_outil_pre_autorise_passe_le_controle(isolated_workspace, monkeypatch):
    from nexus_os import config
    from nexus_os.runtime import RunResult

    monkeypatch.setattr(config, "ALLOW_SHELL", True)
    rt = Runtime()
    res = RunResult(run_id="r", agent_id="coder")
    out = rt._exec_tool("shell", {"command": "echo autorisé"}, "coder", lambda e: None, res,
                        approval="smart", approved={"shell"})
    assert "autorisé" in out and not res.pending_approvals


def test_mode_manuel_exige_tout_valider(isolated_workspace):
    from nexus_os.runtime import RunResult

    rt = Runtime()
    res = RunResult(run_id="r", agent_id="writer")
    out = rt._exec_tool("write_file", {"path": "a.md", "content": "x"}, "writer",
                        lambda e: None, res, approval="manuel")
    assert "autorisation" in out and res.pending_approvals == ["write_file"]


def test_run_porte_le_mode_et_la_confiance(isolated_workspace):
    rt = Runtime()
    events, res = collect(rt.run("rédige une accroche", "writer", approval="manuel"))
    assert res.approval == "manuel"
    assert any(e["type"] == "approval_required" for e in events)
    assert res.confidence == "à vérifier"
    assert any(e.get("confidence") for e in events if e["type"] == "message")


# -------------------------------------------------------------------------- #
# Flotte parallèle
# -------------------------------------------------------------------------- #
def test_run_parallel_fait_tourner_plusieurs_agents(isolated_workspace):
    rt = Runtime()
    events, results = collect(rt.stream_parallel("décris le routeur", ["researcher", "writer"]))
    assert [r.agent_id for r in results] == ["researcher", "writer"]
    assert all(r.result for r in results)
    tagged = {e.get("agent_id") for e in events if e.get("agent_id")}
    assert {"researcher", "writer"} <= tagged, "les événements ne sont pas étiquetés par agent"


def test_parallel_exige_au_moins_deux_agents():
    rt = Runtime()
    with pytest.raises(ValueError):
        rt.run_parallel("x", ["writer"])
    with pytest.raises(KeyError):
        rt.run_parallel("x", ["writer", "inexistant"])


def test_api_parallel(client):
    assert client.get("/api/parallel",
                      params={"task": "x", "agents_list": "writer"}).status_code == 400
    assert client.get("/api/parallel",
                      params={"task": "x", "agents_list": "writer,zzz"}).status_code == 404


# -------------------------------------------------------------------------- #
# Nouveaux outils
# -------------------------------------------------------------------------- #
def test_outils_supplementaires_enregistres():
    names = set(ToolRegistry().names())
    assert {"diff_files", "render_chart", "task_board", "export_harness",
            "create_skill", "mcp_servers", "context_report", "learn_instinct"} <= names
    assert len(names) == 22


def test_diff_files(isolated_workspace):
    from nexus_os import config

    reg = ToolRegistry()
    a = config.READ_ROOT / "nexus_os" / "__init__.py"
    b = config.READ_ROOT / "nexus_os" / "config.py"
    out = reg.execute("diff_files", {"path_a": str(a), "path_b": str(b)}, ToolContext())
    assert "lignes" in out and ("+" in out or "-" in out)
    same = reg.execute("diff_files", {"path_a": str(a), "path_b": str(a)}, ToolContext())
    assert "aucune différence" in same


def test_render_chart_bar_et_line(isolated_workspace):
    reg = ToolRegistry()
    out = reg.execute("render_chart", {"title": "Tokens par jour", "kind": "bar",
                                       "labels": "lun, mar, mer", "values": "120, 340, 90"},
                      ToolContext())
    assert "tokens-par-jour.svg" in out
    svg = (isolated_workspace / "charts" / "tokens-par-jour.svg").read_text()
    assert svg.startswith("<svg") and "<rect" in svg and "340" in svg
    line = reg.execute("render_chart", {"title": "Courbe", "kind": "line",
                                        "labels": "a, b, c", "values": "1, 5, 3"}, ToolContext())
    assert "courbe.svg" in line
    assert "<polyline" in (isolated_workspace / "charts" / "courbe.svg").read_text()


def test_render_chart_refuse_les_donnees_incoherentes(isolated_workspace):
    reg = ToolRegistry()
    with pytest.raises(ToolError):
        reg.execute("render_chart", {"title": "x", "labels": "a, b", "values": "1"}, ToolContext())
    with pytest.raises(ToolError):
        reg.execute("render_chart", {"title": "x", "labels": "a", "values": "abc"}, ToolContext())


def test_create_skill_ecrit_un_skill_decouvrable(isolated_workspace, tmp_path, monkeypatch):
    from nexus_os import config
    from nexus_os.skills import SkillLibrary

    user = tmp_path / "skills"
    monkeypatch.setattr(config, "USER_SKILLS_DIR", user)
    reg = ToolRegistry()
    out = reg.execute("create_skill", {
        "name": "Recette Deploy",
        "description": "Déployer sans casse sur ce dépôt",
        "triggers": "déploie, mise en prod",
        "body": "1. Lancer les tests.\n2. Vérifier la migration.\n3. Déployer puis sonder.",
    }, ToolContext())
    assert "recette-deploy" in out
    lib = SkillLibrary([user])
    got = lib.get("recette-deploy")
    assert got and got.source == "user"
    assert got.triggers == ["déploie", "mise en prod"]
    assert "Lancer les tests" in got.body


def test_create_skill_refuse_un_corps_trop_court(isolated_workspace):
    reg = ToolRegistry()
    with pytest.raises(ToolError):
        reg.execute("create_skill", {"name": "vide", "body": "trop court"}, ToolContext())


def test_export_harness_depuis_l_outil(isolated_workspace):
    reg = ToolRegistry()
    out = reg.execute("export_harness", {"agent_id": "jurist", "target": "cline"}, ToolContext())
    assert "harness/cline/.clinerules" in out
    assert (isolated_workspace / "harness" / "cline" / ".clinerules").exists()
    with pytest.raises(ToolError):
        reg.execute("export_harness", {"agent_id": "jurist", "target": "nope"}, ToolContext())


# -------------------------------------------------------------------------- #
# Kanban
# -------------------------------------------------------------------------- #
def test_task_board_cycle_complet(isolated_workspace):
    reg = ToolRegistry()
    ctx = ToolContext()
    assert "vide" in reg.execute("task_board", {"action": "list"}, ctx)
    added = reg.execute("task_board", {"action": "add", "title": "Relire le contrat",
                                       "agent": "jurist"}, ctx)
    assert "à faire" in added
    tid = re.search(r"\]\s+(\S+)", added).group(1)
    assert "en cours" in reg.execute("task_board", {"action": "move", "column": "en cours",
                                                    "task_id": tid}, ctx)
    assert "terminé" in reg.execute("task_board", {"action": "done", "task_id": tid}, ctx)
    listing = reg.execute("task_board", {"action": "list"}, ctx)
    assert "Relire le contrat" in listing and "## terminé (1)" in listing
    assert "supprimée" in reg.execute("task_board", {"action": "remove", "task_id": tid}, ctx)


def test_task_board_colonne_invalide(isolated_workspace):
    with pytest.raises(ToolError):
        ToolRegistry().execute("task_board", {"action": "move", "column": "nulle part",
                                              "task_id": "x"}, ToolContext())


def test_api_board(client):
    r = client.post("/api/board", json={"action": "add", "title": "Tâche API",
                                        "agent": "pm", "column": "à faire"})
    assert r.status_code == 200
    board = client.get("/api/board").json()
    assert board["count"] >= 1 and len(board["columns"]) == 4
    item = next(i for i in board["items"] if i["title"] == "Tâche API")
    assert client.post("/api/board", json={"action": "done",
                                           "task_id": item["id"]}).status_code == 200
    assert client.post("/api/board", json={"action": "add", "title": "x",
                                           "column": "invalide"}).status_code == 400
    client.post("/api/board", json={"action": "remove", "task_id": item["id"]})


# -------------------------------------------------------------------------- #
# Options de l'API d'exécution
# -------------------------------------------------------------------------- #
def test_run_accepte_les_parametres_d_option(client):
    with client.stream("GET", "/api/run",
                       params={"task": "relis une clause", "agent": "jurist",
                               "approval": "manuel"}) as r:
        assert r.status_code == 200
        text = "".join(r.iter_text())
    assert "approval_required" in text


def test_run_refuse_un_mode_invalide(client):
    assert client.get("/api/run", params={"task": "x", "agent": "writer",
                                          "approval": "nimporte"}).status_code == 422


def test_22_agents_tous_coherents():
    """Chaque agent déclare des outils et des compétences qui existent vraiment."""
    from nexus_os.skills import library

    tools = set(ToolRegistry().names())
    skills = {s.name for s in library().all()}
    for a in registry().all():
        assert set(a.tools) <= tools, f"{a.id} : outils inconnus {set(a.tools) - tools}"
        assert set(a.skills) <= skills, f"{a.id} : compétences inconnues {set(a.skills) - skills}"
        assert a.tools, f"{a.id} n'a aucun outil"
        assert a.triggers, f"{a.id} n'a aucun déclencheur de routage"
        assert len(a.system_prompt) > 200, f"{a.id} : prompt système trop court"


# -------------------------------------------------------------------------- #
# Nommage du créateur (l'identifiant sert de nom de fichier dans les harness)
# -------------------------------------------------------------------------- #
@pytest.mark.parametrize("phrase,ident_attendu", [
    ("Un agent qui relit les fiches de paie et signale les anomalies légales",
     "relit-fiches-paie-signale"),
    ("je veux un assistant pour rédiger des posts LinkedIn percutants",
     "rediger-posts-linkedin-percutant"),
    ("Crée un agent capable de cartographier les risques d'un territoire",
     "cartographier-risques-d-un-terri"),
    ("outil qui traduit du français vers l'espagnol juridique",
     "traduit-francais-vers-l-espagnol"),
])
def test_le_createur_ne_garde_pas_la_formule_dans_le_nom(phrase, ident_attendu):
    from nexus_os.creator import draft

    r = draft(phrase, use_llm=False)
    assert r.spec.id == ident_attendu
    assert "agent" not in r.spec.id and "qui" not in r.spec.id
    assert "Un Agent Qui" not in r.spec.name
    assert r.spec.role and len(r.spec.role) <= 60
    assert not r.spec.role.endswith((" et", " de", " l", " vers"))


def test_slug_ascii_sans_perte_d_accent():
    from nexus_os.creator import slugify

    assert slugify("Rédacteur Français — Café") == "redacteur-francais-cafe"
    assert slugify("Élodie Ünlü") == "elodie-unlu"
    assert slugify("!!!") == "agent"
    assert len(slugify("x" * 200)) == 32


def test_la_consolidation_porte_une_confiance(isolated_workspace):
    rt = Runtime()
    events, res = collect(rt.run("audite ce fichier", "orchestrator"))
    finals = [e for e in events if e["type"] == "message" and e.get("final") and not e.get("depth")]
    assert finals, "aucune réponse finale de niveau 0"
    assert finals[-1]["confidence"] in {"confiant", "à vérifier"}
