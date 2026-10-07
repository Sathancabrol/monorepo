"""Routeur de modèles multi-fournisseurs (inspiré OmniRoute).

Un seul point d'entrée (`Router.route`), un catalogue de fournisseurs/modèles,
sélection *quota-aware* avec bascule automatique : si un fournisseur n'a pas de
clé, dépasse son budget du jour ou renvoie une erreur, la chaîne passe au
suivant. Le catalogue est volontairement éditable ici — c'est de la config, pas
de la logique.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field, asdict
from typing import Any, Literal

from nexus_os import config
from nexus_os.db import store

ApiStyle = Literal["openai", "anthropic", "mock"]


@dataclass(frozen=True)
class ModelSpec:
    id: str
    label: str
    context: int = 128_000
    free: bool = False
    #: $ par million de tokens (entrée, sortie) — indicatif, sert au tri/coût.
    price_in: float = 0.0
    price_out: float = 0.0
    vision: bool = False
    tools: bool = True
    reasoning: bool = False


@dataclass(frozen=True)
class ProviderSpec:
    id: str
    name: str
    base_url: str
    env_key: str
    style: ApiStyle = "openai"
    models: tuple[ModelSpec, ...] = ()
    priority: int = 100  # plus bas = testé en premier
    #: budget de tokens/jour propre au fournisseur (None = config globale)
    daily_budget: int | None = None


# --------------------------------------------------------------------------- #
# Catalogue
# --------------------------------------------------------------------------- #
PROVIDERS: tuple[ProviderSpec, ...] = (
    ProviderSpec(
        id="anthropic",
        name="Anthropic",
        base_url="https://api.anthropic.com",
        env_key="ANTHROPIC_API_KEY",
        style="anthropic",
        priority=10,
        models=(
            ModelSpec("claude-opus-4-5", "Claude Opus 4.5", 200_000, price_in=15, price_out=75,
                      vision=True, reasoning=True),
            ModelSpec("claude-sonnet-4-5", "Claude Sonnet 4.5", 200_000, price_in=3, price_out=15,
                      vision=True, reasoning=True),
            ModelSpec("claude-haiku-4-5", "Claude Haiku 4.5", 200_000, price_in=0.8, price_out=4),
        ),
    ),
    ProviderSpec(
        id="openai",
        name="OpenAI",
        base_url="https://api.openai.com/v1",
        env_key="OPENAI_API_KEY",
        priority=20,
        models=(
            ModelSpec("gpt-5.2", "GPT-5.2", 400_000, price_in=2.5, price_out=10, vision=True,
                      reasoning=True),
            ModelSpec("gpt-5-mini", "GPT-5 mini", 400_000, price_in=0.25, price_out=2, vision=True),
            ModelSpec("gpt-4.1-mini", "GPT-4.1 mini", 1_000_000, price_in=0.4, price_out=1.6,
                      vision=True),
        ),
    ),
    ProviderSpec(
        id="google",
        name="Google Gemini",
        base_url="https://generativelanguage.googleapis.com/v1beta/openai",
        env_key="GEMINI_API_KEY",
        priority=30,
        models=(
            ModelSpec("gemini-3-pro", "Gemini 3 Pro", 1_000_000, price_in=1.25, price_out=10,
                      vision=True, reasoning=True),
            ModelSpec("gemini-3-flash", "Gemini 3 Flash", 1_000_000, free=True, vision=True),
        ),
    ),
    ProviderSpec(
        id="openrouter",
        name="OpenRouter",
        base_url="https://openrouter.ai/api/v1",
        env_key="OPENROUTER_API_KEY",
        priority=40,
        models=(
            ModelSpec("deepseek/deepseek-v3.2", "DeepSeek V3.2", 128_000, price_in=0.28,
                      price_out=0.42),
            ModelSpec("moonshotai/kimi-k2", "Kimi K2", 256_000, price_in=0.6, price_out=2.5),
            ModelSpec("qwen/qwen3-max", "Qwen3 Max", 256_000, price_in=1.2, price_out=6),
            ModelSpec("z-ai/glm-4.6", "GLM-4.6", 200_000, price_in=0.6, price_out=2.2),
            ModelSpec("minimax/minimax-m2", "MiniMax M2", 200_000, free=True),
        ),
    ),
    ProviderSpec(
        id="groq",
        name="Groq",
        base_url="https://api.groq.com/openai/v1",
        env_key="GROQ_API_KEY",
        priority=50,
        daily_budget=400_000,
        models=(
            ModelSpec("llama-3.3-70b-versatile", "Llama 3.3 70B", 128_000, free=True),
            ModelSpec("openai/gpt-oss-120b", "gpt-oss 120B", 128_000, free=True, reasoning=True),
        ),
    ),
    ProviderSpec(
        id="mistral",
        name="Mistral",
        base_url="https://api.mistral.ai/v1",
        env_key="MISTRAL_API_KEY",
        priority=60,
        models=(
            ModelSpec("mistral-large-latest", "Mistral Large", 256_000, price_in=2, price_out=6),
            ModelSpec("devstral-small-latest", "Devstral Small", 128_000, free=True),
        ),
    ),
    ProviderSpec(
        id="ollama",
        name="Ollama (local)",
        base_url="http://localhost:11434/v1",
        env_key="OLLAMA_API_KEY",  # optionnel : Ollama accepte n'importe quelle valeur
        priority=70,
        daily_budget=0,  # illimité
        models=(
            ModelSpec("qwen2.5-coder:14b", "Qwen2.5 Coder 14B", 32_000, free=True),
            ModelSpec("llama3.1:8b", "Llama 3.1 8B", 128_000, free=True),
        ),
    ),
    ProviderSpec(
        id="local",
        name="Moteur local NEXUS",
        base_url="",
        env_key="",
        style="mock",
        priority=999,
        daily_budget=0,
        models=(
            ModelSpec("nexus-local", "NEXUS local (hors-ligne)", 32_000, free=True),
        ),
    ),
)

PROVIDER_BY_ID: dict[str, ProviderSpec] = {p.id: p for p in PROVIDERS}
MODEL_INDEX: dict[str, tuple[ProviderSpec, ModelSpec]] = {
    m.id: (p, m) for p in PROVIDERS for m in p.models
}


@dataclass
class RoutedModel:
    """Résultat de routage : le modèle choisi + la chaîne de secours essayée."""

    model: ModelSpec
    provider: ProviderSpec
    reason: str = ""
    fallbacks: list[dict[str, str]] = field(default_factory=list)

    @property
    def model_id(self) -> str:
        return self.model.id

    def to_dict(self) -> dict[str, Any]:
        return {
            "model": self.model.id,
            "provider": self.provider.id,
            "reason": self.reason,
            "fallbacks": self.fallbacks,
            "style": self.provider.style,
            "base_url": self.provider.base_url,
        }


@dataclass
class ModelRequest:
    """Contraintes exprimées par l'appelant (agent, tâche, phase)."""

    preferred: str | None = None
    need_tools: bool = False
    need_vision: bool = False
    need_reasoning: bool = False
    min_context: int = 0
    prefer_free: bool | None = None
    exclude: tuple[str, ...] = ()


class Router:
    """Sélection quota-aware + bascule automatique."""

    def __init__(self, *, budget: int | None = None) -> None:
        self.budget = config.DAILY_TOKEN_BUDGET if budget is None else budget
        self._failures: dict[str, float] = {}  # model_id -> timestamp du dernier échec
        self.cooldown = 300  # s : un modèle en erreur est écarté 5 min

    # --- état --------------------------------------------------------------
    def has_key(self, provider: ProviderSpec) -> bool:
        """Un fournisseur est « configuré » si sa clé est présente.

        Ollama n'exige pas de secret côté serveur, mais on exige quand même
        ``OLLAMA_API_KEY`` (n'importe quelle valeur) : sans marqueur explicite,
        un démon absent ferait croire à un mode live qui ne répond pas.
        """
        if provider.style == "mock":
            return True
        return bool(config.secret(provider.env_key))

    def budget_of(self, provider: ProviderSpec) -> int:
        if provider.daily_budget is not None:
            return provider.daily_budget
        return self.budget

    def quota_left(self, provider: ProviderSpec) -> int | None:
        b = self.budget_of(provider)
        if not b:
            return None
        return max(0, b - store().tokens_today(provider.id))

    def cooling_down(self, model_id: str) -> bool:
        ts = self._failures.get(model_id)
        return bool(ts and (time.time() - ts) < self.cooldown)

    def mark_failure(self, model_id: str) -> None:
        self._failures[model_id] = time.time()

    def mark_success(self, model_id: str) -> None:
        self._failures.pop(model_id, None)

    # --- catalogue ---------------------------------------------------------
    def catalog(self) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for p in sorted(PROVIDERS, key=lambda x: x.priority):
            key = self.has_key(p)
            left = self.quota_left(p)
            for m in p.models:
                out.append(
                    {
                        **asdict(m),
                        "provider": p.id,
                        "provider_name": p.name,
                        "ready": key and not self.cooling_down(m.id),
                        "has_key": key,
                        "quota_left": left,
                        "cooling_down": self.cooling_down(m.id),
                        "style": p.style,
                    }
                )
        return out

    def providers_status(self) -> list[dict[str, Any]]:
        out = []
        for p in sorted(PROVIDERS, key=lambda x: x.priority):
            left = self.quota_left(p)
            budget = self.budget_of(p)
            used = store().tokens_today(p.id)
            out.append(
                {
                    "id": p.id,
                    "name": p.name,
                    "style": p.style,
                    "base_url": p.base_url,
                    "env_key": p.env_key,
                    "has_key": self.has_key(p),
                    "models": len(p.models),
                    "budget": budget or None,
                    "used_today": used,
                    "quota_left": left,
                    "priority": p.priority,
                }
            )
        return out

    def is_live(self) -> bool:
        """True si au moins un vrai fournisseur (hors moteur local) est utilisable."""
        return any(self.has_key(p) for p in PROVIDERS if p.style != "mock")

    # --- routage -----------------------------------------------------------
    def candidates(self, req: ModelRequest | None = None) -> list[tuple[ProviderSpec, ModelSpec, str]]:
        """Chaîne ordonnée de (fournisseur, modèle, motif) prête pour la bascule."""
        req = req or ModelRequest()
        scored: list[tuple[float, ProviderSpec, ModelSpec, str]] = []
        for p in PROVIDERS:
            if p.style == "mock":
                continue  # toujours gardé en dernier recours, ajouté après le tri
            if not self.has_key(p):
                continue
            if (self.quota_left(p) or 0) <= 0 and self.budget_of(p):
                continue
            for m in p.models:
                if m.id in req.exclude or p.id in req.exclude:
                    continue
                if req.need_tools and not m.tools:
                    continue
                if req.need_vision and not m.vision:
                    continue
                if req.need_reasoning and not m.reasoning:
                    continue
                if m.context < req.min_context:
                    continue
                if self.cooling_down(m.id):
                    continue
                score = float(p.priority)
                if req.prefer_free is None and config.PREFER_FREE or req.prefer_free:
                    score -= 40 if m.free else 0
                score += m.price_in + m.price_out  # le moins cher d'abord
                if req.preferred and (m.id == req.preferred or p.id == req.preferred):
                    score -= 1000  # choix explicite de l'utilisateur
                reason = "choix explicite" if score < 0 else ("gratuit" if m.free else "quota+coût")
                scored.append((score, p, m, reason))
        scored.sort(key=lambda x: x[0])
        chain = [(p, m, r) for _, p, m, r in scored]
        chain.append((PROVIDER_BY_ID["local"], PROVIDER_BY_ID["local"].models[0],
                      "repli hors-ligne (aucun fournisseur joignable)"))
        return chain

    def route(self, req: ModelRequest | None = None) -> RoutedModel:
        chain = self.candidates(req)
        p, m, reason = chain[0]
        return RoutedModel(
            model=m,
            provider=p,
            reason=reason,
            fallbacks=[{"model": mm.id, "provider": pp.id, "reason": rr} for pp, mm, rr in chain[1:]],
        )

    def chain_for(self, req: ModelRequest | None = None) -> list[RoutedModel]:
        """Toute la chaîne sous forme de RoutedModel (pour la bascule côté llm)."""
        chain = self.candidates(req)
        return [
            RoutedModel(model=m, provider=p, reason=r) for p, m, r in chain
        ]
