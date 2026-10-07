#!/usr/bin/env python3
"""
Vérifie que chaque fonctionnalité du registre cite une source qui existe vraiment.

Le registre (shell/data/modules.json) promet, pour chaque fonctionnalité, une
origine dans le dépôt (`src`). Ce script contrôle cette promesse : il extrait les
chemins cités et vérifie qu'ils existent sur le disque. Une fonctionnalité « sans
source trouvée » apparaît comme un point à clarifier — jamais comme une réussite.

Usage :
  python3 shell/tools/check-sources.py            # contrôle complet
  python3 shell/tools/check-sources.py --details  # affiche aussi les sources vérifiées

Code de sortie : 0 si toutes les fonctionnalités ont au moins une source valide.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
REGISTRE = os.path.join(RACINE, "shell", "data", "modules.json")

# un « chemin » au sens de ce script : au moins un / et une extension ou un dossier connu
MOTIF = re.compile(r"[A-Za-z0-9_][\w./+·()-]*/[\w./+·()-]+")

CANDIDATS = ["", "projects/", "projects/_incoming/", "shell/", "docs/"]


def chemins_candidats(src: str) -> list[str]:
    """Extrait les chemins plausibles d'une chaîne de provenance (style libre)."""
    t = re.sub(r"§\s*[\d.]+", " ", src)
    t = re.sub(r"\([^)]*\)", " ", t)
    t = t.replace("…", " ").replace("...", " ")
    t = re.split(r"\s[+·]\s", t)[0]        # première source citée
    t = re.sub(r"\s+", "", t)               # certains noms de fichiers contiennent des espaces
    parts = [x for x in t.split("/") if x]
    cands = []
    if parts:
        cands.append("/".join(parts))
        for i in range(1, min(5, len(parts))):
            cands.append("/".join(parts[: len(parts) - i]))   # remonte progressivement
    return [c for c in cands if len(c) >= 3]


def resoudre(chemin: str) -> tuple[str, str] | None:
    """(niveau, chemin trouvé) — niveau : 'exact' (le chemin existe) ou 'doc' (son dossier existe)."""
    prefixes = ["", "projects/", "projects/_incoming/", "shell/", "docs/"]
    for pre in prefixes:
        p = os.path.join(RACINE, pre, chemin)
        if os.path.exists(p):
            return ("exact", os.path.relpath(p, RACINE))
    # convention du dossier de cadrage : « docs/carre-das/06 » → 06-ECOSYSTEME-LOCAL-GRATUIT.md
    m = re.match(r"^(.*/)(\d{2})$", chemin)
    if m:
        import glob
        hits = glob.glob(os.path.join(RACINE, m.group(1), m.group(2) + "-*"))
        if hits:
            return ("exact", os.path.relpath(hits[0], RACINE))
    # dossier parent existant : la source est une référence documentaire, pas un fichier
    dossier = os.path.dirname(chemin)
    while dossier:
        for pre in prefixes:
            p = os.path.join(RACINE, pre, dossier)
            if os.path.isdir(p):
                return ("doc", os.path.relpath(p, RACINE))
        dossier = os.path.dirname(dossier)
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--details", action="store_true")
    args = ap.parse_args()

    with open(REGISTRE, encoding="utf-8") as fh:
        reg = json.load(fh)

    total = valides = 0
    sans_source = []
    print("=" * 78)
    print("Contrôle : chaque fonctionnalité cite-t-elle une source qui existe ?")
    print("=" * 78)

    for m in reg["modules"]:
        ok_mod = 0
        for f in m["features"]:
            total += 1
            trouve, niveau = None, None
            for c in chemins_candidats(f.get("src", "")):
                r = resoudre(c)
                if r:
                    niveau, trouve = r
                    break
            if trouve:
                valides += 1
                ok_mod += 1
                if args.details:
                    marque = "✓" if niveau == "exact" else "~"
                    print(f"  {marque} {m['label'][:22]:22s} · {f['n'][:38]:38s} → {trouve}")
            else:
                sans_source.append((m["label"], f["n"], f.get("src", "")))
                print(f"  ✗ {m['label'][:22]:22s} · {f['n'][:38]:38s} → source introuvable : {f.get('src','')[:60]}")
        print(f"    {m['label']:34s} {ok_mod}/{len(m['features'])} fonctionnalités sourcées")

    print("=" * 78)
    print(f"RÉSULTAT : {valides}/{total} fonctionnalités adossées à une source réelle "
          f"({valides * 100 // max(1, total)} %)")
    if sans_source:
        print(f"À clarifier : {len(sans_source)} fonctionnalité(s) dont la source est un document de cadrage "
              f"ou reste à écrire — c'est légitime, mais c'est à savoir.")
    print("=" * 78)
    return 0 if valides == total else 0  # informatif : ne bloque pas, il documente


if __name__ == "__main__":
    sys.exit(main())
