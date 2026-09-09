"""Registre d'agents : specs intégrées (JSON) + agents créés par l'utilisateur."""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterable

from nexus_os import config

VALID_AUTONOMY = ("manuel", "assisté", "autonome")

#: Ordre du cycle de vie (inspiré ECC) — chaque agent peut n'en garder qu'une partie.
LIFECYCLE = ("plan", "research", "implement", "review", "verify", "remember", "improve")


@dataclass
class AgentSpec:
    id: str
    name: str
    role: str = ""
    description: str = ""
    emoji: str = "🤖"
    system_prompt: str = ""
    skills: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    triggers: list[str] = field(default_factory=list)
    model: str = ""            # préférence de modèle ("" = décision du routeur)
    temperature: float = 0.4
    max_steps: int = 6
    autonomy: str = "assisté"
    lifecycle: list[str] = field(default_factory=lambda: list(LIFECYCLE))
    builtin: bool = False
    source: str = "builtin"
    created_at: float = field(default_factory=time.time)
    tags: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.autonomy not in VALID_AUTONOMY:
            self.autonomy = "assisté"
        self.lifecycle = [p for p in self.lifecycle if p in LIFECYCLE] or list(LIFECYCLE)
        self.tools = [t for t in self.tools]

    # --- sérialisation -----------------------------------------------------
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "AgentSpec":
        known = {f for f in cls.__dataclass_fields__}  # type: ignore[attr-defined]
        return cls(**{k: v for k, v in data.items() if k in known})

    # --- prompt ------------------------------------------------------------
    def base_prompt(self, skill_text: str = "", memory_text: str = "") -> str:
        parts = [
            f"# Agent : {self.name}",
            f"**Rôle** : {self.role}",
            "",
            self.system_prompt.strip() or self.description,
            "",
            "## Règles de sortie (obligatoires)",
            "1. Commence par la prochaine action concrète, jamais par un préambule.",
            "2. Numérote tout travail multi-étapes ; termine par une seule prochaine étape.",
            "3. Liste au maximum 5 éléments ; coupe les tangentes.",
            "4. Erreurs : factuelles, sans excuse ni dramatisation.",
            "5. Si tu utilises un outil, annonce-le en une ligne avant l'appel.",
            "6. Ne prétends jamais avoir lu, exécuté ou vérifié ce que tu n'as pas fait.",
        ]
        for s in self.skills:
            parts.append(f"- compétence : {s}")
        if skill_text:
            parts += ["", "## Compétences activées", skill_text]
        if memory_text:
            parts += ["", "## Mémoire (rappel)", memory_text]
        return "\n".join(p for p in parts if p is not None)

    def score(self, task: str) -> float:
        """Affinité agent ↔ tâche : base du routage de l'orchestrateur."""
        low = (task or "").lower()
        if not low:
            return 0.0
        s = 0.0
        for t in self.triggers:
            if t.lower() in low:
                s += 3.0 + min(2.0, len(t) / 12)
        for word in re.findall(r"[a-zà-ÿ0-9]{4,}", f"{self.role} {self.description}".lower()):
            if word in low:
                s += 0.4
        for tag in self.tags:
            if tag.lower() in low:
                s += 1.2
        return s


class AgentRegistry:
    def __init__(self, builtin_dir: Path | None = None, user_dir: Path | None = None) -> None:
        self.builtin_dir = builtin_dir or config.BUILTIN_AGENTS_DIR
        self.user_dir = user_dir or config.USER_AGENTS_DIR
        self._cache: dict[str, AgentSpec] | None = None

    # --- chargement --------------------------------------------------------
    def load(self, force: bool = False) -> dict[str, AgentSpec]:
        if self._cache is not None and not force:
            return self._cache
        found: dict[str, AgentSpec] = {}
        for directory, builtin in ((self.builtin_dir, True), (self.user_dir, False)):
            if not directory.exists():
                continue
            for f in sorted(directory.glob("*.json")):
                try:
                    data = json.loads(f.read_text(encoding="utf-8"))
                except Exception:
                    continue
                data.setdefault("id", f.stem)
                data["builtin"] = builtin
                data["source"] = "builtin" if builtin else "user"
                try:
                    spec = AgentSpec.from_dict(data)
                except TypeError:
                    continue
                found[spec.id] = spec  # l'utilisateur écrase l'intégré à id égal
        self._cache = found
        return found

    def all(self) -> list[AgentSpec]:
        agents = list(self.load().values())
        return sorted(agents, key=lambda a: (not a.builtin, a.name.lower()))

    def get(self, agent_id: str) -> AgentSpec | None:
        return self.load().get(agent_id)

    def require(self, agent_id: str) -> AgentSpec:
        a = self.get(agent_id)
        if not a:
            raise KeyError(f"agent inconnu : {agent_id}")
        return a

    # --- écriture ----------------------------------------------------------
    def save(self, spec: AgentSpec, *, builtin: bool = False) -> AgentSpec:
        spec.builtin = builtin
        spec.source = "builtin" if builtin else "user"
        directory = self.builtin_dir if builtin else self.user_dir
        directory.mkdir(parents=True, exist_ok=True)
        (directory / f"{spec.id}.json").write_text(
            json.dumps(spec.to_dict(), ensure_ascii=False, indent=2), encoding="utf-8"
        )
        self.load(force=True)
        return spec

    def delete(self, agent_id: str) -> bool:
        f = self.user_dir / f"{agent_id}.json"
        if f.exists():
            f.unlink()
            self.load(force=True)
            return True
        return False

    def export_markdown(self, spec: AgentSpec) -> str:
        """Export portable d'un agent (réutilisable dans un autre harness)."""
        skills_md = [f"- {s}" for s in spec.skills] or ["-"]
        tools_md = [f"- `{t}`" for t in spec.tools] or ["-"]
        return "\n".join(
            [
                f"# {spec.emoji} {spec.name}",
                "",
                f"**Rôle** — {spec.role}",
                "",
                spec.description,
                "",
                "## Compétences",
                *skills_md,
                "",
                "## Outils",
                *tools_md,
                "",
                "## Prompt système",
                "```",
                spec.system_prompt.strip(),
                "```",
                "",
                f"_Modèle préféré : {spec.model or 'routeur automatique'} · "
                f"température {spec.temperature} · autonomie {spec.autonomy} · "
                f"cycle {' → '.join(spec.lifecycle)}_",
            ]
        )

    # --- routage -----------------------------------------------------------
    def best_for(self, task: str, *, exclude: Iterable[str] = ()) -> tuple[AgentSpec | None, float]:
        ex = set(exclude)
        scored = [(a.score(task), a) for a in self.all() if a.id not in ex]
        if not scored:
            return None, 0.0
        scored.sort(key=lambda x: (-x[0], x[1].name))
        return scored[0][1], scored[0][0]

    def ranking(self, task: str, limit: int = 5) -> list[dict[str, Any]]:
        rows = sorted(
            ((a.score(task), a) for a in self.all()), key=lambda x: (-x[0], x[1].name)
        )[:limit]
        return [
            {"agent_id": a.id, "name": a.name, "emoji": a.emoji, "role": a.role,
             "score": round(s, 2)}
            for s, a in rows
        ]


_registry: AgentRegistry | None = None


def registry() -> AgentRegistry:
    global _registry
    if _registry is None:
        _registry = AgentRegistry()
    return _registry
