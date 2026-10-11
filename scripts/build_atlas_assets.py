#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Construit la coquille Atlas Frontignan (Phase 0) depuis la spec canonique.

Entrées :
  - data/atlas-frontignan/atlas-frontignan-2026.json      (spec, schéma atlas-frontignan-v1)
  - data/climat/frontignan-episodes-cevenols/…            (dataset cévenols — zones DATA)
  - data/climat/el-nino-2026/…                            (dataset El Niño — watchpoints
    climat locaux au bassin de Thau, injectés en projection allégée : meta + geo.watchpoints
    filtrés sur category == "local")

Sortie :
  - projects/frontignan/atlas.html — console territoriale autonome (sans dépendance) :
    14 lentilles de vue, carte stylisée SVG, inspecteur, 7 modules, arbre de 15 actions,
    comparateur avant/après (placeholders assumés), 5 phases, méthode & statuts
    EMPTY → SHELL → DATA → LIVE → SIM.

Usage : python3 scripts/build_atlas_assets.py [--check]
  --check : ne réécrit rien, vérifie que l'artefact est à jour.
"""
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

SPEC_PATH = BASE / "data" / "atlas-frontignan" / "atlas-frontignan-2026.json"
CEV_PATH = BASE / "data" / "climat" / "frontignan-episodes-cevenols" / "frontignan-cevenols-2026.json"
ELN_PATH = BASE / "data" / "climat" / "el-nino-2026" / "el-nino-godzilla-2026.json"
TEMPLATE = BASE / "scripts" / "templates" / "atlas" / "atlas-shell.html.tmpl"
OUT = BASE / "projects" / "frontignan" / "atlas.html"

PLACEHOLDER_RE = re.compile(r"__[A-Z]+_DATA__")


def safe_json_for_script(data) -> str:
    """JSON sûr à embarquer dans <script type="application/json">."""
    s = json.dumps(data, ensure_ascii=True)
    return s.replace("</", "<\\/")  # empêche toute fermeture prématurée de la balise script


def slim_elnino(e: dict) -> dict:
    """Projection allégée du dataset El Niño : seuls les watchpoints locaux servent la carte."""
    locals_ = [w for w in e.get("geo", {}).get("watchpoints", []) if w.get("category") == "local"]
    return {
        "meta": {"id": e["meta"]["id"], "version": e["meta"]["version"], "as_of": e["meta"]["as_of"]},
        "geo": {"watchpoints": locals_},
        "note": "projection allégée du dataset el-nino-godzilla-2026 (watchpoints locaux au bassin de Thau) — construite par scripts/build_atlas_assets.py",
    }


def main():
    check_only = "--check" in sys.argv
    for p in (SPEC_PATH, CEV_PATH, ELN_PATH, TEMPLATE):
        if not p.exists():
            print(f"✗ introuvable : {p}")
            sys.exit(2)

    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    cev = json.loads(CEV_PATH.read_text(encoding="utf-8"))
    eln = json.loads(ELN_PATH.read_text(encoding="utf-8"))

    tpl = TEMPLATE.read_text(encoding="utf-8")
    for ph, data in {
        "__ATLAS_SPEC__": spec,
        "__CEVENOLS_DATA__": cev,
        "__ELNINO_DATA__": slim_elnino(eln),
    }.items():
        if ph in tpl:
            tpl = tpl.replace(ph, safe_json_for_script(data))
    leftover = PLACEHOLDER_RE.search(tpl)
    if leftover:
        raise RuntimeError(f"{TEMPLATE.name} : marqueur non résolu {leftover.group(0)}")

    if check_only:
        current = OUT.read_text(encoding="utf-8") if OUT.exists() else ""
        fresh = current == tpl
        print(f"{'✓' if fresh else '✗'} coquille Atlas : {OUT.relative_to(BASE)} {'à jour' if fresh else 'PÉRIMÉ — relance build_atlas_assets.py'}")
        sys.exit(0 if fresh else 1)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(tpl, encoding="utf-8")
    n_data = sum(1 for o in spec["map"]["objects"] if o.get("data_link"))
    print(f"✓ coquille Atlas → {OUT.relative_to(BASE)} ({OUT.stat().st_size // 1024} Ko)")
    print(f"  spec v{spec['meta']['version']} (as_of {spec['meta']['as_of']}) : "
          f"{len(spec['modes'])} modes · {len(spec['modules'])} modules · {len(spec['actions'])} actions · "
          f"{len(spec['indicators'])} indicateurs · {len(spec['map']['objects'])} objets carte ({n_data} DATA)")
    print(f"  datasets injectés : cévenols (complet, {len(cev['blocking_points'])} blocages) + "
          f"el-nino (allégé, {len(slim_elnino(eln)['geo']['watchpoints'])} watchpoints locaux)")
    print("Rappel : artefact généré — ne pas l'éditer à la main ; modifier la spec puis relancer ce script.")


if __name__ == "__main__":
    main()
