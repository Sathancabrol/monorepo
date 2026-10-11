#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Valide les datasets climat canoniques de data/climat/*/.

Chaque dataset porte meta.schema ; le contrôle est dispatché par schéma :

- « el-nino-thau-v1 » (data/climat/el-nino-2026/) :
  sections obligatoires, vocabulaires status/attribution, références source_ids,
  thau.timeline (horizons/risk_types couverts par timeline_filters), geo.watchpoints,
  quiz (answer valide), learning (correct valide, concepts dans le graphe déclaré).

- « territorial-risk-v1 » (data/climat/frontignan-episodes-cevenols/) :
  blocking_points (ids uniques, mécanisme + blocage, refs sources),
  solutions.matrix (priorité/verbe/solution/application + PAPI), atlas_opportunities,
  pilot.steps (done booléen), geo.watchpoints (lat/lon valides).

Usage :
  python3 scripts/validate_climat_data.py              # valide TOUS les datasets data/climat/*/*.json
  python3 scripts/validate_climat_data.py <chemin.json>  # valide un seul fichier
Sortie : liste d'erreurs (exit 1) ou OK (exit 0).
"""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CLIMAT_DIR = BASE / "data" / "climat"

STATUSES = {"observe", "prevu", "incertain"}
ATTRIBUTIONS = {"el_nino", "mixte", "meteo_locale", "rechauffement_fond", "non_attribue"}

SCHEMA_EL_NINO = "el-nino-thau-v1"
SCHEMA_RISK = "territorial-risk-v1"


# ────────────────────────────────────────────── schéma el-nino-thau-v1
def validate_el_nino(data: dict) -> list:
    errors = []
    required = [
        "meta", "key_message", "sources", "glossary", "mechanism", "indicators", "quotes",
        "global_facts", "projections", "scenarios", "effects_matrix", "second_order_risks",
        "prevention", "epistemics", "conclusions", "thau", "geo", "quiz", "learning",
    ]
    for s in required:
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
        for ref in obj.get("source_ids", []) or []:
            if ref not in source_ids:
                errors.append(f"{where} : source_id inconnue « {ref} »")
        if obj.get("source_id") and obj["source_id"] not in source_ids:
            errors.append(f"{where} : source_id inconnue « {obj['source_id']} »")

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

    errors.extend(check_geo(data["geo"]))

    for q in data["quiz"]:
        where = f"quiz[{q.get('id', '?')}]"
        opts = q.get("options") or []
        if len(opts) < 2:
            errors.append(f"{where} : moins de 2 options")
        if not (isinstance(q.get("answer"), int) and 0 <= q["answer"] < len(opts)):
            errors.append(f"{where} : answer invalide")

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

    mort = data["projections"].get("mortality", {})
    if mort.get("warning") and "PROJECTION" not in mort["warning"].upper():
        errors.append("projections.mortality : l'avertissement doit rappeler le statut PROJECTION")
    return errors


# ────────────────────────────────────────────── schéma territorial-risk-v1
def validate_territorial_risk(data: dict) -> list:
    errors = []
    required = ["meta", "key_message", "sources", "blocking_points", "solutions", "atlas_opportunities", "pilot", "geo"]
    for s in required:
        if s not in data:
            errors.append(f"section manquante : {s}")
        elif isinstance(data[s], (list, dict)) and not data[s]:
            errors.append(f"section vide : {s}")
    if errors:
        return errors

    source_ids = {s.get("id") for s in data["sources"]}
    if None in source_ids:
        errors.append("sources : une entrée n'a pas d'id")

    for k in ("headline", "diagnosis", "conclusion"):
        if not data["key_message"].get(k):
            errors.append(f"key_message : champ « {k} » manquant")

    bp_ids = set()
    for bp in data["blocking_points"]:
        where = f"blocking_points[{bp.get('id', '?')}]"
        for k in ("id", "n", "title", "mechanism", "blockage"):
            if bp.get(k) in (None, ""):
                errors.append(f"{where} : champ « {k} » manquant")
        if bp.get("id") in bp_ids:
            errors.append(f"{where} : id dupliqué")
        bp_ids.add(bp.get("id"))
        if not isinstance(bp.get("n"), int):
            errors.append(f"{where} : n doit être un entier")
        for ref in bp.get("source_ids", []) or []:
            if ref not in source_ids:
                errors.append(f"{where} : source_id inconnue « {ref} »")

    sol = data["solutions"]
    if not sol.get("principle"):
        errors.append("solutions : « principle » manquant")
    if not isinstance(sol.get("matrix"), list) or not sol["matrix"]:
        errors.append("solutions : « matrix » manquant ou vide")
    else:
        for i, s in enumerate(sol["matrix"]):
            where = f"solutions.matrix[{i}]"
            for k in ("priority", "verb", "solution", "application"):
                if not s.get(k):
                    errors.append(f"{where} : champ « {k} » manquant")
            if s.get("source_id") and s["source_id"] not in source_ids:
                errors.append(f"{where} : source_id inconnue « {s['source_id']} »")
    papi = sol.get("papi")
    if not isinstance(papi, dict):
        errors.append("solutions : « papi » manquant")
    else:
        for k in ("name", "actions", "communes", "budget_millions", "point_a_verifier"):
            if k not in papi:
                errors.append(f"solutions.papi : champ « {k} » manquant")
        if papi.get("source_id") and papi["source_id"] not in source_ids:
            errors.append("solutions.papi : source_id inconnue")

    ao = data["atlas_opportunities"]
    if not ao.get("intro"):
        errors.append("atlas_opportunities : « intro » manquant")
    if not isinstance(ao.get("modules"), list) or not ao["modules"]:
        errors.append("atlas_opportunities : « modules » manquant ou vide")
    else:
        mod_ids = set()
        for m in ao["modules"]:
            where = f"atlas_opportunities.modules[{m.get('id', '?')}]"
            for k in ("id", "name", "status", "description", "rule"):
                if not m.get(k):
                    errors.append(f"{where} : champ « {k} » manquant")
            if m.get("id") in mod_ids:
                errors.append(f"{where} : id dupliqué")
            mod_ids.add(m.get("id"))

    pil = data["pilot"]
    if not pil.get("recommendation"):
        errors.append("pilot : « recommendation » manquant")
    if not isinstance(pil.get("steps"), list) or not pil["steps"]:
        errors.append("pilot : « steps » manquant ou vide")
    else:
        for i, s in enumerate(pil["steps"]):
            where = f"pilot.steps[{i}]"
            if not isinstance(s.get("done"), bool):
                errors.append(f"{where} : « done » doit être un booléen")
            if not s.get("title") or not s.get("detail"):
                errors.append(f"{where} : title/detail manquant")
    if not isinstance(pil.get("sources_to_exploit"), list) or not pil["sources_to_exploit"]:
        errors.append("pilot : « sources_to_exploit » manquant ou vide")

    errors.extend(check_geo(data["geo"]))
    return errors


# ────────────────────────────────────────────── commun
def check_geo(geo: dict) -> list:
    errors = []
    seen = set()
    for w in geo.get("watchpoints", []):
        where = f"geo.watchpoints[{w.get('id', '?')}]"
        if w.get("id") in seen:
            errors.append(f"{where} : id dupliqué")
        seen.add(w.get("id"))
        if not (-90 <= w.get("lat", 999) <= 90):
            errors.append(f"{where} : lat hors plage")
        if not (-180 <= w.get("lon", 999) <= 180):
            errors.append(f"{where} : lon hors plage")
    return errors


SCHEMAS = {
    SCHEMA_EL_NINO: validate_el_nino,
    SCHEMA_RISK: validate_territorial_risk,
}


def validate(path: Path) -> list:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"JSON illisible : {e}"]
    schema = (data.get("meta") or {}).get("schema")
    if not schema:
        return ["meta.schema manquant (schémas connus : " + ", ".join(SCHEMAS) + ")"]
    fn = SCHEMAS.get(schema)
    if fn is None:
        return [f"meta.schema inconnu « {schema} » (connus : " + ", ".join(SCHEMAS) + ")"]
    return fn(data)


def main():
    if len(sys.argv) > 1:
        paths = [Path(sys.argv[1])]
    else:
        paths = sorted(CLIMAT_DIR.glob("*/*.json")) if CLIMAT_DIR.exists() else []
    if not paths:
        print("✗ aucun dataset trouvé dans data/climat/*/")
        sys.exit(2)

    total_errors = 0
    for path in paths:
        errors = validate(path)
        if errors:
            total_errors += len(errors)
            print(f"✗ {len(errors)} erreur(s) dans {path.relative_to(BASE)} :")
            for e in errors:
                print("  -", e)
        else:
            data = json.loads(path.read_text(encoding="utf-8"))
            extra = ""
            if data["meta"]["schema"] == SCHEMA_EL_NINO:
                extra = (f" · {len(data['sources'])} sources · {len(data['global_facts'])} faits globaux · "
                         f"{len(data['thau']['timeline'])} phases Thau · {len(data['geo']['watchpoints'])} watchpoints · "
                         f"{len(data['quiz'])} quiz · {len(data['learning']['levels'])} niveaux learning")
            else:
                extra = (f" · {len(data['sources'])} sources · {len(data['blocking_points'])} blocages · "
                         f"{len(data['solutions']['matrix'])} solutions · {len(data['atlas_opportunities']['modules'])} modules Atlas · "
                         f"{len(data['pilot']['steps'])} étapes pilote · {len(data['geo']['watchpoints'])} watchpoints")
            print(f"✓ dataset valide [{data['meta']['schema']}] : {path.name} v{data['meta']['version']} (as_of {data['meta']['as_of']}){extra}")

    if total_errors:
        print(f"\n✗ {total_errors} erreur(s) au total")
        sys.exit(1)
    print(f"\n✓ {len(paths)} dataset(s) valide(s)")


if __name__ == "__main__":
    main()
