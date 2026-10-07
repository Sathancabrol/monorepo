"""Instincts — la couche d'apprentissage d'ECC (`affaan-m/ECC`, 274 k★).

ECC distingue trois couches : **skills** (méthodes écrites), **instincts**
(motifs appris qui orientent la décision sans prompt explicite) et **memory**
(faits). NEXUS·OS avait les deux autres ; voici la manquante.

Un instinct n'est pas un souvenir : c'est une **règle de conduite** dérivée de
ce qui s'est réellement passé en exécution, avec un déclencheur, un compteur de
renforcements et une confiance. Concrètement, après une exécution :

* un outil qui a échoué → « vérifie X avant d'utiliser cet outil » ;
* un outil bloqué par l'approbation → « annonce-le, ne le tente pas en boucle » ;
* un outil qui a produit le livrable → « pour ce type de tâche, commence par là » ;
* une réponse « à vérifier » → « cite la source, ne conclus pas ».

Les instincts sont injectés dans le prompt système de l'agent concerné, et se
renforcent à chaque nouvelle occurrence. Ils restent éditables et supprimables :
un apprentissage automatique qu'on ne peut pas reprendre en main n'est pas un
apprentissage, c'est une dérive.
"""
from __future__ import annotations

import json
import re
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from nexus_os import config

INSTINCTS_FILE = config.NEXUS_HOME / "instincts.json"

#: En dessous de ce score, l'instinct n'est pas injecté dans le prompt.
MIN_SCORE = 1.0
#: Nombre maximal d'instincts injectés par exécution (le contexte n'est pas infini).
MAX_INJECTED = 6


@dataclass
class Instinct:
    id: str
    rule: str
    triggers: list[str] = field(default_factory=list)
    agent_id: str = ""          # vide = tous les agents
    source: str = "run"         # run | manuel
    hits: int = 0
    confidence: float = 0.5
    created: float = field(default_factory=time.time)
    last_hit: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Instinct":
        known = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in d.items() if k in known})

    def score(self, task: str, agent_id: str) -> float:
        """Pertinence pour une tâche et un agent donnés.

        Un instinct porteur de déclencheurs ne compte **que** si l'un d'eux
        correspond : injecter une règle de déploiement pendant la relecture d'un
        contrat, c'est du bruit qui coûte du contexte.
        """
        if self.agent_id and self.agent_id != agent_id:
            return 0.0
        low = (task or "").lower()
        if self.triggers:
            matched = sum(1 for t in self.triggers if t.strip() and t.lower().strip() in low)
            if not matched:
                return 0.0
            s = 2.0 * matched
        else:
            s = 0.5                       # règle générale, toujours un peu pertinente
        if self.agent_id == agent_id:
            s += 1.0
        return s * (0.5 + self.confidence)


class InstinctBook:
    def __init__(self, path: Path | None = None) -> None:
        self.path = Path(path or INSTINCTS_FILE)

    # --- persistance --------------------------------------------------------
    def _load(self) -> list[Instinct]:
        if not self.path.exists():
            return []
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return []
        return [Instinct.from_dict(x) for x in raw if isinstance(x, dict) and x.get("rule")]

    def _flush(self, rows: list[Instinct]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps([r.to_dict() for r in rows],
                                        ensure_ascii=False, indent=2) + "\n",
                             encoding="utf-8")

    # --- lecture ------------------------------------------------------------
    def all(self) -> list[Instinct]:
        return self._load()

    def count(self) -> int:
        return len(self._load())

    def get(self, instinct_id: str) -> Instinct | None:
        return next((i for i in self._load() if i.id == instinct_id), None)

    def for_task(self, task: str, agent_id: str = "") -> list[Instinct]:
        rows = [i for i in self._load() if i.score(task, agent_id) >= MIN_SCORE]
        rows.sort(key=lambda i: (-i.score(task, agent_id), -i.hits, -i.last_hit))
        return rows[:MAX_INJECTED]

    def render(self, task: str, agent_id: str = "") -> str:
        picked = self.for_task(task, agent_id)
        if not picked:
            return ""
        lines = ["## Instincts (appris d'exécutions précédentes)",
                 "Respecte-les sauf raison explicite de t'en écarter :"]
        for i in picked:
            scope = f"[{i.agent_id}] " if i.agent_id else ""
            lines.append(f"- {scope}{i.rule} ({i.hits} renforcement(s))")
        return "\n".join(lines)

    # --- écriture -----------------------------------------------------------
    def add(self, rule: str, *, triggers: list[str] | None = None, agent_id: str = "",
            source: str = "manuel", confidence: float = 0.6) -> Instinct:
        rule = (rule or "").strip()
        if len(rule) < 12:
            raise ValueError("règle trop courte (12 caractères minimum)")
        rows = self._load()
        # Même règle + même portée : on renforce au lieu de dupliquer.
        for r in rows:
            if r.rule == rule and r.agent_id == agent_id:
                r.hits += 1
                r.last_hit = time.time()
                r.confidence = min(1.0, r.confidence + 0.1)
                self._flush(rows)
                return r
        inst = Instinct(id=f"ins-{len(rows) + 1:04d}", rule=rule,
                        triggers=[t.strip() for t in (triggers or []) if t.strip()],
                        agent_id=agent_id, source=source, hits=1,
                        confidence=max(0.0, min(1.0, confidence)))
        rows.append(inst)
        self._flush(rows)
        return inst

    def reinforce(self, instinct_id: str, *, delta: float = 0.1) -> bool:
        rows = self._load()
        for r in rows:
            if r.id == instinct_id:
                r.hits += 1
                r.last_hit = time.time()
                r.confidence = max(0.0, min(1.0, r.confidence + delta))
                self._flush(rows)
                return True
        return False

    def forget(self, instinct_id: str) -> bool:
        rows = self._load()
        kept = [r for r in rows if r.id != instinct_id]
        if len(kept) == len(rows):
            return False
        self._flush(kept)
        return True

    def clear(self) -> int:
        n = len(self._load())
        self._flush([])
        return n

    # --- apprentissage ------------------------------------------------------
    def learn_from_result(self, result: Any, task: str = "") -> list[Instinct]:
        """Déduit des règles d'un `RunResult`. Retourne ce qui a été appris/renforcé."""
        learned: list[Instinct] = []
        agent_id = getattr(result, "agent_id", "") or ""
        events = getattr(result, "events", []) or []

        failures = [e for e in events if e.get("type") == "tool_result" and not e.get("ok")]
        approvals = [e for e in events if e.get("type") == "approval_required"]
        artifacts = [e for e in events if e.get("type") == "artifact"]
        used = [e.get("name") for e in events if e.get("type") == "tool_call"]

        for e in failures:
            name = e.get("name", "outil")
            reason = str(e.get("result", "")).splitlines()[0][:140] if e.get("result") else ""
            learned.append(self.add(
                f"L'outil `{name}` a échoué ici ({reason}). Vérifie son prérequis "
                f"avant de le relancer, ou choisis une autre voie.",
                triggers=_keywords(task) + [name], agent_id=agent_id,
                source="run", confidence=0.45))

        blocked = sorted({e.get("name") for e in approvals if e.get("name")})
        if blocked:
            learned.append(self.add(
                f"{', '.join(f'`{b}`' for b in blocked)} exige une autorisation "
                "explicite : annonce-le d'emblée au lieu de le tenter en boucle.",
                triggers=_keywords(task) + blocked, agent_id=agent_id,
                source="run", confidence=0.55))

        if artifacts and used:
            winner = used[0]
            learned.append(self.add(
                f"Pour ce type de demande, `{winner}` a produit le livrable "
                f"({len(artifacts)} artéfact(s)) : commence par là.",
                triggers=_keywords(task), agent_id=agent_id, source="run",
                confidence=0.4))

        if (getattr(result, "confidence", "") == "confiant" and not failures
                and len(used) >= 2):
            seq = " → ".join(dict.fromkeys(used))
            learned.append(self.add(
                f"Séquence qui a fonctionné ici : {seq}. Réutilise-la plutôt "
                "que d'improviser un autre enchaînement.",
                triggers=_keywords(task), agent_id=agent_id, source="run",
                confidence=0.4))

        if getattr(result, "confidence", "") == "à vérifier":
            learned.append(self.add(
                "Cette conclusion était « à vérifier » : cite la source exacte et "
                "sépare ce qui est mesuré de ce qui est déduit.",
                triggers=_keywords(task), agent_id=agent_id, source="run",
                confidence=0.35))
        return learned


#: Mots trop fréquents pour servir de déclencheur.
_STOP = frozenset("""le la les un une des du de d et ou à a en dans sur pour qui que avec sans
ce cet cette ces est sont être je tu il elle nous vous ils plus tout tous toute toutes faire fait
mon ton son ma ta sa mes tes ses par pas ne""".split())


def _keywords(text: str, limit: int = 4) -> list[str]:
    words = re.findall(r"[a-zà-ÿ]{5,}", (text or "").lower())
    out: list[str] = []
    for w in words:
        if w in _STOP or w in out:
            continue
        out.append(w)
        if len(out) >= limit:
            break
    return out


_book: InstinctBook | None = None


def book() -> InstinctBook:
    global _book
    if _book is None:
        _book = InstinctBook()
    return _book
