"""Couche modèle : un seul point d'entrée, plusieurs fournisseurs, dégradation propre.

Hiérarchie voulue — du plus sûr au plus riche :
  1. `none`    : aucun modèle. Toutes les fonctions de génération doivent alors
                 produire leur résultat par gabarit déterministe. C'est le mode
                 de secours : il fonctionne sans réseau, sans GPU, sans clé.
  2. `ollama`  : modèle local (Ollama). Gratuit, hors ligne, privé.
  3. `openai`  : toute API compatible OpenAI (OpenAI, Mistral, Groq, Ollama distant…).

Règle d'or : un appel qui échoue ne casse jamais la réunion. On retente court,
puis on rend la main avec `None` et l'appelant retombe sur le déterministe.
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.request

from . import log

_TIMEOUT_DEFAULT = 20


class ModelError(RuntimeError):
    pass


def _http_json(url: str, payload: dict, headers: dict | None = None, timeout: int = _TIMEOUT_DEFAULT):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    for k, v in (headers or {}).items():
        req.add_header(k, v)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
    try:
        return json.loads(raw)
    except Exception:
        return {"_raw": raw}


class LLM:
    def __init__(self, cfg: dict | None = None):
        self.cfg = cfg or {}
        llm_cfg = self.cfg.get("llm") or {}
        self.provider = llm_cfg.get("provider", "auto")
        self.ollama_url = (llm_cfg.get("ollama_url") or "http://127.0.0.1:11434").rstrip("/")
        self.ollama_model = llm_cfg.get("ollama_model") or "qwen2.5:7b-instruct"
        self.openai_url = (llm_cfg.get("openai_url") or "https://api.openai.com/v1").rstrip("/")
        self.openai_model = llm_cfg.get("openai_model") or "gpt-4o-mini"
        self.key_env = llm_cfg.get("openai_key_env") or "OPENAI_API_KEY"
        self.timeout = int(llm_cfg.get("timeout_s") or _TIMEOUT_DEFAULT)
        self._resolved: str | None = None

    # ---------- détection ----------
    def _ollama_up(self) -> bool:
        try:
            with urllib.request.urlopen(f"{self.ollama_url}/api/tags", timeout=2) as r:
                return r.status == 200
        except Exception:
            return False

    def _openai_key(self) -> str:
        return os.environ.get(self.key_env, "").strip()

    def resolve(self) -> str:
        """Fournisseur effectivement utilisé."""
        if self._resolved:
            return self._resolved
        p = self.provider
        if p == "none":
            self._resolved = "none"
        elif p == "ollama":
            self._resolved = "ollama" if self._ollama_up() else "none"
        elif p == "openai":
            self._resolved = "openai" if self._openai_key() else "none"
        else:  # auto
            if self._ollama_up():
                self._resolved = "ollama"
            elif self._openai_key():
                self._resolved = "openai"
            else:
                self._resolved = "none"
        return self._resolved

    def status(self) -> dict:
        p = self.resolve()
        return {
            "provider_demande": self.provider,
            "provider_actif": p,
            "ollama_url": self.ollama_url,
            "ollama_disponible": self._ollama_up(),
            "ollama_modele": self.ollama_model,
            "openai_modele": self.openai_model,
            "cle_presente": bool(self._openai_key()),
            "deterministe": p == "none",
        }

    # ---------- complétion ----------
    def complete(self, prompt: str, system: str = "", temperature: float = 0.2,
                 max_tokens: int = 1200) -> str | None:
        p = self.resolve()
        if p == "none":
            return None
        try:
            if p == "ollama":
                out = _http_json(
                    f"{self.ollama_url}/api/generate",
                    {"model": self.ollama_model, "prompt": f"{system}\n\n{prompt}".strip(),
                     "system": system, "stream": False,
                     "options": {"temperature": temperature, "num_predict": max_tokens}},
                    timeout=self.timeout,
                )
                return (out.get("response") or "").strip()
            out = _http_json(
                f"{self.openai_url}/chat/completions",
                {"model": self.openai_model, "temperature": temperature,
                 "max_tokens": max_tokens,
                 "messages": ([{"role": "system", "content": system}] if system else [])
                 + [{"role": "user", "content": prompt}]},
                {"Authorization": f"Bearer {self._openai_key()}"},
                timeout=self.timeout,
            )
            return (((out.get("choices") or [{}])[0]).get("message") or {}).get("content", "").strip()
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, OSError) as exc:
            log.warn("llm", f"appel impossible ({p}) : {exc}")
            return None
        except Exception as exc:
            log.error("llm", f"erreur inattendue : {exc}")
            return None

    # ---------- JSON tolérant ----------
    _FENCE = re.compile(r"```(?:json)?\s*(.*?)```", re.S)

    def json_complete(self, prompt: str, system: str = "", schema_hint: str = "",
                      temperature: float = 0.1) -> dict | None:
        """Demande un objet JSON ; tolère les balises markdown et le bruit autour."""
        guard = ("Réponds uniquement par un objet JSON valide, sans commentaire ni balise. "
                 + (f"Forme attendue : {schema_hint}" if schema_hint else ""))
        raw = self.complete(prompt, system=(system + "\n" + guard).strip(),
                            temperature=temperature)
        if not raw:
            return None
        return self._extract_json(raw)

    @classmethod
    def _extract_json(cls, raw: str) -> dict | None:
        text = raw.strip()
        m = cls._FENCE.search(text)
        if m:
            text = m.group(1).strip()
        if not text.startswith("{"):
            i, j = text.find("{"), text.rfind("}")
            if i >= 0 and j > i:
                text = text[i:j + 1]
        try:
            obj = json.loads(text)
        except Exception:
            return None
        return obj if isinstance(obj, dict) else None


_llm_singleton: LLM | None = None


def get(cfg: dict | None = None) -> LLM:
    global _llm_singleton
    if _llm_singleton is None or cfg is not None:
        _llm_singleton = LLM(cfg)
    return _llm_singleton


def reset():
    global _llm_singleton
    _llm_singleton = None
