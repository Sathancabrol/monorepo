#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit les artefacts modules à partir du dataset climat canonique.

Entrée  : data/climat/el-nino-2026/el-nino-godzilla-2026.json
Sorties :
  1. projects/frontignan/el-nino-thau.html
     Module interactif autonome « Atlas Frontignan — El Niño × Thau »
     (onglets : vue d'ensemble, frise filtrable, faits globaux, risques &
     scénarios, mini-simulation canvas, quiz, checklist prévention, sources).
  2. projects/COGNITORIUM/learning/el-nino-poc.html
     PoC Cognitorium Learning Engine « Comprendre El Niño : du Pacifique au
     bassin de Thau » (10 niveaux, graphe de concepts, compréhension,
     question de transfert) — même architecture que le PoC argent.
  3. projects/watchtower/public/data/enso-thau-watchpoints.geojson
     Points de surveillance (15 : 6 Thau + 9 mondiaux) + boîte de la zone
     Niño 3.4, à glisser-déposer sur le globe watchtower (import GeoJSON natif).

Usage : python3 scripts/build_climat_assets.py [--check]
  --check : ne réécrit rien, vérifie seulement que les artefacts sont à jour.
"""
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DATA = BASE / "data" / "climat" / "el-nino-2026" / "el-nino-godzilla-2026.json"
TEMPLATES = BASE / "scripts" / "templates" / "climat"
OUT_FRONTIGNAN = BASE / "projects" / "frontignan" / "el-nino-thau.html"
OUT_POC = BASE / "projects" / "COGNITORIUM" / "learning" / "el-nino-poc.html"
OUT_GEO = BASE / "projects" / "watchtower" / "public" / "data" / "enso-thau-watchpoints.geojson"

PLACEHOLDER = "__ELNINO_DATA__"


def safe_json_for_script(data) -> str:
    """JSON sûr à embarquer dans <script type="application/json">."""
    s = json.dumps(data, ensure_ascii=True)
    # empêche toute fermeture prématurée de la balise script
    return s.replace("</", "<\\/")


def render(template_path: Path, data) -> str:
    tpl = template_path.read_text(encoding="utf-8")
    if PLACEHOLDER not in tpl:
        raise RuntimeError(f"{template_path.name} : marqueur {PLACEHOLDER} introuvable")
    return tpl.replace(PLACEHOLDER, safe_json_for_script(data))


def build_geojson(data) -> dict:
    meta = data["meta"]
    status_label = {"observe": "observé / rapporté", "prevu": "prévu / projection", "incertain": "incertain / hypothèse"}
    features = []
    for w in data["geo"]["watchpoints"]:
        props = {
            "name": w["name"],
            "category": w["category"],
            "scope": w.get("scope", ""),
            "status": w.get("status", ""),
            "status_label": status_label.get(w.get("status", ""), w.get("status", "")),
            "description": w.get("description", ""),
            "dataset": meta["id"],
            "dataset_version": meta["version"],
            "as_of": meta["as_of"],
        }
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [round(w["lon"], 4), round(w["lat"], 4)]},
            "properties": props,
        })
    # boîte de la zone Niño 3.4 (5°N–5°S, 120°W–170°W) en polygone
    features.append({
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
    return {
        "type": "FeatureCollection",
        "name": f"enso-thau-watchpoints (dataset {meta['id']} v{meta['version']}, as_of {meta['as_of']})",
        "metadata": {
            "title": "El Niño 2026–2027 « Godzilla » — points de surveillance × bassin de Thau",
            "generated_by": "scripts/build_climat_assets.py",
            "source_dataset": "data/climat/el-nino-2026/el-nino-godzilla-2026.json",
            "origin": "Vidéo LIMIT « EL NIÑO : GODZILLA » (11/10/2026, Vinz × Xavier Fettweis — ULiège) + synthèse stratégique avec errata du 24/09/2026",
            "disclaimer": meta["disclaimer"],
            "usage": "Glisser-déposer ce fichier sur le globe watchtower (import GeoJSON natif du fork), ou le servir via /preview/watchtower/public/data/.",
        },
        "features": features,
    }


def main():
    check_only = "--check" in sys.argv
    if not DATA.exists():
        print(f"✗ dataset introuvable : {DATA}")
        sys.exit(2)
    data = json.loads(DATA.read_text(encoding="utf-8"))

    outputs = [
        (TEMPLATES / "frontignan-module.html.tmpl", OUT_FRONTIGNAN, "module Atlas Frontignan"),
        (TEMPLATES / "cognitorium-poc.html.tmpl", OUT_POC, "PoC Cognitorium"),
    ]
    ok = True
    for tpl_path, out_path, label in outputs:
        html = render(tpl_path, data)
        if check_only:
            current = out_path.read_text(encoding="utf-8") if out_path.exists() else ""
            fresh = current == html
            print(f"{'✓' if fresh else '✗'} {label} : {out_path.relative_to(BASE)} {'à jour' if fresh else 'PÉRIMÉ — relance build_climat_assets.py'}")
            ok = ok and fresh
        else:
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(html, encoding="utf-8")
            print(f"✓ {label} → {out_path.relative_to(BASE)} ({out_path.stat().st_size // 1024} Ko)")

    geo = build_geojson(data)
    geo_txt = json.dumps(geo, ensure_ascii=False, indent=1) + "\n"
    if check_only:
        current = OUT_GEO.read_text(encoding="utf-8") if OUT_GEO.exists() else ""
        fresh = current == geo_txt
        print(f"{'✓' if fresh else '✗'} watchpoints GeoJSON : {OUT_GEO.relative_to(BASE)} {'à jour' if fresh else 'PÉRIMÉ — relance build_climat_assets.py'}")
        ok = ok and fresh
    else:
        OUT_GEO.parent.mkdir(parents=True, exist_ok=True)
        OUT_GEO.write_text(geo_txt, encoding="utf-8")
        print(f"✓ watchpoints GeoJSON → {OUT_GEO.relative_to(BASE)} ({len(geo['features'])} features, {OUT_GEO.stat().st_size // 1024} Ko)")

    if check_only:
        sys.exit(0 if ok else 1)
    print(f"\nDataset source : {DATA.relative_to(BASE)} (v{data['meta']['version']}, as_of {data['meta']['as_of']})")
    print("Rappel : les artefacts générés ne s'éditent pas à la main — modifier le JSON puis relancer ce script.")


if __name__ == "__main__":
    main()
