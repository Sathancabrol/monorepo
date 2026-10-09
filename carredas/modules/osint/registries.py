# -*- coding: utf-8 -*-
"""Registres d'outils : référencer l'existant plutôt que le recopier.

Le monorepo contient déjà un registre d'outils de référence :
`projects/watchtower/audit/reference/REGISTRE-OUTILS.json` — 86 outils, 25
besoins, 12 catégories, avec rôle, commande d'installation, licence, GPU requis
et références d'origine.

La règle d'intégration du projet est explicite : **référencer d'abord**, adapter
ensuite, n'extraire qu'en dernier. Ce module applique donc cette règle : il lit
le registre Watchtower là où il est, le normalise à la forme du registre local,
et sert les deux ensemble. Aucune copie, aucune divergence possible.

Le registre local (France d'abord : Annuaire des Entreprises, Pappers, JOAFE,
INPI, DVF…) reste utile parce qu'il couvre un autre terrain : les sources
ouvertes administratives françaises, que Watchtower ne traite pas.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

RACINE_DEPOT = Path(__file__).resolve().parents[3]

CHEMIN_PAR_DEFAUT = "projects/watchtower/audit/reference/REGISTRE-OUTILS.json"

# Catégories Watchtower → risque. « 3 · OSINT infrastructures » et
# « 7 · Agents » sont les seules à interroger des tiers.
RISQUE_PAR_CATEGORIE = {
    "0": "passif", "1": "passif", "2": "passif", "3": "actif",
    "4": "passif", "4b": "passif", "5": "passif", "6": "passif",
    "7": "actif", "8": "passif", "9": "passif", "10": "passif",
}


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", str(s or "").lower()).strip("-") or "x"


def numero_categorie(cat: str) -> str:
    """« 4b · Positionnement spatial (VPS)… » → « 4b »."""
    return str(cat or "").split("·")[0].strip() or "?"


def chemin_registre(config: dict | None = None) -> Path | None:
    """Chemin du registre Watchtower, tel que configuré (ou par défaut)."""
    cfg = (config or {}).get("osint") or {}
    brut = cfg.get("registre_watchtower", CHEMIN_PAR_DEFAUT)
    if not brut:
        return None
    p = Path(brut)
    if not p.is_absolute():
        p = RACINE_DEPOT / p
    return p if p.exists() else None


def charger_watchtower(config: dict | None = None) -> dict | None:
    """Charge le registre Watchtower. Rend None si absent ou illisible."""
    p = chemin_registre(config)
    if not p:
        return None
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(d, dict) or not isinstance(d.get("outils"), list):
        return None
    d["_chemin"] = str(p)
    return d


def normaliser_outil_watchtower(o: dict) -> dict:
    """Forme Watchtower → forme du registre unifié."""
    cat = str(o.get("cat") or "")
    num = numero_categorie(cat)
    urls = o.get("urls") or []
    install = o.get("install") or []
    return {
        "id": "wt-" + str(o.get("id") or _slug(o.get("nom", ""))),
        "categorie": "wt-" + _slug(num),
        "categorie_nom": cat,
        "type": _deviner_type(install, o),
        "risque": RISQUE_PAR_CATEGORIE.get(num, "passif"),
        "nom": o.get("nom") or o.get("id") or "—",
        "licence": o.get("licence") or "à vérifier",
        "etoiles": None,
        "description": o.get("role") or "",
        "usage": o.get("notes") or "",
        "url": urls[0] if urls else "",
        "urls": urls,
        "install": install[0] if install else "",
        "verifier": o.get("verifier") or "",
        "gpu": o.get("gpu") or "",
        "prix": o.get("prix") or "",
        "statut_outil": o.get("statut") or "",
        "integree": o.get("integree") or "",
        "origine": o.get("origine") or {},
        "registre": "watchtower",
    }


def _deviner_type(install: list, o: dict) -> str:
    blob = " ".join(str(x) for x in install).lower()
    if "docker" in blob:
        return "service"
    if any(m in blob for m in ("winget", "pip ", "pipx", "npm", "choco", "apt ", "binaire")):
        return "cli"
    if o.get("urls"):
        return "web"
    return "bibliotheque"


def categories_watchtower(d: dict) -> list[dict]:
    """Les catégories Watchtower, sous la forme attendue par l'interface."""
    out = []
    for c in (d.get("categories") or []):
        num = numero_categorie(c)
        out.append({
            "id": "wt-" + _slug(num),
            "nom": str(c),
            "icone": "▤",
            "ordre": 100 + (int(num) if num.isdigit() else 90),
            "registre": "watchtower",
            "note": "Registre Watchtower — référencé, non dupliqué.",
        })
    return out


def besoins_watchtower(d: dict) -> list[dict]:
    """Les « besoins → outils » : l'entrée la plus utile du registre."""
    out = []
    for b in (d.get("besoins") or []):
        out.append({
            "besoin": b.get("besoin") or "",
            "outils": ["wt-" + str(x) for x in (b.get("outils") or [])],
            "note": b.get("note") or "",
        })
    return out


def fusionner(local: dict, wt: dict | None) -> dict:
    """Registre unifié : catégories locales + Watchtower, outils et besoins."""
    categories = list(local.get("categories") or [])
    outils = [dict(o, registre="local") for o in (local.get("outils") or [])]
    besoins = []
    registres = [{"id": "local", "nom": "Sources ouvertes France",
                  "outils": len(outils), "registre": "local"}]
    if wt:
        wt_outils = [normaliser_outil_watchtower(o) for o in (wt.get("outils") or [])]
        outils += wt_outils
        categories += categories_watchtower(wt)
        besoins = besoins_watchtower(wt)
        registres.append({
            "id": "watchtower",
            "nom": "Registre Watchtower",
            "outils": len(wt_outils),
            "chemin": wt.get("_chemin") or "",
            "genere_le": wt.get("genere_le") or "",
            "version": wt.get("version"),
            "registre": "watchtower",
        })
    return {
        "categories": categories,
        "outils": outils,
        "besoins": besoins,
        "registres": registres,
        "meta": dict(local.get("meta") or {}),
        "legende": (wt or {}).get("legende") or {},
    }
