"""Vraie IA pour Bone — Ollama / Groq / OpenAI (compatible chat completions).

Sans clé : None, le cerveau papier (persona) prend le relais.
"""
from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

_FALLBACK_MODELS = {
    "ollama": "llama3.2",
    "groq": "llama-3.1-8b-instant",
    "openai": "gpt-4o-mini",
}


def _model(kind: str) -> str:
    return os.getenv("BONE_MODEL", "").strip() or _FALLBACK_MODELS[kind]


def _flag_off() -> bool:
    return os.getenv("BONE_LLM", "auto").strip().lower() in {"0", "off", "none", "no", "persona"}


def provider() -> dict[str, str] | None:
    """Quel backend utiliser, ou None = cerveau papier."""
    if _flag_off():
        return None
    mode = os.getenv("BONE_LLM", "auto").strip().lower() or "auto"

    groq = os.getenv("GROQ_API_KEY", "").strip()
    openai = os.getenv("OPENAI_API_KEY", "").strip()
    ollama = os.getenv("OLLAMA_HOST", "").strip().rstrip("/")

    def groq_p():
        return {"id": "groq", "url": "https://api.groq.com/openai/v1/chat/completions",
                "key": groq, "model": _model("groq")}

    def openai_p():
        return {"id": "openai", "url": "https://api.openai.com/v1/chat/completions",
                "key": openai, "model": _model("openai")}

    def ollama_p():
        host = ollama or "http://127.0.0.1:11434"
        return {"id": "ollama", "url": f"{host}/v1/chat/completions",
                "key": "ollama", "model": _model("ollama")}

    if mode == "groq":
        return groq_p() if groq else None
    if mode == "openai":
        return openai_p() if openai else None
    if mode == "ollama":
        return ollama_p()
    # auto : Groq (gratuit) → OpenAI → Ollama si host défini
    if groq:
        return groq_p()
    if openai:
        return openai_p()
    if ollama:
        return ollama_p()
    return None


def complete(messages: list[dict[str, str]], timeout: int = 25) -> str | None:
    p = provider()
    if not p:
        return None
    body: dict[str, Any] = {
        "model": p["model"],
        "messages": messages,
        "temperature": 0.85,
        "max_tokens": 280,
    }
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        p["url"],
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {p['key']}",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError, OSError):
        return None
    try:
        text = payload["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError):
        return None
    if not isinstance(text, str) or not text.strip():
        return None
    return text.strip()


def describe() -> str:
    p = provider()
    if not p:
        return "papier (pas de clé IA — répliques locales)"
    return f"{p['id']} · {p['model']}"
