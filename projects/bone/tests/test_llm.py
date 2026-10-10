import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# isolation
for k in list(os.environ):
    if k in {"OPENAI_API_KEY", "GROQ_API_KEY", "OLLAMA_HOST", "BONE_LLM", "BONE_MODEL"}:
        os.environ.pop(k, None)

from llm import provider, describe, complete
from persona import think, reply


def test_no_key_is_papier():
    assert provider() is None
    assert "papier" in describe()


def test_think_falls_back_without_key():
    t = think("salut", channel_id="t-llm-fallback")
    assert t and len(t) > 5


def test_groq_provider():
    os.environ["GROQ_API_KEY"] = "gsk_fake"
    try:
        p = provider()
        assert p and p["id"] == "groq"
        assert "groq.com" in p["url"]
    finally:
        os.environ.pop("GROQ_API_KEY", None)


def test_complete_without_network_returns_none():
    os.environ["BONE_LLM"] = "off"
    try:
        assert complete([{"role": "user", "content": "hi"}]) is None
    finally:
        os.environ.pop("BONE_LLM", None)
