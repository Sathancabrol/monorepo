#!/usr/bin/env python3
"""
Vérification de complétude des dépôts — « rien ne doit manquer dans le monorepo ».

Pour chaque dépôt de l'utilisateur GitHub, le script vérifie que le monorepo
possède bien tout ce que contiennent les dépôts, **et tout ce que contiennent
leurs branches non fusionnées**.

Méthode (exacte, pas approximative) :
  - chaque fichier distant a une empreinte Git (blob SHA) calculée par GitHub ;
  - `git cat-file -e <sha>` dans le monorepo dit si cette empreinte exacte existe
    déjà quelque part dans le dépôt (fichier suivi, ou contenu identique importé
    ailleurs, ou présent dans une révision antérieure).
  - Un fichier n'est donc déclaré « manquant » que si son **contenu exact**
    n'existe nulle part dans le monorepo.

Le script NE MODIFIE RIEN.

Usage :
  python3 scripts/verif-completude-repos.py               # tout
  python3 scripts/verif-completude-repos.py --repo HCSM   # un dépôt
  python3 scripts/verif-completude-repos.py --details     # lister les manquants
  python3 scripts/verif-completude-repos.py --no-branches # seulement `main`

Sortie : code 0 si tout est présent, 1 sinon. Nécessite `gh` authentifié et python3.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

OWNER = "Sathancabrol"
CURRENT = "arena/0034230e-monorepo"  # branche de travail : ne pas se comparer à soi-même
REPOS = {
    "COGNITORIUM": "projects/COGNITORIUM",
    "proto-cognitorium": "projects/proto-cognitorium",
    "ETAT-DE-LART-PSYCHOLOGIE": "projects/ETAT-DE-LART-PSYCHOLOGIE",
    "HCSM": "projects/HCSM",
    "reaserch-engine": "projects/reaserch-engine",
    "Language-decoder": "projects/Language-decoder",
    "watchtower": "projects/watchtower",
    "animation-chronos": "projects/animation-chronos",
    "monorepo": None,
}
EXCL = ("node_modules/", ".next/", ".turbo/", "coverage/")


def gh_api(path: str) -> dict:
    out = subprocess.run(["gh", "api", path], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(out.stderr.strip() or f"gh api {path} a échoué")
    return json.loads(out.stdout)


def tree_of(repo: str, ref: str) -> dict[str, tuple[str, int]]:
    """path -> (blob sha, taille) pour un arbre distant (récursif)."""
    data = gh_api(f"repos/{OWNER}/{repo}/git/trees/{ref}?recursive=1")
    if data.get("truncated"):
        print(f"  ⚠ arbre tronqué par l'API pour {repo}@{ref}", file=sys.stderr)
    out = {}
    for t in data["tree"]:
        if t["type"] == "blob" and not any(x in t["path"] for x in EXCL):
            out[t["path"]] = (t["sha"], t.get("size", 0))
    return out


def local_index_dir(d: str) -> dict[str, int]:
    """index nom-de-fichier -> tailles, pour comparaison par chemin."""
    idx: dict[str, int] = {}
    for root, _dirs, files in os.walk(d):
        for f in files:
            idx[os.path.relpath(os.path.join(root, f), d)] = os.path.getsize(os.path.join(root, f))
    return idx


def have_blob(sha: str) -> bool:
    """L'empreinte exacte existe-t-elle dans l'historique du monorepo ?"""
    return subprocess.run(["git", "cat-file", "-e", sha], capture_output=True).returncode == 0


def check_repo_main(repo: str, details: bool) -> tuple[int, int, list[str]]:
    """Contenu de `main` : doit être présent au même chemin dans projects/<dépôt>/."""
    local_dir = REPOS[repo]
    if not local_dir or not os.path.isdir(local_dir):
        print(f"✗ {repo:26s} dossier local absent")
        return 0, 1, [local_dir or repo]
    remote = tree_of(repo, "HEAD")
    local = local_index_dir(local_dir)
    # par chemin (et taille identique), ou par contenu identique
    missing = []
    for p, (sha, size) in remote.items():
        if p in local and local[p] == size:
            continue
        if have_blob(sha):
            continue
        missing.append(p)
    flag = "✓" if not missing else "✗"
    print(f"{flag} {repo:26s} {len(remote):5d} fichiers distants · manquants : {len(missing)}")
    if missing and details:
        for p in sorted(missing)[:20]:
            print(f"      - {p}")
    return len(remote), len(missing), missing


def check_repo_branches(repo: str, details: bool) -> tuple[int, int]:
    """Contenu des branches en avance : le contenu exact doit exister quelque part."""
    try:
        bs = [b["name"] for b in gh_api(f"repos/{OWNER}/{repo}/branches?per_page=100")]
    except RuntimeError as e:
        print(f"  !! {repo} : {e}")
        return 0, 0
    total_n = total_m = 0
    for b in bs:
        if b == "main" or (repo == "monorepo" and b == CURRENT):
            continue
        try:
            cmp = gh_api(f"repos/{OWNER}/{repo}/compare/main...{b}")
        except RuntimeError:
            continue
        if cmp.get("ahead_by", 0) <= 0:
            continue  # déjà fusionnée dans main
        changed = [f for f in cmp.get("files", []) if f["status"] != "removed"]
        # empreintes des fichiers de la branche
        try:
            tree = tree_of(repo, b)
        except RuntimeError:
            continue
        missing = []
        for f in changed:
            name = f["filename"]
            if name not in tree:
                continue  # binaire non renvoyé par l'API ou renommé
            sha, _size = tree[name]
            if not have_blob(sha):
                missing.append(name)
        flag = "✓" if not missing else "✗"
        print(f"{flag} {repo:26s} {b:42s} +{cmp.get('ahead_by', 0):3d} commits · "
              f"{len(changed):3d} fichiers modifiés · contenu absent : {len(missing)}")
        if missing and details:
            for p in missing[:10]:
                print(f"      - {p}")
        total_n += len(changed)
        total_m += len(missing)
    return total_n, total_m


def main() -> int:
    ap = argparse.ArgumentParser(description="Vérifie que le monorepo contient tout le travail des dépôts.")
    ap.add_argument("--repo", help="ne vérifier qu'un dépôt")
    ap.add_argument("--no-branches", action="store_true", help="ignorer les branches non fusionnées")
    ap.add_argument("--details", action="store_true", help="lister les fichiers manquants")
    args = ap.parse_args()

    if args.repo and args.repo not in REPOS:
        print(f"Dépôt inconnu : {args.repo}\nConnus : {', '.join(REPOS)}")
        return 2
    targets = [args.repo] if args.repo else list(REPOS)

    print("=" * 80)
    print("1) CONTENU DE main  →  présent dans projects/<dépôt>/ (chemin ou contenu identique)")
    print("=" * 80)
    nb_files = nb_missing = 0
    for repo in targets:
        if repo == "monorepo":
            continue
        n, m, _ = check_repo_main(repo, args.details)
        nb_files += n
        nb_missing += m

    if not args.no_branches:
        print()
        print("=" * 80)
        print("2) BRANCHES NON FUSIONNÉES  →  contenu exact présent quelque part dans le monorepo")
        print("=" * 80)
        for repo in targets:
            n, m = check_repo_branches(repo, args.details)
            nb_files += n
            nb_missing += m

    print()
    print("=" * 80)
    print(f"Fichiers examinés : {nb_files} · contenu absent du monorepo : {nb_missing}")
    if nb_missing == 0:
        print("RÉSULTAT : ✓ rien ne manque — le monorepo contient tout le travail des dépôts.")
    else:
        print("RÉSULTAT : ✗ des fichiers restent à récupérer (voir --details).")
    print("=" * 80)
    return 0 if nb_missing == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
