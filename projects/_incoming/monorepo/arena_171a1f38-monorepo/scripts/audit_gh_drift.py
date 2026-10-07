#!/usr/bin/env python3
"""
audit_gh_drift.py — Écart entre une copie locale et l'état réel d'un dépôt GitHub.

Compare l'arbre local (projects/<nom>) à l'arbre GitHub (branche par défaut, ou
réf. donnée), fichier par fichier (chemin + taille blob). Ignore .git,
node_modules, dist par défaut (option --with-dist).

Sortie : audit/data/drift.json + synthèse stdout.
Usage :
  python3 scripts/audit_gh_drift.py                 # tous les projets mappés
  python3 scripts/audit_gh_drift.py --project watchtower
  python3 scripts/audit_gh_drift.py --project watchtower --ref arena/01a0730a-watchtower
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OWNER = "Sathancabrol"
MAP = {
    "COGNITORIUM": "COGNITORIUM",
    "proto-cognitorium": "proto-cognitorium",
    "HCSM": "HCSM",
    "reaserch-engine": "reaserch-engine",
    "ETAT-DE-LART-PSYCHOLOGIE": "ETAT-DE-LART-PSYCHOLOGIE",
    "watchtower": "watchtower",
    "animation-chronos": "animation-chronos",
    "Language-decoder": "Language-decoder",
}
IGNORE_DIRS = {".git", "node_modules", "__pycache__", ".venv", ".next", "dist", "build"}
OUT = ROOT / "audit" / "data" / "drift.json"


def gh_json(args: list[str]):
    """Appel API JSON (sans --jq : on parse le JSON brut)."""
    res = subprocess.run(["gh", "api", "-H", "Accept: application/vnd.github+json", *args],
                         capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(res.stderr.strip()[:300])
    return json.loads(res.stdout)


def local_tree(base: Path) -> dict[str, int]:
    out = {}
    for p in base.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(base)
        if any(part in IGNORE_DIRS for part in rel.parts):
            continue
        out[str(rel).replace("\\", "/")] = p.stat().st_size
    return out


def remote_tree(repo: str, ref: str) -> dict[str, int]:
    sha = gh_json([f"repos/{OWNER}/{repo}/commits/{ref}"])["sha"]
    data = gh_json([f"repos/{OWNER}/{repo}/git/trees/{sha}?recursive=1"])
    out = {}
    for item in data.get("tree", []):
        if item["type"] != "blob":
            continue
        path = item["path"]
        if any(part in IGNORE_DIRS for part in path.split("/")):
            continue
        out[path] = item.get("size", -1)
    return out, sha, data.get("truncated", False)


def compare(name: str, ref: str | None = None) -> dict:
    local_base = ROOT / "projects" / name
    repo = MAP.get(name, name)
    ref = ref or gh_json([f"repos/{OWNER}/{repo}"])["default_branch"]
    loc = local_tree(local_base)
    rem, sha, truncated = remote_tree(repo, ref)
    loc_set, rem_set = set(loc), set(rem)
    common = loc_set & rem_set
    changed = sorted(p for p in common if loc[p] != rem[p])
    return {
        "project": name, "repo": f"{OWNER}/{repo}", "ref": ref, "sha": sha,
        "truncated": truncated,
        "local_files": len(loc), "remote_files": len(rem),
        "only_local": sorted(loc_set - rem_set)[:100],
        "only_remote": sorted(rem_set - loc_set)[:100],
        "size_changed": changed[:100],
        "counts": {"only_local": len(loc_set - rem_set), "only_remote": len(rem_set - loc_set),
                   "size_changed": len(changed)},
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", default=None)
    ap.add_argument("--ref", default=None)
    args = ap.parse_args()

    out = json.loads(OUT.read_text()) if OUT.exists() else {}
    projects = [args.project] if args.project else list(MAP)
    for name in projects:
        try:
            r = compare(name, args.ref if args.project else None)
        except Exception as e:
            print(f"{name}: ERREUR {e}")
            continue
        out[name] = r
        c = r["counts"]
        print(f"{name:28} ref={r['ref']:<28} sha={r['sha'][:8]} "
              f"local={r['local_files']:>4} remote={r['remote_files']:>4} "
              f"| +local {c['only_local']:>3} | +remote {c['only_remote']:>3} | Δtaille {c['size_changed']:>3}"
              + (" (tronqué)" if r["truncated"] else ""))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out["_generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n→ {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
