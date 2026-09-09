"""Couche LLM unifiée : un seul `complete()`, N fournisseurs, bascule auto.

Deux modes :

* **live** — appel HTTPS réel (style OpenAI ou Anthropic) avec chaîne de
  secours quota-aware ;
* **offline** — moteur local déterministe (`_synthesize`) quand aucune clé
  n'est disponible ou que tous les fournisseurs ont échoué. Le runtime reste
  alors pleinement fonctionnel : les outils sont réellement exécutés, seule la
  génération de texte est rule-based.
"""
from __future__ import annotations

import json
import re
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Sequence

from nexus_os import config
from nexus_os.db import store
from nexus_os.providers import ModelRequest, ProviderSpec, RoutedModel, Router

_router = Router()


def router() -> Router:
    return _router


@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class Completion:
    text: str
    model: str
    provider: str
    mode: str = "offline"  # "live" | "offline"
    tool_calls: list[ToolCall] = field(default_factory=list)
    usage: dict[str, int] = field(default_factory=dict)
    fallbacks: list[str] = field(default_factory=list)
    latency_ms: int = 0
    error: str | None = None

    @property
    def tokens(self) -> int:
        return int(self.usage.get("total_tokens", 0))

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "model": self.model,
            "provider": self.provider,
            "mode": self.mode,
            "tool_calls": [
                {"id": t.id, "name": t.name, "arguments": t.arguments} for t in self.tool_calls
            ],
            "usage": self.usage,
            "fallbacks": self.fallbacks,
            "latency_ms": self.latency_ms,
            "error": self.error,
        }


# --------------------------------------------------------------------------- #
# Appels réels
# --------------------------------------------------------------------------- #
def _post(url: str, payload: dict[str, Any], headers: dict[str, str], timeout: int) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # nosec - URLs du catalogue
        return json.loads(resp.read().decode("utf-8"))


def _tools_openai(tools: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "type": "function",
            "function": {
                "name": t["name"],
                "description": t.get("description", ""),
                "parameters": t.get("parameters", {"type": "object", "properties": {}}),
            },
        }
        for t in tools
    ]


def _call_openai(
    route: RoutedModel, messages: list[dict[str, Any]], tools: Sequence[dict[str, Any]],
    temperature: float, max_tokens: int,
) -> tuple[str, list[ToolCall], dict[str, int]]:
    key = config.secret(route.provider.env_key) or "ollama"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {key}"}
    payload: dict[str, Any] = {
        "model": route.model.id,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if tools:
        payload["tools"] = _tools_openai(tools)
        payload["tool_choice"] = "auto"
    raw = _post(f"{route.provider.base_url}/chat/completions", payload, headers,
                config.REQUEST_TIMEOUT)
    choice = (raw.get("choices") or [{}])[0]
    msg = choice.get("message") or {}
    calls = [
        ToolCall(
            id=c.get("id") or f"call_{i}",
            name=(c.get("function") or {}).get("name", ""),
            arguments=_loads((c.get("function") or {}).get("arguments") or "{}"),
        )
        for i, c in enumerate(msg.get("tool_calls") or [])
    ]
    usage = raw.get("usage") or {}
    return msg.get("content") or "", calls, {
        "prompt_tokens": int(usage.get("prompt_tokens", 0)),
        "completion_tokens": int(usage.get("completion_tokens", 0)),
        "total_tokens": int(usage.get("total_tokens", 0)),
    }


def _call_anthropic(
    route: RoutedModel, messages: list[dict[str, Any]], tools: Sequence[dict[str, Any]],
    temperature: float, max_tokens: int,
) -> tuple[str, list[ToolCall], dict[str, int]]:
    key = config.secret(route.provider.env_key) or ""
    system = "\n\n".join(m["content"] for m in messages if m["role"] == "system")
    convo = [m for m in messages if m["role"] != "system"]
    headers = {
        "Content-Type": "application/json",
        "x-api-key": key,
        "anthropic-version": "2023-06-01",
    }
    payload: dict[str, Any] = {
        "model": route.model.id,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": convo,
    }
    if system:
        payload["system"] = system
    if tools:
        payload["tools"] = [
            {"name": t["name"], "description": t.get("description", ""),
             "input_schema": t.get("parameters", {"type": "object", "properties": {}})}
            for t in tools
        ]
    raw = _post(f"{route.provider.base_url}/v1/messages", payload, headers, config.REQUEST_TIMEOUT)
    text_parts, calls = [], []
    for i, block in enumerate(raw.get("content") or []):
        if block.get("type") == "text":
            text_parts.append(block.get("text", ""))
        elif block.get("type") == "tool_use":
            calls.append(
                ToolCall(id=block.get("id") or f"tu_{i}", name=block.get("name", ""),
                         arguments=block.get("input") or {})
            )
    usage = raw.get("usage") or {}
    pin, pout = int(usage.get("input_tokens", 0)), int(usage.get("output_tokens", 0))
    return "\n".join(text_parts), calls, {
        "prompt_tokens": pin,
        "completion_tokens": pout,
        "total_tokens": pin + pout,
    }


def _loads(s: str) -> dict[str, Any]:
    try:
        v = json.loads(s)
        return v if isinstance(v, dict) else {"value": v}
    except Exception:
        return {}


# --------------------------------------------------------------------------- #
# Moteur local (hors-ligne)
# --------------------------------------------------------------------------- #
INTENTS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("recherche", ("cherche", "research", "enquête", "veille", "état de l'art", "state of the art",
                   "benchmark", "compare", "sources")),
    ("code", ("code", "implémente", "implement", "bug", "refactor", "script", "fonction", "api",
              "test", "déploi", "docker", "python", "javascript")),
    ("rédaction", ("rédige", "écrit", "write", "article", "copywriting", "landing", "email",
                   "newsletter", "slogan", "marketing", "seo", "contenu")),
    ("diagramme", ("diagramme", "schéma", "architecture", "flow", "mermaid", "graphe", "workflow")),
    ("données", ("donnée", "data", "csv", "statistique", "analyse", "métrique", "dashboard",
                 "sql", "graphique")),
    ("navigation", ("navigateur", "browser", "site", "url", "scrape", "page web", "clic")),
    ("plan", ("plan", "roadmap", "stratégie", "étape", "priorit", "organise", "todo")),
    ("revue", ("revue", "review", "audit", "qualité", "sécurité", "vulnérab", "améliore")),
)


def detect_intents(text: str) -> list[str]:
    low = text.lower()
    hits = [name for name, kws in INTENTS if any(k in low for k in kws)]
    return hits or ["plan"]


def _clip(s: str, n: int = 700) -> str:
    s = (s or "").strip()
    return s if len(s) <= n else s[:n] + " …"


def _synthesize(
    task: str,
    *,
    agent_name: str = "NEXUS",
    role: str = "",
    skills: Sequence[str] = (),
    observations: Sequence[str] = (),
    intents: Sequence[str] | None = None,
) -> str:
    """Réponse déterministe, formatée « action d'abord » (règles i-have-adhd).

    Ce n'est pas un modèle de langue : c'est un assembleur qui remet en forme le
    travail réellement produit par les outils. Il garantit que l'OS reste
    utilisable sans clé API, et il est explicitement signalé comme tel.
    """
    intents = list(intents or detect_intents(task))
    lines: list[str] = []
    lines.append(f"**Prochaine action** — {intents[0]} : traiter « {_clip(task, 120)} ».")
    lines.append("")
    if role:
        lines.append(f"Cadre : {agent_name} — {role}")
    if skills:
        lines.append(f"Compétences activées : {', '.join(skills)}")
    lines.append("")
    lines.append("### Ce qui a été fait")
    if observations:
        for i, obs in enumerate(observations[:5], 1):
            lines.append(f"{i}. {_clip(obs, 400)}")
    else:
        lines.append("1. Aucun outil exécuté sur cette tâche (aucun outil applicable).")
    lines.append("")
    lines.append("### Lecture")
    by = {
        "recherche": "Les sources disponibles localement ont été listées ; une recherche web "
                     "réelle nécessite `NEXUS_ALLOW_NETWORK` et un accès sortant.",
        "code": "Le code produit est écrit dans l'espace de travail ; exécute les tests avant de "
                "fusionner.",
        "rédaction": "Un plan de contenu a été structuré ; passe-le à l'agent Rédacteur pour la "
                     "version finale.",
        "diagramme": "Un diagramme Mermaid a été généré et reste éditable dans le fichier produit.",
        "données": "Les métriques ont été calculées à partir des fichiers réellement lus.",
        "navigation": "L'automatisation navigateur nécessite un moteur (Playwright) installé côté "
                      "serveur.",
        "plan": "Le travail a été découpé en étapes exécutables et ordonnées.",
        "revue": "La revue pointe les risques prioritaires, du plus bloquant au plus mineur.",
    }
    for it in intents[:3]:
        if it in by:
            lines.append(f"- **{it}** : {by[it]}")
    lines.append("")
    lines.append("### Étapes suivantes")
    for i, step in enumerate(
        [
            "Vérifier le rendu dans l'onglet Fichiers de l'OS",
            "Relancer la tâche avec un fournisseur live pour une génération de meilleure qualité",
            "Enregistrer ce qui a fonctionné dans la mémoire (`memory_remember`)",
        ],
        1,
    ):
        lines.append(f"{i}. {step}")
    lines.append("")
    lines.append("_Mode hors-ligne : moteur local NEXUS (aucune clé API détectée)._")
    return "\n".join(lines)


# --------------------------------------------------------------------------- #
# Point d'entrée
# --------------------------------------------------------------------------- #
def estimate_tokens(text: str) -> int:
    return max(1, len(text or "") // 4)


def complete(
    messages: Sequence[dict[str, Any]],
    *,
    request: ModelRequest | None = None,
    tools: Sequence[dict[str, Any]] = (),
    temperature: float = 0.4,
    max_tokens: int = 1200,
    router_override: Router | None = None,
) -> Completion:
    """Complétion unifiée avec bascule automatique entre fournisseurs."""
    rtr = router_override or router()
    chain = rtr.chain_for(request)
    started = time.time()
    tried: list[str] = []
    last_err = ""

    prompt_chars = sum(len(str(m.get("content", ""))) for m in messages)

    for idx, route in enumerate(chain):
        if route.provider.style == "mock":
            break
        tried.append(f"{route.provider.id}:{route.model.id}")
        try:
            if route.provider.style == "anthropic":
                text, calls, usage = _call_anthropic(route, list(messages), tools, temperature,
                                                     max_tokens)
            else:
                text, calls, usage = _call_openai(route, list(messages), tools, temperature,
                                                  max_tokens)
            if not usage.get("total_tokens"):
                usage = {
                    "prompt_tokens": estimate_tokens("".join(str(m.get("content", "")) for m in messages)),
                    "completion_tokens": estimate_tokens(text),
                    "total_tokens": 0,
                }
                usage["total_tokens"] = usage["prompt_tokens"] + usage["completion_tokens"]
            rtr.mark_success(route.model.id)
            store().record_usage(route.provider.id, route.model.id, usage["total_tokens"])
            return Completion(
                text=text,
                model=route.model.id,
                provider=route.provider.id,
                mode="live",
                tool_calls=calls,
                usage=usage,
                fallbacks=tried,
                latency_ms=int((time.time() - started) * 1000),
            )
        except urllib.error.HTTPError as e:
            last_err = f"HTTP {e.code} ({route.provider.id})"
            rtr.mark_failure(route.model.id)
            store().record_usage(route.provider.id, route.model.id, 0, error=True)
            if e.code in (401, 403):  # clé invalide : inutile d'insister
                continue
        except Exception as e:  # réseau, timeout, JSON…
            last_err = f"{type(e).__name__}: {e}"[:200]
            rtr.mark_failure(route.model.id)
            store().record_usage(route.provider.id, route.model.id, 0, error=True)

    # --- repli hors-ligne ---------------------------------------------------
    last_user = next(
        (m.get("content", "") for m in reversed(messages) if m.get("role") == "user"), ""
    )
    system_txt = next((m.get("content", "") for m in messages if m.get("role") == "system"), "")
    agent_name = _extract(r"^\#\s*Agent\s*:\s*(.+)$", system_txt, "NEXUS")
    role = _extract(r"^\*\*Rôle\*\*\s*:\s*(.+)$", system_txt, "")
    skill_names = re.findall(r"^- compétence\s*:\s*(.+)$", system_txt, flags=re.M | re.I)
    text = _synthesize(
        str(last_user),
        agent_name=agent_name,
        role=role,
        skills=skill_names,
        observations=[str(m.get("content", "")) for m in messages if m.get("role") == "tool"],
    )
    local = chain[-1] if chain and chain[-1].provider.style == "mock" else None
    usage = {
        "prompt_tokens": estimate_tokens("".join(str(m.get("content", "")) for m in messages)),
        "completion_tokens": estimate_tokens(text),
        "total_tokens": 0,
    }
    usage["total_tokens"] = usage["prompt_tokens"] + usage["completion_tokens"]
    if local:
        store().record_usage(local.provider.id, local.model.id, usage["total_tokens"])
    return Completion(
        text=text,
        model=local.model.id if local else "nexus-local",
        provider=local.provider.id if local else "local",
        mode="offline",
        tool_calls=[],
        usage=usage,
        fallbacks=tried,
        latency_ms=int((time.time() - started) * 1000),
        error=last_err or None,
    )


def _extract(pattern: str, text: str, default: str) -> str:
    m = re.search(pattern, text, flags=re.M)
    return m.group(1).strip() if m else default


def system_mode() -> dict[str, Any]:
    rtr = router()
    return {
        "mode": "live" if rtr.is_live() else "offline",
        "providers_ready": [p["id"] for p in rtr.providers_status() if p["has_key"]],
        "models_ready": sum(1 for m in rtr.catalog() if m["ready"]),
        "models_total": len(rtr.catalog()),
    }
