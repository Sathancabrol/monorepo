#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Valide la spec canonique de la console Atlas Frontignan (schéma atlas-frontignan-v1).

Contrôles :
  - sections obligatoires, meta.schema/id/version/as_of ;
  - statuts : exactement EMPTY → SHELL → DATA → LIVE → SIM, ids uniques ;
  - modes : ids uniques, statut valide, layers avec statut valide, ≥ 10 modes ;
  - modules : ids uniques, sous-modules avec statut valide, modes référencés existants ;
  - actions : ids uniques, module existant, prérequis existants, effets → indicateurs
    existants avec basis ∈ {placeholder, documenté}, map_object existant ;
  - indicateurs : ids uniques, direction ∈ {higher, lower}, baseline numérique ou null ;
  - unités : kinds utilisés par map.objects déclarés ;
  - map.objects : ids uniques, modes ⊆ modes déclarés (ou « * »), statut valide,
    lat/lon dans la projection, data_link → dataset déclaré ET watchpoint existant
    dans le JSON canonique correspondant (chargé depuis data/climat/) ;
  - overlays / phases / data_sources / links / sources : ids uniques, champs clés.

Usage :
  python3 scripts/validate_atlas_spec.py              # valide data/atlas-frontignan/*.json
  python3 scripts/validate_atlas_spec.py <chemin.json>
"""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ATLAS_DIR = BASE / "data" / "atlas-frontignan"
CLIMAT_DIR = BASE / "data" / "climat"

STATUSES = ["EMPTY", "SHELL", "DATA", "LIVE", "SIM"]
DIRECTIONS = {"higher", "lower"}
BASES = {"placeholder", "documenté"}

# datasets canoniques climats → chemin (pour résoudre les data_link)
DATASET_PATHS = {
    "frontignan-cevenols-2026": CLIMAT_DIR / "frontignan-episodes-cevenols" / "frontignan-cevenols-2026.json",
    "el-nino-godzilla-2026": CLIMAT_DIR / "el-nino-2026" / "el-nino-godzilla-2026.json",
}


def validate(path: Path) -> list:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"JSON illisible : {e}"]

    errors = []
    for s in ("meta", "key_message", "statuses", "modes", "modules", "actions",
              "indicators", "units", "overlays", "map", "phases", "data_sources",
              "links", "sources"):
        if s not in data:
            errors.append(f"section manquante : {s}")
    if errors:
        return errors

    m = data["meta"]
    if m.get("schema") != "atlas-frontignan-v1":
        errors.append(f"meta.schema = « {m.get('schema')} » (attendu : atlas-frontignan-v1)")
    for k in ("id", "version", "as_of", "disclaimer"):
        if not m.get(k):
            errors.append(f"meta : champ « {k} » manquant")

    # ── statuts
    st_ids = [s.get("id") for s in data["statuses"]]
    if st_ids != STATUSES:
        errors.append(f"statuts = {st_ids} (attendu : {STATUSES})")
    for s in data["statuses"]:
        for k in ("label", "color", "meaning"):
            if not s.get(k):
                errors.append(f"statut {s.get('id')} : champ « {k} » manquant")
    ST = set(st_ids)

    # ── modes
    mode_ids = set()
    if len(data["modes"]) < 10:
        errors.append(f"modes : {len(data['modes'])} seulement (≥ 10 attendus — placeholder complet)")
    for mo in data["modes"]:
        where = f"modes[{mo.get('id', '?')}]"
        if mo.get("id") in mode_ids:
            errors.append(f"{where} : id dupliqué")
        mode_ids.add(mo.get("id"))
        for k in ("icon", "name", "question", "status", "note"):
            if not mo.get(k):
                errors.append(f"{where} : champ « {k} » manquant")
        if mo.get("status") not in ST:
            errors.append(f"{where} : status invalide « {mo.get('status')} »")
        if not mo.get("layers"):
            errors.append(f"{where} : aucune couche déclarée")
        for ly in mo.get("layers", []):
            if not ly.get("name"):
                errors.append(f"{where} : couche sans nom")
            if ly.get("status") not in ST:
                errors.append(f"{where} : couche « {ly.get('name')} » status invalide « {ly.get('status')} »")

    # ── modules
    module_ids = set()
    for mo in data["modules"]:
        where = f"modules[{mo.get('id', '?')}]"
        if mo.get("id") in module_ids:
            errors.append(f"{where} : id dupliqué")
        module_ids.add(mo.get("id"))
        for k in ("icon", "name", "color", "status"):
            if not mo.get(k):
                errors.append(f"{where} : champ « {k} » manquant")
        if mo.get("status") not in ST:
            errors.append(f"{where} : status invalide")
        for mm in mo.get("modes", []):
            if mm not in mode_ids:
                errors.append(f"{where} : mode lié inconnu « {mm} »")
        for sm in mo.get("submodules", []):
            if not sm.get("id") or not sm.get("name"):
                errors.append(f"{where} : sous-module sans id/name")
            if sm.get("status") not in ST:
                errors.append(f"{where}.submodules[{sm.get('id', '?')}] : status invalide « {sm.get('status')} »")

    # ── indicateurs
    ind_ids = set()
    for ind in data["indicators"]:
        where = f"indicators[{ind.get('id', '?')}]"
        if ind.get("id") in ind_ids:
            errors.append(f"{where} : id dupliqué")
        ind_ids.add(ind.get("id"))
        for k in ("icon", "name", "unit", "direction", "status", "baseline_basis"):
            if not ind.get(k):
                errors.append(f"{where} : champ « {k} » manquant")
        if ind.get("direction") not in DIRECTIONS:
            errors.append(f"{where} : direction invalide « {ind.get('direction')} »")
        if ind.get("status") not in ST:
            errors.append(f"{where} : status invalide")
        b = ind.get("baseline")
        if b is not None and not isinstance(b, (int, float)):
            errors.append(f"{where} : baseline doit être numérique ou null")

    # ── actions
    act_ids = set()
    for a in data["actions"]:
        where = f"actions[{a.get('id', '?')}]"
        if a.get("id") in act_ids:
            errors.append(f"{where} : id dupliqué")
        act_ids.add(a.get("id"))
        for k in ("name", "module", "cost", "cost_basis", "delay", "status"):
            if not a.get(k):
                errors.append(f"{where} : champ « {k} » manquant")
        if a.get("module") not in module_ids:
            errors.append(f"{where} : module inconnu « {a.get('module')} »")
        if a.get("status") not in ST:
            errors.append(f"{where} : status invalide")
        if a.get("cost_basis") not in BASES:
            errors.append(f"{where} : cost_basis invalide « {a.get('cost_basis')} »")
        for pr in a.get("prereqs", []):
            if pr not in act_ids and pr not in {x.get("id") for x in data["actions"]}:
                errors.append(f"{where} : prérequis inconnu « {pr} »")
        if not a.get("effects"):
            errors.append(f"{where} : aucun effet déclaré")
        for ef in a.get("effects", []):
            if ef.get("indicator") not in ind_ids:
                errors.append(f"{where} : effet vers indicateur inconnu « {ef.get('indicator')} »")
            if ef.get("basis") not in BASES:
                errors.append(f"{where} : effet basis invalide « {ef.get('basis')} »")
            if not isinstance(ef.get("delta"), (int, float)):
                errors.append(f"{where} : delta non numérique")
        if a.get("map_object") and a["map_object"] not in {o.get("id") for o in data["map"]["objects"]}:
            errors.append(f"{where} : map_object inconnu « {a['map_object']} »")
        if a.get("source_id") and a["source_id"] not in {s.get("id") for s in data["sources"]}:
            errors.append(f"{where} : source_id inconnu « {a['source_id']} »")

    # ── unités
    unit_ids = {u.get("id") for u in data["units"]}
    for u in data["units"]:
        for k in ("name", "desc", "examples"):
            if not u.get(k):
                errors.append(f"units[{u.get('id', '?')}] : champ « {k} » manquant")

    # ── overlays / phases / data_sources / links / sources
    for sec in ("overlays", "phases", "data_sources", "links", "sources"):
        seen = set()
        for item in data[sec]:
            iid = item.get("id") or item.get("label")
            if not iid:
                errors.append(f"{sec} : entrée sans id/label")
                continue
            if iid in seen:
                errors.append(f"{sec} : id/label dupliqué « {iid} »")
            seen.add(iid)
    for ph in data["phases"]:
        if ph.get("state") not in {"livré", "prévu"}:
            errors.append(f"phases[{ph.get('id', '?')}] : state invalide « {ph.get('state')} »")
        if not ph.get("deliverables"):
            errors.append(f"phases[{ph.get('id', '?')}] : aucun livrable déclaré")
    for ds in data["data_sources"]:
        if ds.get("status") not in ST:
            errors.append(f"data_sources[{ds.get('id', '?')}] : status invalide")
        if ds.get("phase") and ds["phase"] not in {p.get("id") for p in data["phases"]}:
            errors.append(f"data_sources[{ds.get('id', '?')}] : phase inconnue « {ds['phase']} »")

    # ── carte
    proj = data["map"].get("projection", {})
    for k in ("lon_min", "lon_max", "lat_min", "lat_max", "width", "height"):
        if k not in proj:
            errors.append(f"map.projection : champ « {k} » manquant")
    obj_ids = set()
    obj_by_id = {}
    for o in data["map"]["objects"]:
        where = f"map.objects[{o.get('id', '?')}]"
        if o.get("id") in obj_ids:
            errors.append(f"{where} : id dupliqué")
        obj_ids.add(o.get("id"))
        obj_by_id[o.get("id")] = o
        for k in ("kind", "name", "status", "desc"):
            if not o.get(k):
                errors.append(f"{where} : champ « {k} » manquant")
        if o.get("kind") not in unit_ids:
            errors.append(f"{where} : kind inconnu « {o.get('kind')} »")
        if o.get("status") not in ST:
            errors.append(f"{where} : status invalide « {o.get('status')} »")
        for mm in o.get("modes", []):
            if mm != "*" and mm not in mode_ids:
                errors.append(f"{where} : mode inconnu « {mm} »")
        if "lat" in o or "lon" in o:
            lat, lon = o.get("lat"), o.get("lon")
            if lat is None or lon is None:
                errors.append(f"{where} : lat/lon incomplets")
            else:
                if not (proj.get("lat_min", 0) <= lat <= proj.get("lat_max", 90)):
                    errors.append(f"{where} : lat {lat} hors projection")
                if not (proj.get("lon_min", -180) <= lon <= proj.get("lon_max", 180)):
                    errors.append(f"{where} : lon {lon} hors projection")
        dl = o.get("data_link")
        if dl:
            ds_id = dl.get("dataset")
            if ds_id not in DATASET_PATHS:
                errors.append(f"{where} : data_link dataset inconnu « {ds_id} »")
            elif ds_id not in (m.get("related_datasets") or []):
                errors.append(f"{where} : data_link dataset « {ds_id} » absent de meta.related_datasets")
            else:
                dpath = DATASET_PATHS[ds_id]
                if not dpath.exists():
                    errors.append(f"{where} : fichier dataset introuvable {dpath.relative_to(BASE)}")
                else:
                    ddata = json.loads(dpath.read_text(encoding="utf-8"))
                    wps = {w.get("id") for w in ddata.get("geo", {}).get("watchpoints", [])}
                    if dl.get("watchpoint") not in wps:
                        errors.append(f"{where} : watchpoint « {dl.get('watchpoint')} » absent de {ds_id}")

    # ── key_message
    km = data["key_message"]
    for k in ("headline", "one_liner", "fil_rouge", "method_steps", "vigilance"):
        if not km.get(k):
            errors.append(f"key_message : champ « {k} » manquant")

    return errors


def main():
    if len(sys.argv) > 1:
        paths = [Path(sys.argv[1])]
    else:
        paths = sorted(ATLAS_DIR.glob("*.json")) if ATLAS_DIR.exists() else []
    if not paths:
        print("✗ aucune spec trouvée dans data/atlas-frontignan/")
        sys.exit(2)

    total = 0
    for path in paths:
        errors = validate(path)
        if errors:
            total += len(errors)
            print(f"✗ {len(errors)} erreur(s) dans {path.relative_to(BASE)} :")
            for e in errors:
                print("  -", e)
        else:
            d = json.loads(path.read_text(encoding="utf-8"))
            n_obj = len(d["map"]["objects"])
            n_link = sum(1 for o in d["map"]["objects"] if o.get("data_link"))
            n_ghost = sum(1 for a in d["actions"] if a.get("map_preview"))
            print(f"✓ spec valide [atlas-frontignan-v1] : {path.name} v{d['meta']['version']} (as_of {d['meta']['as_of']})"
                  f" · {len(d['modes'])} modes · {len(d['modules'])} modules ({sum(len(m['submodules']) for m in d['modules'])} sous-modules)"
                  f" · {len(d['actions'])} actions ({n_ghost} preview carte) · {len(d['indicators'])} indicateurs"
                  f" · {n_obj} objets carte ({n_link} branchés DATA) · {len(d['phases'])} phases · {len(d['data_sources'])} sources de données")
    if total:
        print(f"\n✗ {total} erreur(s) au total")
        sys.exit(1)
    print("\n✓ spec Atlas cohérente (refs modes/modules/actions/indicateurs/data_link vérifiées)")


if __name__ == "__main__":
    main()
