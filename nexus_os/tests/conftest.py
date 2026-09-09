"""Conftest : isole NEXUS·OS dans un dossier temporaire avant tout import du paquet."""
from __future__ import annotations

import os
import tempfile

_TMP = tempfile.mkdtemp(prefix="nexus-test-")
os.environ["NEXUS_HOME"] = _TMP
os.environ["NEXUS_ALLOW_SHELL"] = "0"
os.environ["NEXUS_ALLOW_NETWORK"] = "0"
for key in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY", "GEMINI_API_KEY", "OPENROUTER_API_KEY",
            "GROQ_API_KEY", "MISTRAL_API_KEY"):
    os.environ.pop(key, None)

import pytest  # noqa: E402

from nexus_os import config  # noqa: E402


@pytest.fixture(autouse=True)
def isolated_workspace(tmp_path, monkeypatch):
    """Chaque test écrit dans sa propre sandbox."""
    ws = tmp_path / "workspace"
    ws.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(config, "WORKSPACE_DIR", ws)
    yield ws
