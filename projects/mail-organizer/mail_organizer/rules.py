"""Moteur de règles : associe un message à un dossier cible.

La première règle qui correspond gagne. La comparaison ignore la casse et
les accents (normalisation NFD), pour que « Alerte de sécurité » et
« alerte de securite » soient équivalents.
"""

from __future__ import annotations

import unicodedata
from dataclasses import dataclass, field
from email.utils import parseaddr
from typing import Iterable


def normalize(text: str) -> str:
    """Minuscules + suppression des accents (NFD)."""
    if not text:
        return ""
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return text.lower()


def extract_address(from_header: str) -> str:
    """Extrait l'adresse e-mail d'un en-tête From (« Nom <a@b.c> » → a@b.c)."""
    if not from_header:
        return ""
    name, addr = parseaddr(from_header)
    return (addr or from_header).strip().lower()


def extract_domain(address: str) -> str:
    return address.rsplit("@", 1)[-1].lower() if "@" in address else ""


@dataclass
class MessageMeta:
    """Métadonnées minimales d'un message, suffisantes pour le classer."""

    uid: int
    from_addr: str = ""
    subject: str = ""
    date: str = ""
    header_names: frozenset = field(default_factory=frozenset)

    @property
    def domain(self) -> str:
        """Domaine de l'adresse e-mail, même si from_addr contient un nom (« Nom <a@b.c> »)."""
        return extract_domain(extract_address(self.from_addr))


@dataclass
class Rule:
    folder: str
    from_domains: list[str] = field(default_factory=list)
    from_contains: list[str] = field(default_factory=list)
    subject_contains: list[str] = field(default_factory=list)
    has_header: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, raw: dict) -> "Rule":
        return cls(
            folder=raw["folder"],
            from_domains=[normalize(d) for d in raw.get("from_domains", [])],
            from_contains=[normalize(c) for c in raw.get("from_contains", [])],
            subject_contains=[normalize(s) for s in raw.get("subject_contains", [])],
            has_header=[h.lower() for h in raw.get("has_header", [])],
        )

    def matches(self, meta: MessageMeta) -> bool:
        domain = meta.domain
        if domain and any(domain == d or domain.endswith("." + d) for d in self.from_domains):
            return True
        sender = normalize(meta.from_addr)
        if sender and any(c in sender for c in self.from_contains):
            return True
        subject = normalize(meta.subject)
        if subject and any(s in subject for s in self.subject_contains):
            return True
        if self.has_header and any(h in meta.header_names for h in self.has_header):
            return True
        return False


def classify(meta: MessageMeta, rules: Iterable[Rule], default_folder: str) -> str:
    """Retourne le dossier cible du message (première règle gagnante)."""
    for rule in rules:
        if rule.matches(meta):
            return rule.folder
    return default_folder


def top_domains(metas: list[MessageMeta], count: int = 25) -> list[tuple[str, int]]:
    """Statistiques : domaines d'expéditeurs les plus fréquents.

    Utile pour découvrir les règles à ajouter à la config.
    """
    tally: dict[str, int] = {}
    for meta in metas:
        dom = meta.domain or "(inconnu)"
        tally[dom] = tally.get(dom, 0) + 1
    return sorted(tally.items(), key=lambda kv: (-kv[1], kv[0]))[:count]
