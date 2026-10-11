#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Valide le dataset climat canonique data/climat/el-nino-2026/el-nino-godzilla-2026.json.

Contrôles (stdlib uniquement) :
- JSON parseable, sections obligatoires présentes et non vides ;
- vocabulaires contrôlés : status ∈ {observe, prevu, incertain},
  attribution ∈ {el_nino, mixte, meteo_locale, rechauffement_fond, non_attribue} ;
- cohérence des références : source_ids / source_id des faits pointent vers des sources existantes ;
- geo.watchpoints : lat/lon dans les plages valides, ids uniques ;
- quiz : answer est un index valide de options ;
- learning : chaque niveau a choices, correct valide, concepts présents dans le graphe déclaré ;
- thau.timeline : ids uniques, horizons et risk_types couverts par timeline_filters.

Usage : python3 scripts/validate_climat_data.py [chemin.json]
Sortie : liste d'erreurs (exit 1) ou OK (exit 0).
"""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DEFAULT = BASE / "data" / "climat" / "el-nino-2026" / "el-nino-godzilla-2026.json"

STATUSES = {"observe", "prevu", "incertain"}
ATTRIBUTIONS = {"el_nino", "mixte", "meteo_locale", "rechauffement_fond", "non_attribue"}

REQUIRED_SECTIONS = [
    "meta", "key_message", "sources", "glossary", "mechanism", "indicators", "quotes",
    "global_facts", "projections", "scenarios", "effects_matrix", "second_order_risks",
    "prevention", "epistemics", "conclusions", "thau", "geo", "quiz", "learning",
]


def validate(path: Path) -> list:
    errors = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"JSON illisible : {e}"]

    # --- sections obligatoires
    for s in REQUIRED_SECTIONS:
        if s not in data:
            errors.append(f"section manquante : {s}")
        elif isinstance(data[s], (list, dict)) and not data[s]:
            errors.append(f"section vide : {s}")
    if errors:
        return errors

    source_ids = {s.get("id") for s in data["sources"]}
    if None in source_ids:
        errors.append("sources : une entrée n'a pas d'id")

    def check_refs(obj, where):
        for key in ("source_ids",):
            for ref in obj.get(key, []) or []:
                if ref not in source_ids:
                    errors.append(f"{where} : source_id inconnue « {ref} »")
        if "source_id" in obj and obj["source_id"]:
            if obj["source_id"] not in source_ids:
                errors.append(f"{where} : source_id inconnue « {obj['source_id']} »")

    # --- global_facts
    fact_ids = set()
    for f in data["global_facts"]:
        where = f"global_facts[{f.get('id', '?')}]"
        for k in ("id", "region", "title", "status", "attribution"):
            if not f.get(k):
                errors.append(f"{where} : champ « {k} » manquant")
        if f.get("id") in fact_ids:
            errors.append(f"{where} : id dupliqué")
        fact_ids.add(f.get("id"))
        if f.get("status") not in STATUSES:
            errors.append(f"{where} : status invalide « {f.get('status')} »")
        if f.get("attribution") not in ATTRIBUTIONS:
            errors.append(f"{where} : attribution invalide « {f.get('attribution')} »")
        check_refs(f, where)

    # --- thau
    thau = data["thau"]
    for k in ("scope", "timeline", "risks", "tools", "dashboard", "timeline_filters"):
        if not thau.get(k):
            errors.append(f"thau : section « {k} » manquante")
    horizons = {h["id"] for h in thau.get("timeline_filters", {}).get("horizons", [])}
    risk_types = {r["id"] for r in thau.get("timeline_filters", {}).get("risk_types", [])}
    phase_ids = set()
    for p in thau.get("timeline", []):
        where = f"thau.timeline[{p.get('id', '?')}]"
        for k in ("id", "phase", "period", "title", "status"):
            if p.get(k) in (None, ""):
                errors.append(f"{where} : champ « {k} » manquant")
        if p.get("id") in phase_ids:
            errors.append(f"{where} : id dupliqué")
        phase_ids.add(p.get("id"))
        if p.get("status") not in STATUSES:
            errors.append(f"{where} : status invalide « {p.get('status')} »")
        if p.get("horizon") and p["horizon"] not in horizons:
            errors.append(f"{where} : horizon inconnu « {p['horizon']} »")
        for rt in p.get("risk_types", []):
            if rt not in risk_types:
                errors.append(f"{where} : risk_type inconnu « {rt} »")
        check_refs(p, where)
    for lf in thau.get("local_facts", []):
        if lf.get("status") not in STATUSES:
            errors.append(f"thau.local_facts[{lf.get('id', '?')}] : status invalide")
        check_refs(lf, f"thau.local_facts[{lf.get('id', '?')}]")

    # --- geo
    seen = set()
    for w in data["geo"]["watchpoints"]:
        where = f"geo.watchpoints[{w.get('id', '?')}]"
        if w.get("id") in seen:
            errors.append(f"{where} : id dupliqué")
        seen.add(w.get("id"))
        if not (-90 <= w.get("lat", 999) <= 90):
            errors.append(f"{where} : lat hors plage")
        if not (-180 <= w.get("lon", 999) <= 180):
            errors.append(f"{where} : lon hors plage")
        if w.get("category") not in {"local", "global"}:
            errors.append(f"{where} : category invalide")

    # --- quiz
    for q in data["quiz"]:
        where = f"quiz[{q.get('id', '?')}]"
        opts = q.get("options") or []
        if len(opts) < 2:
            errors.append(f"{where} : moins de 2 options")
        if not (isinstance(q.get("answer"), int) and 0 <= q["answer"] < len(opts)):
            errors.append(f"{where} : answer invalide")

    # --- learning
    learn = data["learning"]
    graph = set(learn.get("concepts_graph", []))
    lvl_ids = set()
    for lvl in learn.get("levels", []):
        where = f"learning.levels[{lvl.get('id', '?')}]"
        if lvl.get("id") in lvl_ids:
            errors.append(f"{where} : id dupliqué")
        lvl_ids.add(lvl.get("id"))
        choices = lvl.get("choices") or []
        if len(choices) < 2:
            errors.append(f"{where} : moins de 2 choix")
        if not (isinstance(lvl.get("correct"), int) and 0 <= lvl["correct"] < len(choices)):
            errors.append(f"{where} : correct invalide")
        for c in lvl.get("concepts", []):
            if c not in graph:
                errors.append(f"{where} : concept « {c} » absent de concepts_graph")

    # --- projections (garde-fous sémantiques)
    mort = data["projections"].get("mortality", {})
    if mort.get("warning") and "PROJECTION" not in mort["warning"].upper():
        errors.append("projections.mortality : l'avertissement doit rappeler le statut PROJECTION")

    return errors


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT
    if not path.exists():
        print(f"✗ fichier introuvable : {path}")
        sys.exit(2)
    errors = validate(path)
    if errors:
        print(f"✗ {len(errors)} erreur(s) dans {path} :")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    data = json.loads(path.read_text(encoding="utf-8"))
    print(f"✓ dataset valide : {path.name} v{data['meta']['version']} (as_of {data['meta']['as_of']})")
    print(f"  {len(data['sources'])} sources · {len(data['global_facts'])} faits globaux · "
          f"{len(data['thau']['timeline'])} phases Thau · {len(data['geo']['watchpoints'])} watchpoints · "
          f"{len(data['quiz'])} quiz · {len(data['learning']['levels'])} niveaux learning")
    sys.exit(0)


if __name__ == "__main__":
    main()
