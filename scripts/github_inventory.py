#!/usr/bin/env python3
"""
Inventaire GitHub — stdlib uniquement, token côté serveur, jamais exposé.
- Liste les dépôts de Sathancabrol (publics) via API GitHub (paginate, rate-limit)
- Pour chaque repo : branches, 20 derniers commits du default_branch, modules détectés, languages
- Écrit data/github_inventory.json (snapshot)
Usage:
  GITHUB_TOKEN=ghp_xxx python scripts/github_inventory.py [--user Sathancabrol] [--out data/github_inventory.json]
  # sans token : mode public anonyme (60 req/h)
"""
from __future__ import annotations
import argparse
import base64
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timezone

API = "https://api.github.com"
MANIFEST_FILES = {
    "package.json": "node",
    "pyproject.toml": "python",
    "requirements.txt": "python",
    "setup.py": "python",
    "setup.cfg": "python",
    "go.mod": "go",
    "Cargo.toml": "rust",
    "pom.xml": "java",
    "build.gradle": "java",
    "Gemfile": "ruby",
    "composer.json": "php",
    ".csproj": "dotnet",
}

def gh_fetch(url: str, token: str | None, accept: str = "application/vnd.github.v3+json"):
    headers = {"Accept": accept, "User-Agent": "monorepo-inventory/1.0"}
    if token:
        headers["Authorization"] = f"token {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
            remaining = resp.headers.get("X-RateLimit-Remaining")
            reset = resp.headers.get("X-RateLimit-Reset")
            return data, resp.headers, None
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:2000] if e.fp else ""
        return None, e.headers, (e.code, body, dict(e.headers))
    except Exception as e:
        return None, {}, (0, str(e), {})

def paginate(url: str, token: str | None):
    out = []
    next_url = url
    while next_url:
        data, headers, err = gh_fetch(next_url, token)
        if err:
            print(f"  ! HTTP {err[0]} for {next_url}: {err[1][:400]}", file=sys.stderr)
            break
        if isinstance(data, list):
            out.extend(data)
        else:
            out.append(data)
        link = headers.get("Link", "") if hasattr(headers, "get") else ""
        # parse Link: <url>; rel="next"
        nxt = None
        if link:
            for part in link.split(","):
                if 'rel="next"' in part:
                    nxt = part.split(";")[0].strip().strip("<>").strip()
        next_url = nxt
        # pagination delay
        if next_url:
            time.sleep(0.2)
    return out

def detect_modules_local(repo_name: str, projects_root: Path):
    """Scan local projects/<repo> for manifeste -> module list."""
    base = projects_root / repo_name
    if not base.exists():
        return []
    modules = []
    # root is always a module if has manifest or is known project
    # scan depth 2
    seen = set()
    for root, dirs, files in os.walk(base):
        rel = Path(root).relative_to(base)
        depth = len(rel.parts)
        if depth > 2:
            dirs[:] = []
            continue
        # skip hidden, node_modules, dist, .git, venv, __pycache__
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in ("node_modules", "dist", "build", "__pycache__", "venv", ".venv", "target", "out")]
        for f in files:
            if f in MANIFEST_FILES or f.endswith(".csproj"):
                mod_path = str(rel) if str(rel) != "." else "."
                if mod_path not in seen:
                    lang = MANIFEST_FILES.get(f, "unknown")
                    if f.endswith(".csproj"):
                        lang = "dotnet"
                    modules.append({"path": mod_path, "manifest": f, "lang": lang})
                    seen.add(mod_path)
    if not modules:
        # fallback: root as generic module with detected lang via GitHub language
        modules.append({"path": ".", "manifest": None, "lang": "unknown"})
    return modules

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", default=os.environ.get("GITHUB_USER", "Sathancabrol"))
    ap.add_argument("--out", default="data/github_inventory.json")
    ap.add_argument("--projects-root", default="projects")
    args = ap.parse_args()
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    user = args.user
    out_path = Path(args.out)
    projects_root = Path(args.projects_root)

    print(f"→ inventaire GitHub pour {user} (token={'oui' if token else 'non-anonyme'})")
    # list repos (public, not fork filtering done later)
    repos, headers, err = gh_fetch(f"{API}/users/{user}/repos?per_page=100&sort=updated", token)
    # actually paginate for real
    if isinstance(repos, list) and headers.get("Link"):
        repos = paginate(f"{API}/users/{user}/repos?per_page=100&sort=updated", token)
    if err and repos is None:
        print(f"ERREUR liste repos: {err}", file=sys.stderr)
        repos = []
    if not isinstance(repos, list):
        repos = [repos] if repos else []
    # filter: exclude the monorepo itself from source list? keep but mark
    all_repos = []
    for r in repos:
        # gh_fetch single-page without paginate already returns list; ensure we have dicts
        if not isinstance(r, dict):
            continue
        all_repos.append(r)

    # dedup by name
    seen = {}
    for r in all_repos:
        seen[r["name"]] = r
    all_repos = list(seen.values())
    print(f"  {len(all_repos)} dépôts trouvés")

    inventory = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "user": user,
        "count": len(all_repos),
        "repos": [],
        "rate_limit_remaining": None,
    }

    total_api_calls = 1
    for idx, repo in enumerate(sorted(all_repos, key=lambda x: x["name"].lower()), 1):
        name = repo["name"]
        print(f"[{idx}/{len(all_repos)}] {name} ...")
        is_monorepo = name == "monorepo"
        # branches
        branches_data, _, err = gh_fetch(f"{API}/repos/{user}/{name}/branches?per_page=100", token)
        total_api_calls += 1
        if err:
            branches = []
            print(f"  ! branches err {err[0]}")
        else:
            branches = branches_data if isinstance(branches_data, list) else []
        # commits (20 derniers sur default_branch)
        default_branch = repo.get("default_branch") or "main"
        commits_data, _, err = gh_fetch(f"{API}/repos/{user}/{name}/commits?per_page=20&sha={default_branch}", token)
        total_api_calls += 1
        if err:
            commits = []
        else:
            commits = commits_data if isinstance(commits_data, list) else []
        # languages
        langs_data, _, _ = gh_fetch(f"{API}/repos/{user}/{name}/languages", token)
        total_api_calls += 1
        langs = langs_data if isinstance(langs_data, dict) else {}

        # modules local scan
        local_modules = detect_modules_local(name, projects_root)

        # build repo entry
        entry = {
            "name": name,
            "full_name": repo.get("full_name"),
            "html_url": repo.get("html_url"),
            "description": repo.get("description"),
            "language": repo.get("language"),
            "languages": langs,
            "topics": repo.get("topics", []),
            "private": repo.get("private"),
            "fork": repo.get("fork"),
            "archived": repo.get("archived"),
            "size_kb": repo.get("size"),
            "default_branch": default_branch,
            "updated_at": repo.get("updated_at"),
            "pushed_at": repo.get("pushed_at"),
            "is_monorepo": is_monorepo,
            "branches": [{"name": b["name"], "sha": b["commit"]["sha"][:7], "full_sha": b["commit"]["sha"]} for b in branches[:20]],
            "commits": [
                {
                    "sha": c["sha"][:7],
                    "full_sha": c["sha"],
                    "message": (c["commit"]["message"].split("\n")[0])[:120],
                    "author": c["commit"]["author"].get("name"),
                    "date": c["commit"]["author"].get("date"),
                    "url": c.get("html_url"),
                }
                for c in commits[:20]
            ],
            "modules": local_modules,
            "file_count_local": None,
        }
        # count local files if exists
        p = projects_root / name
        if p.exists():
            try:
                cnt = sum(1 for _ in p.rglob("*") if _.is_file() and ".git" not in str(_.relative_to(p)) and "node_modules" not in str(_))
                entry["file_count_local"] = cnt
            except:
                pass
        inventory["repos"].append(entry)
        time.sleep(0.15)

    # graph fusion: deps communes (scan package.json)
    fusion = {"nodes": [], "links": []}
    dep_map = {}
    for repo in inventory["repos"]:
        if repo["name"] == "monorepo":
            continue
        # parse package.json deps if exists locally
        pj = projects_root / repo["name"] / "package.json"
        deps = []
        if pj.exists():
            try:
                j = json.loads(pj.read_text())
                deps = list((j.get("dependencies") or {}).keys()) + list((j.get("devDependencies") or {}).keys())
            except:
                pass
        dep_map[repo["name"]] = set(deps)
        fusion["nodes"].append({"id": repo["name"], "lang": repo["language"], "deps": deps, "modules": len(repo["modules"])})

    # links: shared deps >2 or explicit watchtower-mods etc
    names = list(dep_map.keys())
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            a, b = names[i], names[j]
            common = dep_map[a] & dep_map[b]
            if len(common) >= 2:
                fusion["links"].append({"source": a, "target": b, "weight": len(common), "common": sorted(list(common))[:8], "type": "shared-deps"})
    # explicit known relation COGNITORIUM -> watchtower via watchtower-mods
    has_cog = any(r["name"] == "COGNITORIUM" for r in inventory["repos"])
    has_wt = any(r["name"] == "watchtower" for r in inventory["repos"])
    if has_cog and has_wt:
        fusion["links"].append({"source": "COGNITORIUM", "target": "watchtower", "weight": 1, "common": ["watchtower-mods"], "type": "explicit"})

    inventory["fusion"] = fusion
    inventory["api_calls"] = total_api_calls

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(inventory, ensure_ascii=False, indent=2))
    print(f"✓ snapshot écrit: {out_path} ({len(inventory['repos'])} repos, {total_api_calls} appels API)")
    # also write MANIFEST
    manifest = {
        "generated_at": inventory["generated_at"],
        "user": user,
        "repos": [
            {"name": r["name"], "url": r["html_url"], "sha": (r["branches"][0]["full_sha"] if r["branches"] else None), "branch": r["default_branch"]}
            for r in inventory["repos"]
        ],
    }
    Path("MANIFEST.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    print("✓ MANIFEST.json écrit")

if __name__ == "__main__":
    main()
