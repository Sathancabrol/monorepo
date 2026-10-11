#!/usr/bin/env python3
"""Read-only branch-gap scanner. Tree discovery is not semantic or runtime verification."""
import datetime as dt
import json
import os
import urllib.parse
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG = ROOT / "data/audit/portfolio.json"
OUT = ROOT / "reports/project-audit"
INDEX = OUT / "branch-index.json"
API = "https://api.github.com"
BATCH = max(1, int(os.getenv("AUDIT_MAX_BRANCH_TREES", "15")))
KEYWORDS = ("carre", "carré", "nexus", "btp", "interface", "audit", "agent", "watchtower",
            "cognitorium", "research", "frontignan", "atlas", "tool", "memory", "preview",
            "rule", "policy", "instruction", "agent_handoff", "contributing", "decision", "standard")

def get_json(url):
    headers = {"Accept":"application/vnd.github+json", "X-GitHub-Api-Version":"2022-11-28",
               "User-Agent":"gap-driven-project-audit/1.0"}
    token = os.getenv("GH_AUDIT_TOKEN") or os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=25) as response:
            return json.loads(response.read().decode("utf-8")), None
    except urllib.error.HTTPError as exc:
        return None, "HTTP " + str(exc.code) + ": " + exc.read().decode("utf-8", errors="replace")[:250]
    except Exception as exc:
        return None, type(exc).__name__ + ": " + str(exc)

def load(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default

def all_pages(url):
    result, errors, page = [], [], 1
    while True:
        sep = "&" if "?" in url else "?"
        data, error = get_json(url + sep + "per_page=100&page=" + str(page))
        if error:
            errors.append(error)
            break
        if not isinstance(data, list):
            errors.append("Unexpected branch-list response")
            break
        result.extend(data)
        if len(data) < 100:
            break
        page += 1
    return result, errors

def main():
    cfg = load(CONFIG, {})
    previous = load(INDEX, {"branches": {}})
    old = previous.get("branches", {})
    current, candidates, errors = {}, [], []
    owner = cfg.get("owner", "Sathancabrol")
    for repo_cfg in cfg.get("repositories", []):
        repo = owner + "/" + repo_cfg["name"]
        meta, err = get_json(API + "/repos/" + repo)
        if err:
            errors.append({"repo":repo,"stage":"metadata","error":err})
            continue
        default = meta.get("default_branch", "main")
        branches, page_errors = all_pages(API + "/repos/" + repo + "/branches")
        errors.extend({"repo":repo,"stage":"branches","error":e} for e in page_errors)
        seen = set()
        for item in branches:
            name = item.get("name")
            sha = (item.get("commit") or {}).get("sha")
            if not name or not sha:
                continue
            seen.add(name)
            key = repo + "@" + name
            prior = old.get(key, {})
            changed = bool(prior and prior.get("sha") != sha)
            is_new = not bool(prior)
            status = prior.get("status", "unseen")
            if is_new or changed or status not in ("tree_inspected", "content_reviewed", "accepted_as_irrelevant"):
                status = "needs_tree_audit"
            rec = {
                "repo":repo,"branch":name,"sha":sha,"default_branch":default,
                "is_default":name == default,"new_branch":is_new,"changed_since_audit":changed,
                "status":status,"last_inspected_sha":prior.get("last_inspected_sha"),
                "last_inspected_at":prior.get("last_inspected_at"),
                "tree_file_count":prior.get("tree_file_count"),
                "relevant_paths":prior.get("relevant_paths",[]),
                "content_review_status":prior.get("content_review_status","not_started"),
                "evidence_url":"https://github.com/" + repo + "/tree/" + urllib.parse.quote(name, safe="/")
            }
            current[key] = rec
            if status == "needs_tree_audit":
                focus = name in repo_cfg.get("focus_branches", [])
                kw = any(word in name.lower() for word in KEYWORDS)
                score = (100 if focus else 0) + (80 if is_new else 0) + (60 if changed else 0) + (25 if kw else 0) + (10 if name == default else 0)
                candidates.append((score, key))
        for key, prior in old.items():
            if key.startswith(repo + "@") and prior.get("branch") not in seen and key not in current:
                gone = dict(prior)
                gone["status"] = "not_listed_now"
                current[key] = gone

    candidates.sort(key=lambda x: (-x[0], x[1]))
    audited = []
    for _, key in candidates[:BATCH]:
        rec = current[key]
        url = API + "/repos/" + rec["repo"] + "/git/trees/" + urllib.parse.quote(rec["sha"], safe="") + "?recursive=1"
        tree, err = get_json(url)
        rec["audit_attempted_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
        if err or not isinstance(tree, dict):
            rec["status"] = "tree_error"
            rec["tree_error"] = err or "Unexpected tree response"
            errors.append({"repo":rec["repo"],"branch":rec["branch"],"stage":"tree","error":rec["tree_error"]})
            continue
        paths = sorted(x.get("path","") for x in tree.get("tree",[]) if x.get("type") == "blob")
        relevant = [p for p in paths if any(w in p.lower() for w in
                    ("readme","audit","roadmap","agent","nexus","interface","carre","btp","module",
                     "manifest","test","workflow","architecture","memory","preview","registry","inventory",
                     "agents.md","claude.md","gemini.md","copilot_instructions","contributing","policy",
                     "rules","standard","handoff","decision","adr/","instructions","security"))
                    and p.lower().endswith((".md",".rst",".toml",".json",".yml",".yaml",".py",".ts",".tsx",".js",".jsx"))]
        rec.update({
            "status":"tree_inspected","last_inspected_sha":rec["sha"],
            "last_inspected_at":rec["audit_attempted_at"],"tree_file_count":len(paths),
            "relevant_paths":relevant[:250],"tree_truncated":bool(tree.get("truncated",False)),
            "content_review_status":"pending","tree_error":None
        })
        audited.append({"repo":rec["repo"],"branch":rec["branch"],"sha":rec["sha"],
                        "file_count":len(paths),"relevant_path_count":len(relevant)})

    pending = []
    for rec in current.values():
        if rec.get("status") in ("needs_tree_audit","tree_error") or rec.get("content_review_status") == "pending":
            pending.append({k:rec.get(k) for k in ("repo","branch","sha","status","new_branch",
                "changed_since_audit","content_review_status","tree_file_count","relevant_paths","evidence_url")})
    generated = dt.datetime.now(dt.timezone.utc).isoformat()
    OUT.mkdir(parents=True, exist_ok=True)
    INDEX.write_text(json.dumps({"schema_version":1,"generated_at":generated,"branches":current},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    report = {"generated_at":generated,"branches_indexed":len(current),"trees_inspected_this_run":len(audited),
              "pending_gaps":len(pending),"max_tree_audits_per_run":BATCH,"runtime_verified":False,
              "semantic_content_review_automated":False,"audited_this_run":audited,
              "pending":pending,"api_errors":errors}
    (OUT/"gaps.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    lines = ["# Gap-driven branch audit","","> Generated: "+generated,"",
             "Branch inventory is not proof of semantic review or runtime health.",
             "- Branches indexed: "+str(len(current)),
             "- Trees inspected this run: "+str(len(audited)),
             "- Pending gaps: "+str(len(pending)),
             "- API errors: "+str(len(errors)),"","## Pending evidence queue",""]
    for gap in sorted(pending,key=lambda x:(x.get("repo") or "",x.get("branch") or "")):
        lines += ["### "+str(gap.get("repo"))+" / "+str(gap.get("branch")),
                  "- Status: "+str(gap.get("status"))+"; content review: "+str(gap.get("content_review_status")),
                  "- SHA: "+str(gap.get("sha")),"- Evidence: "+str(gap.get("evidence_url"))]
        paths = gap.get("relevant_paths") or []
        if paths:
            lines.append("- Relevant paths:")
            lines.extend("  - "+p for p in paths[:40])
        else:
            lines.append("- Relevant paths: none identified; inspect the complete tree before closing.")
        lines.append("")
    if errors:
        lines += ["## API errors",""] + ["- "+e["repo"]+" ("+e["stage"]+"): "+e["error"] for e in errors]
    lines += ["","## Closure rule","","Close a gap only after reading relevant files and recording path, branch, SHA, date, finding, and next action. Tree inspection alone is not content review."]
    (OUT/"gaps.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
    print(json.dumps({"ok":True,"branches_indexed":len(current),"trees_inspected":len(audited),
                      "pending_gaps":len(pending),"api_errors":len(errors)}))

if __name__ == "__main__":
    main()
