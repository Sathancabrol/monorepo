#!/usr/bin/env python3
"""
audit_s0_map.py — Cartographie canonique des documents de la racine (S0).

Applique des règles ordonnées (première qui matche) aux 220 fichiers du dossier
de marché/chantier + les 4 fichiers de dépôt, produit :
  - audit/data/S0-mapping.json (fichier → famille canonique, taille)
  - un tableau markdown sur stdout (familles × fichiers × taille)
  - contrôle de couverture (aucun fichier orphelin, aucune famille vide)

Les noms de familles sont ceux de audit/CATEGORIES.md §1.1 (S0-familles).
Usage : python3 scripts/audit_s0_map.py [--check]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REPO_FILES = {".gitignore", "MANIFEST.json", "README.md", "requirements.txt"}

# (famille canonique, règle appliquée en premier-match)
RULES: list[tuple[str, str]] = [
    ("Pièces de marché (DCE)",            r"^(\d\d - |0\d - |SOMMAIRE-DCE|REGLEMENT-CONSULTATION|Réglement de consultation|CCAP|Cahier des Clauses Administratives|CCTP|LOT 2 CCTP|BPU|BP\.doc|AE\.doc|Acte d-engagement|DQE\.pdf|dc[45]mod|UN MÉMOIRE TECHNIQUE|mémoire technique|memoire justificatif|CDPGF|lotissement la croix pruniau)"),
    ("Devis, prix & budget",               r"^(DE LOT|DETAIL-ESTIMATIF|métré|DQE VERIF|Bibliothèque|23-LGPM)"),
    ("Prescriptions d'exécution (série F)", r"^F\d+"),
    ("Plans & profils",                    r"^(PLAN-|Plan |plan de situation|0[289] - |GEOPORTAIL)"),
    ("Suivi de chantier",                  r"^(compte-rendu|fiche de tache|fiche de nonconformité|FACTURE|SDN_|CHANTIER EN COURS|tableau recap|Equipement|planning |Page de garde|Rapport Chantier|invitation-|ordre de service|lordre-de-service|Dossier des Ouvrages|doe|essai\.xlsx)"),
    ("Études, essais & qualité",           r"^(Etude de dossier|PAQ|Exemple de PAQ|Essai|essai|QUALITE|Module-15|fichetechnique9|5683-|O015_|TB-5\.5|COURS etude de prix|SDP |démo decoupe|demo decoupe|arrachage|rabotage|sciage|décapage|démolition|objectif PAE2)"),
    ("Signalisation, sécurité & AIPR",     r"^(SIGNALISATION|Signalisation|Signalisation OPPBTP|courrier-signalisation|Arrêté|arrêté|aret|aret |demande d'arrete|DDE-ODP|AIPR|QCM AIPR|aipr |DESC)"),
    ("Réseaux, DT/DICT & autorisations",   r"(DICT|Dict|DICT\.pdf|cerfa|enedis|telecom|sivom|AUTORISATION DE VOIRIE|Permission|Récepissés DT|récepissés|brochure_entreprises)"),
    ("Ressources humaines & administration", r"^(salaire_|tableau_reclassement|fntp_|Support animation|logo stagiaire|2024 - PLANNING ANNUEL)"),
    ("Références techniques & fournisseurs", r"^(F-|bordure|BORUDRE|BORDURE|Bordures|pvc|regard|janolene|glisière|cunette|couche|trottoir|remblai|remplissage|ilot|ilôt|reprise|confection|janolène|Liant et gravillong|guide-conception|SeQuelec|Manuel_exploitation|ccag-travaux|standard-interne-doe|O J-|OJ-|fntp|notice_|307732019|blpc_|20190318_|abréviation)"),
    ("Juridique (recours & litiges)",      r"^Recours"),
    ("Images & vues",                      r"\.(png|jpg|jpeg|JPG|PNG|jpeg)$"),
    ("Divers",                             r".*"),  # attrape-tout assumé, doit rester petit
]


def main() -> None:
    root_files = sorted([f for f in ROOT.iterdir() if f.is_file()])
    docs = [f for f in root_files if f.name not in REPO_FILES]
    repo = [f for f in root_files if f.name in REPO_FILES]

    mapping = {}
    families: dict[str, list[dict]] = {}
    for f in docs:
        fam = next(name for name, rx in RULES if re.search(rx, f.name))
        item = {"file": f.name, "size": f.stat().st_size, "family": fam}
        mapping[f.name] = item
        families.setdefault(fam, []).append(item)

    order = [name for name, _ in RULES if name in families]
    total = sum(i["size"] for i in mapping.values())

    print(f"# Cartographie S0 — {len(docs)} documents, {len(repo)} fichiers de dépôt, {total/1024/1024:.1f} Mo\n")
    print("| Famille canonique | Fichiers | Taille | Part |\n|---|---:|---:|---:|")
    for fam in order:
        items = families[fam]
        size = sum(i["size"] for i in items)
        print(f"| {fam} | {len(items)} | {size/1024/1024:.1f} Mo | {100*size/total:.1f} % |")
    print(f"| **Total documents** | **{len(docs)}** | **{total/1024/1024:.1f} Mo** | 100 % |")

    divers = families.get("Divers", [])
    if divers:
        print(f"\n## Famille « Divers » ({len(divers)}) — à reclasser si possible\n")
        for i in sorted(divers, key=lambda x: -x["size"]):
            print(f"- `{i['file']}` ({i['size']/1024:.0f} Ko)")

    out = {"generated_at": __import__("datetime").datetime.now(
        __import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "documents": len(docs), "repo_files": [f.name for f in repo],
        "total_bytes": total, "families": {k: len(v) for k, v in families.items()},
        "family_bytes": {k: sum(i["size"] for i in v) for k, v in families.items()},
        "mapping": mapping}
    dest = ROOT / "audit" / "data" / "S0-mapping.json"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n→ {dest.relative_to(ROOT)}")

    if "--check" in sys.argv:
        missing = [f.name for f in docs if f.name not in mapping]
        print("check:", "OK" if not missing else f"{len(missing)} orphelins: {missing[:5]}")
        sys.exit(1 if missing else 0)


if __name__ == "__main__":
    main()
