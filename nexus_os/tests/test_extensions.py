"""Tests des trois ajouts : plugins, tâches asynchrones, barème d'évaluation."""
from __future__ import annotations

import json
import time

import pytest
from fastapi.testclient import TestClient

from nexus_os import config, evals, plugins, tasks
from nexus_os.agents import registry as agent_registry
from nexus_os.app import app
from nexus_os.skills import library as skill_library


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def sandbox(tmp_path, monkeypatch):
    """Plugins, tâches et barème dans un NEXUS_HOME jetable."""
    monkeypatch.setattr(plugins, "PLUGINS_DIR", tmp_path / "plugins")
    monkeypatch.setattr(plugins, "REGISTRY_FILE", tmp_path / "plugins.json")
    monkeypatch.setattr(tasks, "TASKS_FILE", tmp_path / "tasks.json")
    monkeypatch.setattr(evals, "EVALS_FILE", tmp_path / "evals.json")
    (tmp_path / "workspace").mkdir(parents=True, exist_ok=True)
    yield tmp_path


# -------------------------------------------------------------------------- #
# Plugins
# -------------------------------------------------------------------------- #
def test_installation_d_un_plugin_valide(sandbox):
    src = plugins.make_sample(sandbox / "src")
    data, problems = plugins.validate(src)
    assert problems == [] and data["name"] == "exemple"

    info = plugins.register(src)
    assert info.status == "ok" and info.version == "0.1.0"
    assert info.skills == ["skills/methode-exemple"]
    assert info.agents == ["agents/lecteur.json"]
    assert (plugins.PLUGINS_DIR / "exemple" / "plugin.json").exists()


def test_un_plugin_apporte_vraiment_des_competences_et_des_agents(sandbox):
    avant_skills = len(skill_library().all())
    avant_agents = len(agent_registry().all())

    plugins.register(plugins.make_sample(sandbox / "src"))
    skill_library().load(force=True)
    agent_registry().load(force=True)

    assert len(skill_library().all()) == avant_skills + 1
    assert skill_library().get("methode-exemple").source == "user"
    assert len(agent_registry().all()) == avant_agents + 1
    agent = agent_registry().require("lecteur")
    assert agent.source == "plugin" and "read_file" in agent.tools


def test_desactiver_un_plugin_redonne_l_os_d_avant(sandbox):
    """La recette de la compétence plugin-authoring, vérifiée."""
    plugins.register(plugins.make_sample(sandbox / "src"))
    skill_library().load(force=True)
    agent_registry().load(force=True)
    avec = len(skill_library().all()), len(agent_registry().all())

    plugins.set_enabled("exemple", False)
    skill_library().load(force=True)
    agent_registry().load(force=True)
    sans = len(skill_library().all()), len(agent_registry().all())

    assert avec[0] == sans[0] + 1 and avec[1] == sans[1] + 1
    assert plugins.describe("exemple").status == "inactif"
    assert "lecteur" not in {a.id for a in agent_registry().all()}


def test_manifeste_invalide_est_signale_pas_charge(sandbox):
    src = sandbox / "casse"
    (src / "skills" / "manquante").mkdir(parents=True)
    (src / "plugin.json").write_text(json.dumps({
        "name": "casse", "version": "0.1.0",
        "skills": ["skills/manquante"],           # SKILL.md absent
        "requires": ["outil_qui_n_existe_pas"],   # prérequis impossible
    }), encoding="utf-8")

    data, problems = plugins.validate(src)
    assert data.get("description", "") == "" and any("description" in p for p in problems)
    assert any("SKILL.md" in p for p in problems)
    assert any("inexistants" in p for p in problems)
    with pytest.raises(plugins.PluginError):
        plugins.register(src)
    assert plugins.discover() == []


def test_manifeste_absent(sandbox):
    src = sandbox / "vide"
    src.mkdir()
    with pytest.raises(plugins.PluginError, match="plugin.json absent"):
        plugins.register(src)


def test_json_invalide(sandbox):
    src = sandbox / "pourri"
    src.mkdir()
    (src / "plugin.json").write_text("{ pas du json", encoding="utf-8")
    _, problems = plugins.validate(src)
    assert any("illisible" in p for p in problems)


def test_desinstallation_supprime_les_fichiers(sandbox):
    plugins.register(plugins.make_sample(sandbox / "src"))
    assert (plugins.PLUGINS_DIR / "exemple").exists()
    assert plugins.unregister("exemple", delete_files=True) is True
    assert not (plugins.PLUGINS_DIR / "exemple").exists()
    assert plugins.unregister("exemple") is False


def test_api_plugins(client, sandbox):
    src = plugins.make_sample(sandbox / "src")
    r = client.post("/api/plugins", json={"path": str(src)})
    assert r.status_code == 200
    assert r.json()["plugin"]["name"] == "exemple"
    assert "lecteur" in {a["id"] for a in client.get("/api/agents").json()}

    assert client.post("/api/plugins/exemple/toggle", json={"enabled": False}).status_code == 200
    assert "lecteur" not in {a["id"] for a in client.get("/api/agents").json()}

    assert client.delete("/api/plugins/exemple?delete_files=true").status_code == 200
    assert client.get("/api/plugins").json()["count"] == 0
    assert client.post("/api/plugins", json={"path": "/nulle/part"}).status_code == 400
    assert client.delete("/api/plugins/inconnu").status_code == 404


def test_api_plugin_sample(client):
    r = client.post("/api/plugins/sample")
    assert r.status_code == 200
    assert r.json()["manifest"]["name"] == "exemple"


# -------------------------------------------------------------------------- #
# Tâches asynchrones
# -------------------------------------------------------------------------- #
def test_submit_retourne_avant_la_fin_puis_se_laisse_relire(sandbox):
    task_id = tasks.submit("audite la structure du dépôt", "orchestrator", approval="off")
    assert isinstance(task_id, str) and len(task_id) == 12
    rec = tasks.wait(task_id, timeout=60)
    assert rec["state"] == "completed"
    assert rec["result"] and rec["duration_ms"] >= 0
    assert rec["progress"]["events"] > 0


def test_etats_conformes_a_la_specification(sandbox):
    assert tasks.STATES == ("working", "input_required", "completed", "failed", "cancelled")


def test_une_autorisation_demandee_place_la_tache_en_input_required(sandbox):
    task_id = tasks.submit("relis cette clause", "jurist", approval="manuel")
    rec = tasks.wait(task_id, timeout=60)
    assert rec["state"] == "input_required"
    assert rec["progress"]["pending_tools"], "aucun outil signalé comme bloquant"
    # Autoriser relance avec les outils permis, sous un nouvel identifiant.
    new_id = tasks.approve(task_id)
    assert new_id != task_id
    suite = tasks.wait(new_id, timeout=60)
    assert suite["state"] == "completed"
    assert tasks.get(task_id)["state"] == "cancelled"


def test_annulation(sandbox):
    task_id = tasks.submit("audite longuement le dépôt et détaille tout", "orchestrator",
                           approval="off")
    time.sleep(0.05)
    if tasks.get(task_id)["state"] == "working":
        assert tasks.cancel(task_id) is True
        assert tasks.wait(task_id, timeout=30)["state"] == "cancelled"
    with pytest.raises(tasks.TaskError):
        tasks.cancel(task_id)          # déjà terminale


def test_tache_inconnue(sandbox):
    with pytest.raises(tasks.TaskError):
        tasks.get("inexistante")
    with pytest.raises(KeyError):
        tasks.submit("x", "agent_qui_n_existe_pas")
    with pytest.raises(ValueError):
        tasks.submit("   ", "writer")


def test_persistees_et_incrementales(sandbox):
    task_id = tasks.submit("rédige une accroche", "writer", approval="off")
    tasks.wait(task_id, timeout=60)
    stored = json.loads(tasks.TASKS_FILE.read_text(encoding="utf-8"))
    assert task_id in stored and stored[task_id]["state"] == "completed"

    evs = tasks.events(task_id, since=0, limit=3)
    assert len(evs["events"]) == 3 and evs["next"] == 3
    suite = tasks.events(task_id, since=evs["next"], limit=100)
    assert suite["next"] > evs["next"]
    assert suite["total"] == evs["total"]


def test_api_tasks(client, sandbox):
    r = client.post("/api/tasks", json={"task": "rédige une accroche", "agent_id": "writer",
                                        "approval": "off"})
    assert r.status_code == 200
    task_id = r.json()["id"]
    for _ in range(120):
        if client.get(f"/api/tasks/{task_id}").json()["state"] != "working":
            break
        time.sleep(0.1)
    assert client.get(f"/api/tasks/{task_id}").json()["state"] == "completed"
    assert client.get(f"/api/tasks/{task_id}/events?since=0").json()["total"] > 0
    assert client.get("/api/tasks").json()["summary"]["count"] >= 1
    assert client.get("/api/tasks/inconnue").status_code == 404
    assert client.post("/api/tasks", json={"task": "x", "agent_id": "zzz"}).status_code == 404


# -------------------------------------------------------------------------- #
# Barème
# -------------------------------------------------------------------------- #
def test_le_bareme_couvre_des_capacites_reelles():
    suite = evals.suite()
    assert len(suite) == 10
    assert {c["agent_id"] for c in suite} >= {"coder", "architect", "orchestrator", "analyst"}
    for c in suite:
        assert c["task"].strip() and c["id"]


def test_un_cas_isole_passe(sandbox):
    case = next(c for c in evals.SUITE if c.id == "architecte-dessine")
    res = evals.run_case(case)
    assert res.passed, res.to_dict()
    assert any(c["check"] == "artéfact" for c in res.checks)


def test_un_cas_impossible_echoue_proprement(sandbox):
    """Un barème qui ne peut pas échouer ne mesure rien."""
    # Le rédacteur produit un livrable : exiger l'inverse doit échouer.
    case = evals.Case("piège", "writer", "rédige une accroche",
                      produces_artifact=False, mentions=("chaîne introuvable xyz",))
    res = evals.run_case(case)
    assert res.passed is False
    assert any(not c["ok"] and c["check"] == "artéfact" for c in res.checks)
    assert any(not c["ok"] and "introuvable" in c["check"] for c in res.checks)


def test_bareme_complet_et_persiste(sandbox):
    sc = evals.run_suite()
    assert sc["cases"] == 10 and sc["score"] == 1.0, evals.render(sc)
    assert sc["failed"] == 0
    saved = evals.last()
    assert saved and saved["passed"] == 10
    assert "Barème" in evals.render(sc)


def test_bareme_restreint_a_un_agent(sandbox):
    sc = evals.run_suite("qa")
    assert sc["cases"] == 1 and sc["passed"] == 1
    with pytest.raises(KeyError):
        evals.run_suite("agent_inexistant")


def test_api_evals(client, sandbox):
    body = client.get("/api/evals").json()
    assert len(body["suite"]) == 10 and body["last"] is None
    sc = client.post("/api/evals", json={"agent_id": "writer"}).json()
    assert sc["cases"] == 1 and sc["passed"] == 1
    assert client.post("/api/evals", json={"agent_id": "zzz"}).status_code == 404
