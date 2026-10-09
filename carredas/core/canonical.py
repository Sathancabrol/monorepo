# -*- coding: utf-8 -*-
"""Contrat de données partagé — l'enregistrement canonique.

Une seule idée, et elle est structurante : **toute information qui traverse
l'application doit pouvoir se ramener à la même forme**. Un outil référencé, une
preuve collectée, une décision prise en réunion, un point sur la carte, un
indicateur de prévision — ce sont cinq objets métier différents, mais un seul
enregistrement canonique.

Sans ce contrat, chaque module parle sa langue et les liens entre eux se font à
la main. Avec lui, relier une preuve documentaire à un lieu et à une décision
devient mécanique, et surtout : l'origine de l'information ne se perd jamais.

Champs porteurs de sens :
  * `status` distingue **fact** (constaté) / **inference** (déduit) /
    **hypothesis** (supposé). Un système qui mélange les trois produit des
    documents indéfendables — c'est la règle que le module OSINT applique déjà
    avec sa cotation A→X.
  * `observed_at` ≠ `retrieved_at` : quand le fait s'est produit n'est pas
    quand on l'a appris. Indispensable en prévision et en investigation.
  * `provenance` : qui, comment, à partir de quoi.
"""

from __future__ import annotations

import datetime as _dt
import json
import re
from pathlib import Path

ICI = Path(__file__).resolve().parent

STATUTS = ("fact", "inference", "hypothesis", "unknown")

# Équivalences entre les échelles de confiance des modules et le contrat.
FIABILITE_OSINT = {"A": "fact", "B": "fact", "C": "inference",
                   "D": "hypothesis", "X": "unknown"}


def _charger(nom: str) -> dict:
    return json.loads((ICI / nom).read_text(encoding="utf-8"))


def schema(lequel: str = "canonical-record.schema.json") -> dict:
    return _charger(lequel)


def maintenant() -> str:
    return _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def enregistrement(identifiant: str, type_: str, source: str,
                   statut: str = "unknown", label: str = "", **reste) -> dict:
    """Fabrique un enregistrement canonique. Les champs inconnus sont ignorés."""
    rec = {
        "id": str(identifiant),
        "type": str(type_),
        "label": label or "",
        "source": str(source),
        "source_url": None,
        "retrieved_at": None,
        "observed_at": None,
        "valid_from": None,
        "valid_to": None,
        "geometry": None,
        "provenance": None,
        "confidence": None,
        "license": None,
        "status": statut if statut in STATUTS else "unknown",
        "relations": [],
    }
    for k, v in reste.items():
        if k in rec and k not in ("id", "type", "source"):
            rec[k] = v
    return rec


def valider(rec: dict) -> tuple[bool, list[str]]:
    """Validation minimale et volontairement sans dépendance.

    On ne réimplémente pas JSON Schema : on vérifie l'essentiel — les champs
    obligatoires, les valeurs d'énumération, les bornes. Le schéma complet
    reste publié tel quel pour les outils qui savent le lire.
    """
    erreurs = []
    if not isinstance(rec, dict):
        return False, ["l'enregistrement doit être un objet"]
    for champ in ("id", "type", "source", "status"):
        if not rec.get(champ):
            erreurs.append(f"champ obligatoire manquant : {champ}")
    if "status" in rec and rec["status"] not in STATUTS:
        erreurs.append(f"statut invalide : {rec['status']} (attendu : {', '.join(STATUTS)})")
    c = rec.get("confidence")
    if c is not None:
        try:
            if not 0 <= float(c) <= 1:
                erreurs.append("confiance hors bornes [0, 1]")
        except (TypeError, ValueError):
            erreurs.append("confiance doit être un nombre")
    for champ in ("valid_from", "valid_to", "observed_at", "retrieved_at"):
        v = rec.get(champ)
        if v and not re.match(r"^\d{4}-\d{2}-\d{2}", str(v)):
            erreurs.append(f"{champ} n'est pas une date ISO : {v}")
    return (not erreurs), erreurs


def geometrie_point(lon, lat) -> dict | None:
    try:
        return {"type": "Point", "coordinates": [float(lon), float(lat)]}
    except (TypeError, ValueError):
        return None


# ------------------------------------------------------------------ adaptateurs
# « Référencer l'existant » plutôt que recopier : chaque adaptateur traduit un
# objet métier vers la forme canonique. Le module garde ses propres champs à
# côté (dans `extra`), on ne perd rien.

def depuis_outil(o: dict, origine: str) -> dict:
    """Outil du registre (local ou Watchtower) → enregistrement canonique."""
    return enregistrement(
        identifiant=f"outil:{o.get('id') or re.sub(r'[^a-z0-9]+', '-', str(o.get('nom', '')).lower())}",
        type_="outil", source=origine,
        statut="fact" if o.get("statut") in ("present", "installé", None) else "unknown",
        label=o.get("nom") or o.get("id") or "",
        source_url=(o.get("urls") or [o.get("url")] or [None])[0] if (o.get("urls") or o.get("url")) else None,
        license=o.get("licence") or o.get("license"),
        provenance={"registre": origine, "mode": "référencement"},
        retrieved_at=o.get("maj_le") or maintenant(),
    )


def depuis_preuve(p: dict, cas_id: str) -> dict:
    return enregistrement(
        identifiant=f"preuve:{p.get('id')}",
        type_="preuve", source=f"osint:{cas_id}",
        statut=FIABILITE_OSINT.get(str(p.get("fiabilite") or "X").upper(), "unknown"),
        label=p.get("titre") or "",
        source_url=p.get("url") or None,
        observed_at=p.get("collecte_le") or None,
        retrieved_at=p.get("collecte_le") or None,
        confidence={"haute": 0.9, "moyenne": 0.6, "faible": 0.3}.get(p.get("confiance"), None),
        provenance={"outil": p.get("outil"), "collecte_par": p.get("collecte_par"),
                    "source_citee": p.get("source")},
    )


def depuis_decision(d: dict, reunion_id: str) -> dict:
    return enregistrement(
        identifiant=f"decision:{d.get('id')}",
        type_="decision", source=f"reunion:{reunion_id}",
        statut="fact", label=d.get("texte") or "",
        observed_at=d.get("cree_le") or None,
        provenance={"responsable": d.get("responsable"), "source": d.get("source")},
        relations=[{"type": "echeance", "valeur": d["echeance"]}] if d.get("echeance") else [],
    )


def depuis_action(a: dict, reunion_id: str) -> dict:
    return enregistrement(
        identifiant=f"action:{a.get('id')}",
        type_="action", source=f"reunion:{reunion_id}",
        statut="fact", label=a.get("texte") or "",
        valid_to=a.get("echeance") or None,
        provenance={"responsable": a.get("responsable"), "statut": a.get("statut")},
    )


def depuis_point(p: dict) -> dict:
    return enregistrement(
        identifiant=f"lieu:{p.get('id')}",
        type_="lieu", source="carto",
        statut="unknown" if p.get("etat") == "à vérifier" else "fact",
        label=p.get("nom") or "",
        geometry=geometrie_point(p.get("lon"), p.get("lat")),
        provenance={"commune": p.get("commune"), "source": p.get("source")},
    )


def depuis_profil(p: dict) -> dict:
    return enregistrement(
        identifiant=f"profil:{p.get('id')}",
        type_="profil", source="cognitorium",
        statut="fact" if p.get("verifie_le") else "unknown",
        label=f"{p.get('prenom', '')} {p.get('nom', '')}".strip() or p.get("structure") or "",
        provenance={"structure": p.get("structure"), "role": p.get("role"),
                    "commune": p.get("commune")},
    )


def depuis_indicateur(i: dict) -> dict:
    valeur = i.get("valeur")
    return enregistrement(
        identifiant=f"indicateur:{i.get('id')}",
        type_="indicateur", source=i.get("source") or "prevision",
        statut="fact" if valeur is not None else "unknown",
        label=i.get("nom") or "",
        source_url=i.get("url") or None,
        license=i.get("licence"),
        confidence={"haute": 0.9, "moyenne": 0.6, "faible": 0.3}.get(i.get("confiance")),
        retrieved_at=i.get("maj_le") or None,
        provenance={"famille": i.get("famille"), "unite": i.get("unite"), "valeur": valeur},
    )
