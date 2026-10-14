#!/usr/bin/env python3
"""
audit_inventory.py — Inventaire factuel reproductible pour l'audit.

Mesure, sans dépendance externe :
  - fichiers / taille / répartition par extension et par dossier de 1er niveau
  - lignes de code par langage (heuristique d'extension + fichiers texte)
  - manifests, tests, docs, TODO/FIXME, fichiers sensibles potentiels
Sortie : JSON (audit/data/inventory.json) + tableau markdown compact sur stdout.

Usage :
  python3 scripts/audit_inventory.py --root . --label racine
  python3 scripts/audit_inventory.py --root projects/watchtower --label watchtower
  python3 scripts/audit_inventory.py --all           # tous les périmètres d'un coup
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", ".next", "dist", "build",
                ".cursor", ".idea", ".vscode", "coverage", ".pytest_cache", ".mypy_cache"}
# dist/ est exclu par défaut (build) mais mesuré séparément si --with-build

CODE_EXT = {
    ".py": "Python", ".js": "JavaScript", ".mjs": "JavaScript", ".cjs": "JavaScript",
    ".ts": "TypeScript", ".tsx": "TypeScript", ".jsx": "JavaScript",
    ".html": "HTML", ".htm": "HTML", ".css": "CSS", ".scss": "CSS",
    ".json": "JSON", ".jsonl": "JSONL", ".geojson": "GeoJSON",
    ".md": "Markdown", ".yaml": "YAML", ".yml": "YAML", ".toml": "TOML",
    ".sh": "Shell", ".ps1": "PowerShell", ".bat": "Batch",
    ".sql": "SQL", ".csv": "CSV", ".tsv": "TSV",
    ".java": "Java", ".rs": "Rust", ".go": "Go", ".c": "C", ".cpp": "C++", ".h": "C",
}
CODE_LANGS = {"Python", "JavaScript", "TypeScript", "HTML", "CSS", "Shell", "PowerShell",
              "Batch", "SQL", "Java", "Rust", "Go", "C", "C++", "TOML", "YAML", "Docker", "Makefile"}
DOC_EXT = {".md", ".docx", ".doc", ".pdf", ".pptx", ".rtf", ".odt", ".xlsx", ".xls"}
DATA_EXT = {".csv", ".tsv", ".json", ".jsonl", ".geojson", ".geojsonl", ".parquet", ".db", ".sqlite", ".yaml", ".yml"}
MANIFESTS = {"package.json", "pyproject.toml", "requirements.txt", "setup.py", "bun.lock",
             "package-lock.json", "Cargo.toml", "go.mod", "pom.xml", "Gemfile", "composer.json",
             "vite.config.js", "vite.config.ts", "tsconfig.json"}
TEST_RE = re.compile(r"(^|/)(tests?|__tests__|spec)(/|$)|(^|/)(test_|.*\.(test|spec)\.)", re.I)
SECRET_RE = re.compile(
    r"(api[_-]?key|secret|passwd|password|token|private[_-]?key|access[_-]?key|client[_-]?secret)",
    re.I)
SECRET_FILES = re.compile(r"(^|/)(\.env(\..+)?|credentials.*|identifiants.*|secrets?\.(json|ya?ml|txt)|.*\.pem|.*\.key|id_rsa.*)$", re.I)
LONG_LINE = 0  # compteur de lignes de code (non vides, non commentaires simples)


def lang_of(path: Path) -> str | None:
    ext = path.suffix.lower()
    if ext in CODE_EXT:
        return CODE_EXT[ext]
    if path.name == "Dockerfile":
        return "Docker"
    if path.name.lower() in {"makefile", "justfile"}:
        return "Makefile"
    return None


def count_loc(path: Path) -> int:
    n = 0
    try:
        with path.open("r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                s = line.strip()
                if s and not s.startswith(("#", "//", "/*", "*", "<!--", "--")):
                    n += 1
    except OSError:
        return 0
    return n


def scan(root: Path, with_build: bool = False) -> dict:
    files = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS or (with_build and d == "dist")]
        for fn in filenames:
            p = Path(dirpath) / fn
            try:
                st = p.stat()
            except OSError:
                continue
            files.append({"path": str(p.relative_to(root)), "ext": p.suffix.lower(),
                          "size": st.st_size, "name": p.name})
    total_size = sum(f["size"] for f in files)
    by_ext = Counter(f["ext"] or "(sans)" for f in files)
    size_by_ext = defaultdict(int)
    for f in files:
        size_by_ext[f["ext"] or "(sans)"] += f["size"]
    by_top = Counter()
    size_by_top = defaultdict(int)
    for f in files:
        top = f["path"].split(os.sep)[0] if os.sep in f["path"] else "(racine)"
        by_top[top] += 1
        size_by_top[top] += f["size"]
    loc = Counter()
    loc_files = Counter()
    loc_other = Counter()
    n_text = 0
    for f in files:
        p = root / f["path"]
        lang = lang_of(p)
        if lang:
            n_text += 1
            if lang in CODE_LANGS:
                loc[lang] += count_loc(p)
                loc_files[lang] += 1
            else:
                loc_other[lang] += count_loc(p)
    big = sorted(files, key=lambda x: -x["size"])[:15]
    manifests = [f["path"] for f in files if f["name"] in MANIFESTS]
    tests = [f["path"] for f in files if TEST_RE.search(f["path"])]
    docs = [f["path"] for f in files if f["ext"] in DOC_EXT]
    data = [f["path"] for f in files if f["ext"] in DATA_EXT]
    sensitive = [f["path"] for f in files if SECRET_FILES.search(f["path"])]
    todos = 0
    todo_by_file = {}
    for f in files:
        if f["ext"] in {".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", ".md", ".yaml", ".yml", ".json"}:
            p = root / f["path"]
            try:
                txt = p.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            c = len(re.findall(r"\b(TODO|FIXME|XXX|HACK)\b", txt))
            if c:
                todos += c
                todo_by_file[f["path"]] = c
    return {
        "label": root.name or ".",
        "root": str(root),
        "scanned_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "files": len(files),
        "size_bytes": total_size,
        "size_human": human(total_size),
        "by_ext": [{"ext": k or "(sans)", "files": v, "size": size_by_ext[k]} for k, v in by_ext.most_common(25)],
        "by_top": [{"dir": k, "files": v, "size": size_by_top[k]} for k, v in by_top.most_common(30)],
        "loc": [{"lang": k, "lines": v, "files": loc_files[k]} for k, v in loc.most_common()],
        "loc_total": sum(loc.values()),
        "loc_other": [{"lang": k, "lines": v} for k, v in loc_other.most_common()],
        "code_files": n_text,
        "manifests": sorted(manifests)[:30],
        "tests": sorted(tests)[:80],
        "tests_count": len(tests),
        "docs": sorted(docs)[:80],
        "docs_count": len(docs),
        "data_files": sorted(data)[:60],
        "data_count": len(data),
        "sensitive_names": sorted(sensitive)[:40],
        "sensitive_count": len(sensitive),
        "todos_total": todos,
        "todos_top": sorted(todo_by_file.items(), key=lambda x: -x[1])[:15],
        "biggest": [{"path": b["path"], "size": b["size"]} for b in big],
    }


def human(n: int) -> str:
    for unit in ("o", "Ko", "Mo", "Go"):
        if n < 1024 or unit == "Go":
            return f"{n:.1f} {unit}" if unit != "o" else f"{n} o"
        n /= 1024
    return f"{n}"


def print_table(inv: dict) -> None:
    print(f"## {inv['label']} — {inv['files']} fichiers, {inv['size_human']}, "
          f"{inv['loc_total']} lignes de code ({inv['code_files']} fichiers code)")
    print("\n| Répartition par extension | Fichiers | Taille |\n|---|---|---|")
    for e in inv["by_ext"][:14]:
        print(f"| `{e['ext']}` | {e['files']} | {human(e['size'])} |")
    print("\n| Langage | Fichiers | Lignes |\n|---|---|---|")
    for l in inv["loc"][:14]:
        print(f"| {l['lang']} | {l['files']} | {l['lines']} |")
    if inv["manifests"]:
        print(f"\nManifests ({len(inv['manifests'])}) : " + ", ".join(f"`{m}`" for m in inv["manifests"][:12]))
    print(f"Tests : {inv['tests_count']} · Docs : {inv['docs_count']} · Données : {inv['data_count']} · "
          f"Noms sensibles : {inv['sensitive_count']} · TODO/FIXME : {inv['todos_total']}")
    if inv["sensitive_names"]:
        print("Noms sensibles :")
        for s in inv["sensitive_names"][:12]:
            print(f"  - `{s}`")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--label", default="")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--out", default="audit/data/inventory.json")
    ap.add_argument("--with-build", action="store_true")
    args = ap.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    existing = json.loads(out.read_text()) if out.exists() else {}

    if args.all:
        root = Path(".")
        scopes = [("S0-racine", root, False), ("S1-infra", None, False)]
        results = {}
        # S0 : fichiers à la racine uniquement (pas de descente)
        s0 = [f for f in root.iterdir() if f.is_file()]
        results["S0-racine-fichiers-directs"] = {
            "files": len(s0), "size_bytes": sum(f.stat().st_size for f in s0),
            "size_human": human(sum(f.stat().st_size for f in s0)),
            "exts": Counter(f.suffix.lower() or "(sans)" for f in s0).most_common(),
        }
        for name in ["app", "scripts", "data", "docs"]:
            p = root / name
            if p.exists():
                results[f"S1-{name}"] = scan(p, args.with_build)
        for name in sorted((root / "projects").iterdir()):
            if name.is_dir():
                results[f"P-{name.name}"] = scan(name, args.with_build)
        existing["scopes"] = results
    else:
        inv = scan(Path(args.root), args.with_build)
        if args.label:
            inv["label"] = args.label
        print_table(inv)
        existing[inv["label"]] = inv

    out.write_text(json.dumps(existing, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n→ {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
