#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit les artefacts modules à partir des datasets climat canoniques.

Entrées (data/climat/*/) :
  - el-nino-2026/el-nino-godzilla-2026.json            (schema el-nino-thau-v1)
  - frontignan-episodes-cevenols/frontignan-cevenols-2026.json (schema territorial-risk-v1)

Sorties :
  1. projects/frontignan/el-nino-thau.html
     Module interactif autonome « Atlas Frontignan — El Niño × Thau »
     (9 onglets : vue d'ensemble, frise Thau filtrable, faits globaux, risques
     & scénarios, épisodes cévenols — blocages & solutions, simulation canvas,
     quiz, checklist prévention, sources). Embarque les DEUX datasets.
  2. projects/COGNITORIUM/learning/el-nino-poc.html
     PoC Cognitorium Learning Engine « Comprendre El Niño : du Pacifique au
     bassin de Thau » (10 niveaux, graphe de concepts, question de transfert).
  3. projects/watchtower/public/data/enso-thau-watchpoints.geojson
     Points de surveillance El Niño × Thau (15 watchpoints + boîte Niño 3.4).
  4. projects/watchtower/public/data/frontignan-cevenols-watchpoints.geojson
     Zones de blocage cévenols à Frontignan (indicatives, diagnostic documentaire).

Usage : python3 scripts/build_climat_assets.py [--check]
  --check : ne réécrit rien, vérifie que les artefacts sont à jour.
"""
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CLIMAT = BASE / "data" / "climat"

DATASETS = {
    "__ELNINO_DATA__": CLIMAT / "el-nino-2026" / "el-nino-godzilla-2026.json",
    "__CEVENOLS_DATA__": CLIMAT / "frontignan-episodes-cevenols" / "frontignan-cevenols-2026.json",
}

TEMPLATES = BASE / "scripts" / "templates" / "climat"
OUT_FRONTIGNAN = BASE / "projects" / "frontignan" / "el-nino-thau.html"
OUT_POC = BASE / "projects" / "COGNITORIUM" / "learning" / "el-nino-poc.html"
OUT_GEO_ENSO = BASE / "projects" / "watchtower" / "public" / "data" / "enso-thau-watchpoints.geojson"
OUT_GEO_CEV = BASE / "projects" / "watchtower" / "public" / "data" / "frontignan-cevenols-watchpoints.geojson"

PLACEHOLDER_RE = re.compile(r"__[A-Z]+_DATA__")


def safe_json_for_script(data) -> str:
    """JSON sûr à embarquer dans <script type="application/json">."""
    s = json.dumps(data, ensure_ascii=True)
    # empêche toute fermeture prématurée de la balise script
    return s.replace("</", "<\\/")


def load_datasets() -> dict:
    out = {}
    for ph, path in DATASETS.items():
        if not path.exists():
            print(f"✗ dataset introuvable : {path}")
            sys.exit(2)
        out[ph] = json.loads(path.read_text(encoding="utf-8"))
    return out


def render(template_path: Path, datasets: dict) -> str:
    tpl = template_path.read_text(encoding="utf-8")
    for ph, data in datasets.items():
        if ph in tpl:
            tpl = tpl.replace(ph, safe_json_for_script(data))
    leftover = PLACEHOLDER_RE.search(tpl)
    if leftover:
        raise RuntimeError(f"{template_path.name} : marqueur non résolu {leftover.group(0)}")
    return tpl


def build_geojson(data, extra_note: str = "") -> dict:
    meta = data["meta"]
    features = []
    for w in data["geo"]["watchpoints"]:
        props = {
            "name": w["name"],
            "category": w.get("category", "local"),
            "description": w.get("description", ""),
            "dataset": meta["id"],
            "dataset_version": meta["version"],
            "as_of": meta["as_of"],
        }
        for k in ("scope", "status", "status_label", "blocking_point_ids"):
            if w.get(k):
                props[k] = w[k]
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [round(w["lon"], 4), round(w["lat"], 4)]},
            "properties": props,
        })
    return {
        "type": "FeatureCollection",
        "name": f"{meta['id']} watchpoints (v{meta['version']}, as_of {meta['as_of']})",
        "metadata": {
            "title": meta["title"],
            "generated_by": "scripts/build_climat_assets.py",
            "source_dataset": str(next(iter(DATASETS.values())).relative_to(BASE)) if not extra_note else extra_note,
            "origin": meta.get("origin", {}),
            "disclaimer": meta.get("disclaimer", ""),
            "usage": "Glisser-déposer ce fichier sur le globe watchtower (import GeoJSON natif du fork), ou le servir via /preview/watchtower/public/data/.",
        },
        "features": features,
    }


def build_enso_geojson(data) -> dict:
    """Watchpoints El Niño × Thau + boîte de la zone Niño 3.4 en polygone."""
    geo = build_geojson(data)
    meta = data["meta"]
    status_label = {"observe": "observé / rapporté", "prevu": "prévu / projection", "incertain": "incertain / hypothèse"}
    for f in geo["features"]:
        st = f["properties"].get("status", "")
        if st and "status_label" not in f["properties"]:
            f["properties"]["status_label"] = status_label.get(st, st)
    geo["metadata"]["source_dataset"] = "data/climat/el-nino-2026/el-nino-godzilla-2026.json"
    geo["features"].append({
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[-170.0, 5.0], [-120.0, 5.0], [-120.0, -5.0], [-170.0, -5.0], [-170.0, 5.0]]],
        },
        "properties": {
            "name": "Zone Niño 3.4 (5°N–5°S · 120°–170°W)",
            "category": "global",
            "scope": "pacifique",
            "status": "observe",
            "status_label": "observé / rapporté",
            "description": "Zone de mesure de l'indice Niño 3.4 : +3,07 °C le 22/09/2026 (record 2015 égalé avec ~2 mois d'avance) ; RONI été 2026 : +1,4 °C (« El Niño moins le réchauffement de fond »).",
            "dataset": meta["id"],
            "dataset_version": meta["version"],
            "as_of": meta["as_of"],
        },
    })
    return geo


def build_cev_geojson(data) -> dict:
    geo = build_geojson(data, extra_note="data/climat/frontignan-episodes-cevenols/frontignan-cevenols-2026.json")
    geo["metadata"]["title"] = "Frontignan face aux épisodes cévenols — zones de blocage (indicatives)"
    geo["metadata"]["usage"] = ("Glisser-déposer ce fichier sur le globe watchtower (import GeoJSON natif du fork). "
                                "Localisations indicatives issues d'un diagnostic documentaire (PCS 2025, PPRI, SMBT, PAPI) — "
                                "ce n'est pas une étude hydraulique.")
    return geo


def main():
    check_only = "--check" in sys.argv
    datasets = load_datasets()
    elnino = datasets["__ELNINO_DATA__"]
    cevenols = datasets["__CEVENOLS_DATA__"]

    outputs_html = [
        (TEMPLATES / "frontignan-module.html.tmpl", OUT_FRONTIGNAN, "module Atlas Frontignan (El Niño × Thau + cévenols)"),
        (TEMPLATES / "cognitorium-poc.html.tmpl", OUT_POC, "PoC Cognitorium"),
    ]
    ok = True
    for tpl_path, out_path, label in outputs_html:
        html = render(tpl_path, datasets)
        if check_only:
            current = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
            fresh = current == html
            print(f"{'✓' if fresh else '✗'} {label} : {out_path.relative_to(BASE)} {'à jour' if fresh else 'PÉRIMÉ — relance build_climat_assets.py'}")
            ok = ok and fresh
        else:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(html, encoding="utf-8")
            print(f"✓ {label} → {out_path.relative_to(BASE)} ({out_path.stat().st_size // 1024} Ko)")

    geo_outputs = [
        (build_enso_geojson(elnino), OUT_GEO_ENSO, "watchpoints GeoJSON El Niño × Thau"),
        (build_cev_geojson(cevenols), OUT_GEO_CEV, "watchpoints GeoJSON cévenols Frontignan"),
    ]
    for geo, out_path, label in geo_outputs:
        geo_txt = json.dumps(geo, ensure_ascii=False, indent=1) + "\n"
        if check_only:
            current = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
            fresh = current == geo_txt
            print(f"{'✓' if fresh else '✗'} {label} : {out_path.relative_to(BASE)} {'à jour' if fresh else 'PÉRIMÉ — relance build_climat_assets.py'}")
            ok = ok and fresh
        else:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(geo_txt, encoding="utf-8")
            print(f"✓ {label} → {out_path.relative_to(BASE)} ({len(geo['features'])} features, {out_path.stat().st_size // 1024} Ko)")

    if check_only:
        sys.exit(0 if ok else 1)
    print(f"\nDatasets sources :")
    for ph, path in DATASETS.items():
        d = datasets[ph]
        print(f"  - {path.relative_to(BASE)} (v{d['meta']['version']}, as_of {d['meta']['as_of']})")
    print("Rappel : les artefacts générés ne s'éditent pas à la main — modifier le JSON puis relancer ce script.")


if __name__ == "__main__":
    main()
