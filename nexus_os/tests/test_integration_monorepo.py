"""Test d'intégration : NEXUS·OS monté dans l'application du monorepo."""
from __future__ import annotations

import pytest

from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def mono_client():
    from app.main import app as mono_app  # racine du dépôt, ajoutée au sys.path par pytest

    with TestClient(mono_app) as c:
        yield c


def test_os_monte_sous_le_monorepo(mono_client):
    r = mono_client.get("/os/")
    assert r.status_code == 200
    assert "NEXUS·OS" in r.text


def test_api_de_l_os_accessible_depuis_le_monorepo(mono_client):
    body = mono_client.get("/os/api/status").json()
    assert body["runtime"]["agents"] >= 10
    assert len(mono_client.get("/os/api/agents").json()) >= 10


def test_assets_de_l_os_sous_le_prefixe(mono_client):
    assert mono_client.get("/os/static/os.css").status_code == 200
    assert mono_client.get("/os/static/os.js").status_code == 200


def test_le_monorepo_garde_ses_routes(mono_client):
    assert mono_client.get("/health").json()["ok"] is True
    assert mono_client.get("/api/manifest").status_code == 200
    assert "NEXUS·OS (agents)" in mono_client.get("/").text
