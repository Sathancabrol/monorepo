#!/usr/bin/env python3
"""Read-only GitHub portfolio audit. Runtime health is never inferred from file presence."""
from __future__ import annotations

import datetime as dt
import html
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "data" / "audit" / "portfolio.json"
OUT = ROOT / "reports" / "project-audit"
API = "https://api.github.com"
NOW = dt.datetime.now(dt.timezone.utc)


def request_json(url: str):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "project-portfolio-audit/1.0",
    }
    token = os.getenv("GH_AUDIT_TOKEN") or os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            return json.loads(response.read().decode("utf-8")), None
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:500]
        return None, f"HTTP {exc.code}: {detail}"
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"


def request_pages(url: str):
    rows = []
    page = 1
    while True:
        separator = "&" if "?" in url else "?"
        data, error = request_json(f"{url}{separator}per_page=100&page={page}")
        if error:
            return rows, error
        if not isinstance(data, list):
            return rows, "unexpected paginated response"
        rows.extend(data)
        if len(data) < 100:
            return rows, None
        page += 1


def parse_date(value):
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def audit_repo(owner: str, item: dict) -> dict:
    name = item["name"]
    full_name = f"{owner}/{name}"
    base = f"{API}/repos/{full_name}"
    meta, error = request_json(base)
    result = {
        "name": name,
        "full_name": full_name,
        "role": item.get("role", ""),
        "priority": item.get("priority", "P2"),
        "url": f"https://github.com/{full_name}",
        "status": "error" if error else "audited",
        "errors": [],
        "default_branch": None,
        "branch_count": None,
        "focus_branches": [],
        "metrics": {},
        "signals": {},
        "recommendations": [],
        "runtime_status": "not_tested",
    }
    if error:
        result["errors"].append(f"repository metadata: {error}")
        result["status"] = "inaccessible_or_missing"
        return result

    default_branch = meta.get("default_branch")
    result["default_branch"] = default_branch
    result["is_private"] = meta.get("private", False)
    result["archived"] = meta.get("archived", False)
    result["updated_at"] = meta.get("updated_at")
    result["pushed_at"] = meta.get("pushed_at")
    last_push = parse_date(meta.get("pushed_at"))
    result["days_since_push"] = max(0, (NOW - last_push).days) if last_push else None

    branches, branch_error = request_pages(f"{base}/branches")
    branch_map = {}
    if branch_error:
        result["errors"].append(f"branches: {branch_error}")
    if branches:
        branch_map = {b.get("name"): b for b in branches}
        result["branch_count"] = len(branches)
    result["branch_inventory_complete"] = branch_error is None

    branch_names = []
    for candidate in [default_branch] + item.get("focus_branches", []):
        if candidate and candidate not in branch_names:
            branch_names.append(candidate)
    selected = []
    for branch_name in branch_names:
        branch_info = branch_map.get(branch_name)
        if not branch_info:
            selected.append({
                "name": branch_name,
                "exists": None if branch_error else False,
                "tree_readable": False,
                "lookup_status": "unknown_due_to_branch_error" if branch_error else "not_found",
            })
            continue
        sha = (branch_info.get("commit") or {}).get("sha")
        tree, tree_error = request_json(f"{base}/git/trees/{urllib.parse.quote(sha or '', safe='')}?recursive=1")
        if tree_error or not isinstance(tree, dict):
            result["errors"].append(f"tree {branch_name}: {tree_error or 'unexpected response'}")
            selected.append({"name": branch_name, "exists": True, "sha": sha, "tree_readable": False})
            continue
        entries = tree.get("tree", [])
        tree_truncated = bool(tree.get("truncated", False))
        if tree_truncated:
            result["errors"].append(f"tree {branch_name}: GitHub returned a truncated tree")
        paths = [entry.get("path", "") for entry in entries if entry.get("type") == "blob"]
        lower_paths = [p.lower() for p in paths]
        docs = [p for p in paths if p.lower().startswith(("docs/", "doc/")) or p.lower().endswith((".md", ".rst"))]
        tests = [p for p in paths if "test" in p.lower() and p.lower().endswith((".py", ".js", ".ts", ".tsx", ".jsx", ".json", ".yml", ".yaml"))]
        workflows = [p for p in paths if p.startswith(".github/workflows/") and p.lower().endswith((".yml", ".yaml"))]
        manifests = [p for p in paths if Path(p).name.lower() in {
            "pyproject.toml", "requirements.txt", "package.json", "pnpm-lock.yaml",
            "poetry.lock", "cargo.toml", "go.mod", "dockerfile", "makefile"
        }]
        source_files = [p for p in paths if p.lower().endswith((".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".cs"))]
        readme = any(Path(p).name.lower().startswith("readme") for p in paths)
        signal_paths = item.get("signals", [])
        signal_results = {s: any(p == s or p.startswith(s.rstrip("/") + "/") for p in paths) for s in signal_paths}
        selected.append({
            "name": branch_name,
            "exists": True,
            "sha": sha,
            "tree_readable": True,
            "tree_truncated": tree_truncated,
            "file_count": len(paths),
            "docs_count": len(docs),
            "test_file_count": len(tests),
            "workflow_count": len(workflows),
            "manifest_count": len(manifests),
            "source_file_count": len(source_files),
            "readme_present": readme,
            "signal_paths": signal_results,
            "sample_workflows": workflows[:10],
            "sample_tests": tests[:10],
        })
    result["focus_branches"] = selected
    default = next((b for b in selected if b["name"] == default_branch), None)
    if default and default.get("tree_readable") and not default.get("tree_truncated"):
        result["metrics"] = {
            "file_count": default.get("file_count", 0),
            "docs_count": default.get("docs_count", 0),
            "test_file_count": default.get("test_file_count", 0),
            "workflow_count": default.get("workflow_count", 0),
            "manifest_count": default.get("manifest_count", 0),
            "source_file_count": default.get("source_file_count", 0),
        }
        result["signals"] = {
            "readme_present": default.get("readme_present", False),
            "has_documentation_signal": default.get("docs_count", 0) > 0,
            "has_test_signal": default.get("test_file_count", 0) > 0,
            "has_ci_signal": default.get("workflow_count", 0) > 0,
            "has_source_signal": default.get("source_file_count", 0) > 0,
            "all_configured_paths_present": all(default.get("signal_paths", {}).values()) if item.get("signals") else None,
        }
    else:
        if not default or not default.get("tree_readable"):
            result["errors"].append("default branch tree could not be inspected")
        elif default.get("tree_truncated"):
            result["errors"].append("default branch metrics withheld because the tree is truncated")
    if result.get("days_since_push") is not None and result["days_since_push"] >= 30:
        result["recommendations"].append("Review stale activity: last push is at least 30 days old.")
    if not result["signals"].get("has_documentation_signal", False):
        result["recommendations"].append("Add or identify a maintained documentation entry point.")
    if not result["signals"].get("has_test_signal", False):
        result["recommendations"].append("Add an automated test signal; inspect actual test quality separately.")
    if not result["signals"].get("has_ci_signal", False):
        result["recommendations"].append("Add CI or document why automated CI is not applicable.")
    if result.get("branch_count") is not None and result["branch_count"] >= 10:
        result["recommendations"].append("Review branch inventory and identify merge, archive or preservation decisions.")
    if result["errors"]:
        result["recommendations"].append("Resolve audit/API errors before treating this repository as fully assessed.")
    result["recommendations"] = list(dict.fromkeys(result["recommendations"]))
    return result


def percent(n, d):
    return round(100 * n / d, 1) if d else 0.0


def build_kpis(repos: list[dict], configured_count: int) -> dict:
    audited = [r for r in repos if r["status"] == "audited"]
    available = [r for r in audited if r.get("signals")]
    return {
        "repositories_configured": configured_count,
        "repositories_audited": len(audited),
        "audit_coverage_pct": percent(len(audited), configured_count),
        "repositories_with_documentation_signal": sum(bool(r.get("signals", {}).get("has_documentation_signal")) for r in available),
        "documentation_signal_coverage_pct": percent(sum(bool(r.get("signals", {}).get("has_documentation_signal")) for r in available), len(available)),
        "repositories_with_test_signal": sum(bool(r.get("signals", {}).get("has_test_signal")) for r in available),
        "test_signal_coverage_pct": percent(sum(bool(r.get("signals", {}).get("has_test_signal")) for r in available), len(available)),
        "repositories_with_ci_signal": sum(bool(r.get("signals", {}).get("has_ci_signal")) for r in available),
        "ci_signal_coverage_pct": percent(sum(bool(r.get("signals", {}).get("has_ci_signal")) for r in available), len(available)),
        "repositories_with_source_signal": sum(bool(r.get("signals", {}).get("has_source_signal")) for r in available),
        "repositories_with_audit_errors": sum(bool(r.get("errors")) for r in repos),
        "runtime_tests_executed": 0,
        "runtime_health_verified": False,
    }


def markdown_report(report: dict) -> str:
    k = report["kpis"]
    source = report.get("generated_from", {})
    lines = [
        "# Automated project audit",
        "",
        f"> Generated at {report['generated_at']} from {source.get('ref', 'unknown')} @ {source.get('sha', 'unknown')} · Read-only GitHub inventory. File presence is not proof of runtime health.",
        "",
        "## Portfolio KPIs",
        "",
        "| KPI | Current value | Interpretation |",
        "|---|---:|---|",
        f"| Repository audit coverage | {k['audit_coverage_pct']}% ({k['repositories_audited']}/{k['repositories_configured']}) | Repositories whose metadata was read successfully |",
        f"| Documentation signal coverage | {k['documentation_signal_coverage_pct']}% | At least one docs/ or Markdown signal; not a quality score |",
        f"| Test signal coverage | {k['test_signal_coverage_pct']}% | Test-like files found; tests have not been run |",
        f"| CI signal coverage | {k['ci_signal_coverage_pct']}% | GitHub Actions workflow files found |",
        f"| Source-code signal | {k['repositories_with_source_signal']} repositories | Source-like files found |",
        f"| Repositories with audit errors | {k['repositories_with_audit_errors']} | Must be resolved before relying on completeness |",
        f"| Runtime verification | {'Yes' if k['runtime_health_verified'] else 'No'} | Separate local/CI test execution required |",
        "",
        "## Repository status",
        "",
        "| Priority | Repository | Default branch | Branch inventory | Files | Docs | Test files | CI workflows | Days since push | Audit status | Errors |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for r in report["repositories"]:
        m = r.get("metrics", {})
        errors = "; ".join(r.get("errors", [])) or "—"
        errors = errors.replace("|", "\\|").replace("\n", " ")
        lines.append(
            f"| {r.get('priority','')} | [{r['name']}]({r['url']}) | {r.get('default_branch') or '—'} | "
            f"{'complete' if r.get('branch_inventory_complete') else 'incomplete'} | "
            f"{m.get('file_count','—')} | {m.get('docs_count','—')} | {m.get('test_file_count','—')} | "
            f"{m.get('workflow_count','—')} | {r.get('days_since_push','—')} | {r['status']} | {errors} |"
        )
    lines += ["", "## Automatically generated next actions", ""]
    actions = []
    for r in report["repositories"]:
        for recommendation in r.get("recommendations", []):
            actions.append((r.get("priority", "P2"), r["name"], recommendation))
    rank = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    actions.sort(key=lambda x: (rank.get(x[0], 9), x[1], x[2]))
    if not actions:
        lines.append("No rule-based actions generated. This does not mean the portfolio is complete.")
    else:
        for priority, repo, action in actions:
            lines.append(f"- **{priority} · {repo}** — {action}")
    lines += [
        "",
        "## Important limitations",
        "",
        "- This audit inspects repository metadata, branch names and file trees; it does not run project code.",
        "- Test-like filenames are a signal only. The test suite, coverage and pass/fail status are not inferred.",
        "- Branch lists are paginated; an interrupted inventory is flagged as incomplete and missing branches remain unknown rather than absent.",
        "- Recommendations are deterministic heuristics, not AI conclusions.",
        "- KPI targets are portfolio tracking goals, not claims of current quality.",
        "",
    ]
    return "\n".join(lines)


def html_report(report: dict) -> str:
    k = report["kpis"]
    source = report.get("generated_from", {})
    cards = [
        ("Audit coverage", f"{k['audit_coverage_pct']}%", f"{k['repositories_audited']} / {k['repositories_configured']} repos"),
        ("Docs signal", f"{k['documentation_signal_coverage_pct']}%", "Docs/Markdown detected"),
        ("Test signal", f"{k['test_signal_coverage_pct']}%", "Test-like files detected, not executed"),
        ("CI signal", f"{k['ci_signal_coverage_pct']}%", "Workflow files detected"),
        ("Audit errors", str(k["repositories_with_audit_errors"]), "Repos requiring inspection"),
    ]
    card_html = "".join(
        f'<article class="kpi"><div class="muted">{html.escape(label)}</div><strong>{html.escape(value)}</strong><div class="muted">{html.escape(note)}</div></article>'
        for label, value, note in cards
    )
    rows = []
    for r in report["repositories"]:
        m = r.get("metrics", {})
        rows.append("<tr>" + "".join([
            f'<td><a href="{html.escape(r["url"], quote=True)}">{html.escape(r["name"])}</a><small>{html.escape(r.get("role",""))}</small></td>',
            f'<td>{html.escape(r.get("priority",""))}</td>',
            f'<td>{html.escape(r.get("default_branch") or "—")}</td>',
            f'<td>{"complete" if r.get("branch_inventory_complete") else "incomplete"}</td>',
            f'<td>{m.get("file_count","—")}</td>',
            f'<td>{m.get("docs_count","—")}</td>',
            f'<td>{m.get("test_file_count","—")}</td>',
            f'<td>{m.get("workflow_count","—")}</td>',
            f'<td>{r.get("days_since_push","—")}</td>',
            f'<td><span class="status">{html.escape(r["status"])}</span></td>',
            f'<td>{html.escape("; ".join(r.get("errors", [])) or "—")}</td>',
        ]) + "</tr>")
    actions = []
    rank = {"P0": 0, "P1": 1, "P2": 2, "P3": 3}
    for r in report["repositories"]:
        for rec in r.get("recommendations", []):
            actions.append((rank.get(r.get("priority", "P2"), 9), r.get("priority", "P2"), r["name"], rec))
    actions.sort()
    action_html = "".join(f'<li><b>{html.escape(p)} · {html.escape(name)}</b> — {html.escape(rec)}</li>' for _, p, name, rec in actions)
    return f"""<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Portfolio Audit</title><style>
:root{{color-scheme:dark;--bg:#0b1020;--panel:#121a2b;--line:#27354c;--text:#e7eef9;--muted:#93a4bb;--accent:#75b7ff}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--text);font:14px/1.5 system-ui,Segoe UI,sans-serif}}
main{{max-width:1400px;margin:auto;padding:28px}}h1{{margin:0 0 6px;font-size:28px}}h2{{margin-top:30px}}.muted,small{{color:var(--muted)}}.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:22px 0}}
.kpi{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px}}.kpi strong{{display:block;font-size:30px;margin:6px 0}}
.table-wrap{{overflow:auto;border:1px solid var(--line);border-radius:12px}}table{{border-collapse:collapse;width:100%;min-width:850px;background:var(--panel)}}th,td{{text-align:left;padding:12px;border-bottom:1px solid var(--line)}}th{{color:var(--muted);font-weight:600}}a{{color:var(--accent)}}small{{display:block;margin-top:3px}}.status{{padding:3px 7px;border:1px solid var(--line);border-radius:6px}}li{{margin:8px 0}}.notice{{margin-top:20px;padding:14px;border:1px solid var(--line);border-radius:10px;color:var(--muted)}}
</style></head><body><main>
<h1>Project Portfolio Audit</h1><div class="muted">Généré le {html.escape(report['generated_at'])} depuis {html.escape(source.get('ref', 'unknown'))} @ {html.escape(source.get('sha', 'unknown'))} · inventaire automatisé en lecture seule</div>
<section class="grid">{card_html}</section>
<h2>Dépôts suivis</h2><div class="table-wrap"><table><thead><tr><th>Dépôt</th><th>Priorité</th><th>Branche principale</th><th>Inventaire branches</th><th>Fichiers</th><th>Docs</th><th>Fichiers test</th><th>Workflows CI</th><th>Jours depuis push</th><th>Audit</th><th>Erreurs</th></tr></thead><tbody>{''.join(rows)}</tbody></table></div>
<h2>Prochaines actions proposées</h2><ul>{action_html or '<li>Aucune action générée par les règles actuelles.</li>'}</ul>
<div class="notice"><b>Limite de preuve :</b> présence de fichiers ≠ tests réussis ≠ application fonctionnelle. L'audit actuel ne lance pas les projets et n'évalue pas la qualité scientifique ou métier des données.</div>
</main></body></html>"""


def main() -> int:
    if not CONFIG.exists():
        print(f"Missing portfolio config: {CONFIG}", file=sys.stderr)
        return 2
    config = json.loads(CONFIG.read_text(encoding="utf-8"))
    owner = config.get("owner", "Sathancabrol")
    repos = [audit_repo(owner, item) for item in config.get("repositories", [])]
    report = {
        "schema_version": 1,
        "generated_at": NOW.isoformat(),
        "generated_from": {
            "ref": os.getenv("GITHUB_REF") or os.getenv("GITHUB_REF_NAME") or "local-unrecorded",
            "sha": os.getenv("GITHUB_SHA") or "local-unrecorded",
        },
        "portfolio_name": config.get("portfolio_name", "Project portfolio"),
        "kpi_rules": config.get("kpi_rules", {}),
        "kpis": build_kpis(repos, len(config.get("repositories", []))),
        "repositories": repos,
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "latest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "latest.md").write_text(markdown_report(report), encoding="utf-8")
    (OUT / "index.html").write_text(html_report(report), encoding="utf-8")
    history = OUT / "history.jsonl"
    with history.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"generated_at": report["generated_at"], "kpis": report["kpis"]}, ensure_ascii=False) + "\n")
    print(json.dumps({"kpis": report["kpis"], "output": str(OUT)}, ensure_ascii=False, indent=2))
    return 0 if report["kpis"]["repositories_audited"] > 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
