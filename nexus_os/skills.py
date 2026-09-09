"""Framework de compétences au format `SKILL.md` (superpowers / openai-skills).

Une compétence = un dossier avec un `SKILL.md` portant un frontmatter :

    ---
    name: diagram-design
    description: Génère des diagrammes d'architecture et de flux.
    triggers: [diagramme, schéma, architecture, mermaid]
    tags: [architecture, visualisation]
    tools: [write_file]
    ---
    # corps markdown = instructions injectées dans le system prompt

Les compétences sont découvertes dans `nexus_os/skills/` (intégrées) et
`.nexus/skills/` (utilisateur, priorité supérieure à nom égal).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Iterable, Sequence

from nexus_os import config

_FRONT = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.S)


def _split_list(raw: str) -> list[str]:
    raw = raw.strip().strip("[]")
    if not raw:
        return []
    return [p.strip().strip("'\"") for p in raw.split(",") if p.strip()]


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    """Mini-parseur YAML (clés plates + listes inline) — aucune dépendance."""
    m = _FRONT.match(text.lstrip("\ufeff"))
    if not m:
        return {}, text
    head, body = m.group(1), m.group(2)
    meta: dict[str, Any] = {}
    for line in head.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip().lower().replace(" ", "_")
        val = val.strip()
        if key in {"triggers", "tags", "tools", "models", "requires"}:
            meta[key] = _split_list(val)
        elif val.lower() in {"true", "false"}:
            meta[key] = val.lower() == "true"
        else:
            try:
                meta[key] = int(val)
            except ValueError:
                meta[key] = val.strip("'\"")
    return meta, body.strip()


@dataclass
class Skill:
    name: str
    description: str = ""
    body: str = ""
    triggers: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    source: str = "builtin"
    path: str = ""
    license: str = ""

    def to_dict(self, *, with_body: bool = False) -> dict[str, Any]:
        d = asdict(self)
        if not with_body:
            d["body"] = f"{len(self.body)} caractères"
        return d

    def prompt_block(self) -> str:
        return f"## Compétence : {self.name}\n{self.description}\n\n{self.body}".strip()

    def score(self, text: str) -> float:
        """Pertinence d'une compétence pour un texte (triggers + tags)."""
        low = (text or "").lower()
        if not low:
            return 0.0
        s = 0.0
        for t in self.triggers:
            t = t.lower()
            if t and t in low:
                s += 3.0 + min(2.0, len(t) / 12)
        for g in self.tags:
            if g.lower() in low:
                s += 1.0
        if self.name.lower().replace("-", " ") in low:
            s += 2.0
        return s


class SkillLibrary:
    def __init__(self, dirs: Iterable[Path] | None = None) -> None:
        self.dirs = list(dirs) if dirs else [config.BUILTIN_SKILLS_DIR, config.USER_SKILLS_DIR]
        self._cache: dict[str, Skill] | None = None

    # --- découverte --------------------------------------------------------
    def load(self, force: bool = False) -> dict[str, Skill]:
        if self._cache is not None and not force:
            return self._cache
        found: dict[str, Skill] = {}
        for d in self.dirs:
            if not d.exists():
                continue
            for md in sorted(d.rglob("SKILL.md")):
                try:
                    raw = md.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    continue
                meta, body = parse_frontmatter(raw)
                name = str(meta.get("name") or md.parent.name).strip()
                source = "builtin" if config.BUILTIN_SKILLS_DIR in md.parents else "user"
                found[name] = Skill(
                    name=name,
                    description=str(meta.get("description", "")),
                    body=body,
                    triggers=[str(x) for x in meta.get("triggers", [])],
                    tags=[str(x) for x in meta.get("tags", [])],
                    tools=[str(x) for x in meta.get("tools", [])],
                    source=source,
                    path=str(md),
                    license=str(meta.get("license", "")),
                )
        self._cache = found
        return found

    def all(self) -> list[Skill]:
        return sorted(self.load().values(), key=lambda s: s.name)

    def get(self, name: str) -> Skill | None:
        return self.load().get(name)

    def select(self, names: Sequence[str]) -> list[Skill]:
        lib = self.load()
        return [lib[n] for n in names if n in lib]

    def match(self, text: str, *, limit: int = 4, threshold: float = 2.0) -> list[Skill]:
        """Compétences pertinentes pour une tâche (routage par triggers)."""
        scored = [(s.score(text), s) for s in self.all()]
        scored = [(sc, s) for sc, s in scored if sc >= threshold]
        scored.sort(key=lambda x: (-x[0], x[1].name))
        return [s for _, s in scored[:limit]]

    def render(self, skills: Sequence[Skill]) -> str:
        if not skills:
            return ""
        return "\n\n".join(s.prompt_block() for s in skills)


_library: SkillLibrary | None = None


def library() -> SkillLibrary:
    global _library
    if _library is None:
        _library = SkillLibrary()
    return _library
