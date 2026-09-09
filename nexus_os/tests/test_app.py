"""Tests de l'API HTTP (FastAPI TestClient) — pages, endpoints et flux SSE."""
from __future__ import annotations

import json

import pytest
from fastapi.testclient import TestClient

from nexus_os.app import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


def parse_sse(text: str) -> list[dict]:
    out = []
    for line in text.splitlines():
        if line.startswith("data: "):
            out.append(json.loads(line[6:]))
    return out


# -------------------------------------------------------------------------- #
def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["ok"] is True and body["agents"] >= 10 and body["skills"] == 14


def test_page_bureau_servie(client):
    r = client.get("/os/")
    assert r.status_code == 200
    assert "NEXUS·OS" in r.text and "static/os.js" in r.text


def test_racine_sert_le_bureau(client):
    r = client.get("/")
    assert r.status_code == 200 and "NEXUS·OS" in r.text


def test_assets_statiques(client):
    assert client.get("static/os.css").status_code == 200
    assert client.get("static/os.js").status_code == 200


def test_status_expose_le_mode(client):
    body = client.get("/api/status").json()
    assert body["mode_info"]["mode"] in {"live", "offline"}
    assert body["runtime"]["tools"] >= 14
    assert set(body["flags"]) >= {"shell", "network", "workspace"}


def test_catalogue_modeles_et_fournisseurs(client):
    providers = client.get("/api/providers").json()
    assert len(providers) >= 7
    assert {"id", "has_key", "budget", "quota_left"} <= set(providers[0])
    models = client.get("/api/models").json()
    assert len(models) >= 15
    assert any(m["free"] for m in models)


def test_liste_agents_et_detail(client):
    agents = client.get("/api/agents").json()
    assert len(agents) >= 10
    detail = client.get("/api/agents/coder")
    assert detail.status_code == 200
    assert "# 🛠️ Ingénieur" in detail.json()["markdown"]
    assert client.get("/api/agents/inexistant").status_code == 404


def test_competences_et_outils(client):
    skills = client.get("/api/skills").json()
    assert len(skills) == 14
    body = client.get("/api/skills/diagram-design").json()
    assert "Une vue = une question" in body["body"]
    tools = client.get("/api/tools").json()
    names = {t["name"] for t in tools}
    assert {"write_file", "grep", "diagram", "handoff", "create_agent"} <= names
    assert any(t["risky"] for t in tools)


def test_route_suggere_le_bon_specialiste(client):
    r = client.post("/api/route", json={"task": "rédige une landing page qui convertit"})
    assert r.status_code == 200
    body = r.json()
    assert body["suggested"]["agent_id"] == "writer"
    assert client.post("/api/route", json={"task": ""}).status_code == 400


# -------------------------------------------------------------------------- #
# Créateur via l'API
# -------------------------------------------------------------------------- #
def test_draft_puis_creation_puis_suppression(client):
    d = client.post("/api/agents/draft", json={
        "description": "un agent qui relit les contrats, cherche les clauses risquées "
                       "et produit un tableau html",
        "use_llm": False,
    })
    assert d.status_code == 200
    spec = d.json()["spec"]
    assert spec["tools"] and spec["skills"] and spec["system_prompt"]

    spec["id"] = "test-contrats"
    spec["name"] = "Test Contrats"
    created = client.post("/api/agents", json=spec)
    assert created.status_code == 200, created.text
    assert created.json()["agent"]["source"] == "user"
    assert any(a["id"] == "test-contrats" for a in client.get("/api/agents").json())

    assert client.delete("/api/agents/test-contrats").status_code == 200
    assert not any(a["id"] == "test-contrats" for a in client.get("/api/agents").json())


def test_creation_avec_outil_inconnu_refusee(client):
    r = client.post("/api/agents", json={"id": "x", "name": "X", "tools": ["outil_inexistant"]})
    assert r.status_code == 400 and "outil" in r.json()["detail"].lower()


def test_draft_sans_description_refuse(client):
    assert client.post("/api/agents/draft", json={"description": "  "}).status_code == 400


def test_suppression_agent_integre_refusee(client):
    assert client.delete("/api/agents/coder").status_code == 404


# -------------------------------------------------------------------------- #
# Exécution en SSE
# -------------------------------------------------------------------------- #
def test_run_stream_complet(client):
    with client.stream("GET", "/api/run",
                       params={"task": "résume la structure du dépôt en 3 points",
                               "agent": "coach"}) as r:
        assert r.status_code == 200
        assert r.headers["content-type"].startswith("text/event-stream")
        events = parse_sse("".join(r.iter_text()))
    tt = [e["type"] for e in events]
    assert tt[0] == "stream_open" and tt[-1] == "stream_close"
    for expected in ("run_start", "phase", "message", "run_end", "result"):
        assert expected in tt, f"événement manquant : {expected}"
    result = next(e for e in events if e["type"] == "result")
    assert result["result"].strip() and result["agent_id"] == "coach"


def test_run_agent_inconnu_404(client):
    assert client.get("/api/run", params={"task": "x", "agent": "nope"}).status_code == 404


def test_pipeline_stream(client):
    with client.stream("GET", "/api/pipeline",
                       params={"task": "décris puis illustre le système",
                               "agents_chain": "researcher,architect"}) as r:
        events = parse_sse("".join(r.iter_text()))
    result = next(e for e in events if e["type"] == "result")
    assert [x["agent_id"] for x in result["runs"]] == ["researcher", "architect"]
    assert client.get("/api/pipeline", params={"task": "x", "agents_chain": "zzz"}).status_code == 404


def test_journal_et_usage_apres_execution(client):
    runs = client.get("/api/runs").json()
    assert runs, "aucune exécution journalisée"
    assert {"id", "agent_id", "status", "tokens", "steps", "phases"} <= set(runs[0])
    usage = client.get("/api/usage").json()
    assert usage["stats"]["runs"] >= 1


# -------------------------------------------------------------------------- #
# Mémoire & espace de travail
# -------------------------------------------------------------------------- #
def test_memoire_crud(client):
    item = client.post("/api/memory", json={"content": "le build se lance avec uvicorn",
                                            "kind": "fact", "tags": "build"}).json()
    assert item["id"]
    assert client.post("/api/memory", json={"content": "  "}).status_code == 400
    got = client.get("/api/memory", params={"q": "build"}).json()
    assert any(i["id"] == item["id"] for i in got["items"])
    assert client.delete(f"/api/memory/{item['id']}").status_code == 200
    assert client.delete(f"/api/memory/{item['id']}").status_code == 404


def test_workspace_liste_et_traversal_bloque(client):
    assert client.get("/workspace").status_code == 200
    assert client.get("/workspace/../../etc/passwd").status_code in (400, 404)
