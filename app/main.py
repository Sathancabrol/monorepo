import json
import mimetypes
import os
import subprocess
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse, PlainTextResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE = Path(__file__).resolve().parent.parent
PROJECTS = BASE / "projects"
DATA_SNAPSHOT = BASE / "data" / "github_inventory.json"
MANIFEST = BASE / "MANIFEST.json"

app = FastAPI(title="Sathancabrol Monorepo — Panorama & Preview")

templates = Jinja2Templates(directory=str(BASE / "app" / "templates"))
# ensure mimetypes for wasm, etc.
mimetypes.add_type("application/wasm", ".wasm")
mimetypes.add_type("text/javascript", ".js")
mimetypes.add_type("text/css", ".css")

# static for app assets (if any)
app_static = BASE / "app" / "static"
app_static.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(app_static)), name="static")

def load_snapshot():
    if DATA_SNAPSHOT.exists():
        try:
            return json.loads(DATA_SNAPSHOT.read_text())
        except:
            return None
    return None

def list_projects():
    if not PROJECTS.exists():
        return []
    out = []
    for p in sorted(PROJECTS.iterdir()):
        if p.is_dir() and not p.name.startswith("."):
            # detect preview availability
            preview_entry = detect_preview_entry(p.name)
            out.append({
                "name": p.name,
                "preview": preview_entry,
                "file_count": sum(1 for _ in p.rglob("*") if _.is_file() and ".git" not in str(_) and "node_modules" not in str(_)) if p.exists() else 0,
            })
    return out

def detect_preview_entry(project: str):
    """Return relative preview entry path if exists, else None"""
    base = PROJECTS / project
    candidates = [
        base / "dist" / "index.html",
        base / "build" / "index.html",
        base / "output" / "visual" / "index.html",
        base / "output" / "visual" / "d3_interactive.html",
        base / "learning" / "index.html",
        base / "learning" / "money-poc.html",
        base / "index.html",
        base / "README.md",
    ]
    for c in candidates:
        if c.exists():
            # return path relative to project root for preview routing
            rel = c.relative_to(base)
            return str(rel)
    return None

def safe_resolve(project: str, subpath: str) -> Path:
    if ".." in subpath or subpath.startswith("/"):
        # will be validated via resolve check below anyway
        pass
    base = (PROJECTS / project).resolve()
    target = (base / subpath).resolve() if subpath else base
    # prevent traversal
    if not str(target).startswith(str(base)):
        raise HTTPException(400, "Chemin invalide (traversal bloqué)")
    return target

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    snap = load_snapshot()
    projects = list_projects()
    # enrichment: map preview types
    return templates.TemplateResponse(request, "index.html", {"snapshot": snap, "projects": projects})

@app.get("/repos", response_class=HTMLResponse)
def repos_page(request: Request):
    snap = load_snapshot()
    return templates.TemplateResponse(request, "repos.html", {"snapshot": snap})

@app.get("/monorepo", response_class=HTMLResponse)
def monorepo_page(request: Request):
    projects = list_projects()
    snap = load_snapshot()
    return templates.TemplateResponse(request, "monorepo.html", {"projects": projects, "snapshot": snap})

# --- API ---
@app.get("/api/github/snapshot")
def api_snapshot():
    snap = load_snapshot()
    if not snap:
        raise HTTPException(404, "Snapshot non trouvé — lance /api/github/refresh")
    return JSONResponse(snap)

@app.get("/api/github/repos")
def api_repos():
    snap = load_snapshot()
    if not snap:
        raise HTTPException(404, "Snapshot manquant")
    return JSONResponse(snap.get("repos", []))

@app.get("/api/github/fusion")
def api_fusion():
    snap = load_snapshot()
    if not snap:
        raise HTTPException(404, "Snapshot manquant")
    return JSONResponse(snap.get("fusion", {}))

@app.post("/api/github/refresh")
def api_refresh():
    """Regénère le snapshot via le script d'inventaire (stdlib, token côté serveur)."""
    script = BASE / "scripts" / "github_inventory.py"
    env = os.environ.copy()
    # ensure token not logged
    try:
        res = subprocess.run(["python3", str(script)], cwd=str(BASE), env=env, capture_output=True, text=True, timeout=90)
        out = res.stdout[-4000:] if res.stdout else ""
        err = res.stderr[-4000:] if res.stderr else ""
        snap = load_snapshot()
        if res.returncode != 0:
            return JSONResponse({"ok": False, "returncode": res.returncode, "stdout": out, "stderr": err}, status_code=500)
        return {"ok": True, "snapshot": snap, "stdout_tail": out, "stderr_tail": err}
    except subprocess.TimeoutExpired:
        raise HTTPException(504, "Refresh timeout")
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/api/fs/list")
def api_fs_list(project: str = Query(...), path: str = Query("", description="chemin relatif")):
    if not (PROJECTS / project).exists():
        raise HTTPException(404, f"Projet inconnu: {project}")
    target = safe_resolve(project, path)
    if not target.exists():
        raise HTTPException(404, "Chemin introuvable")
    if target.is_file():
        return {"type": "file", "name": target.name, "path": path, "size": target.stat().st_size}
    # directory
    entries = []
    try:
        for child in sorted(target.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
            if child.name.startswith(".git"):
                continue
            # hide huge node_modules from listing unless explicit? still list but flag
            is_dir = child.is_dir()
            entries.append({
                "name": child.name,
                "path": str(Path(path) / child.name) if path else child.name,
                "is_dir": is_dir,
                "size": child.stat().st_size if not is_dir else None,
                "ext": child.suffix.lower(),
            })
    except PermissionError:
        raise HTTPException(403, "Accès refusé")
    # breadcrumb
    parts = Path(path).parts if path else []
    breadcrumb = [{"name": project, "path": ""}]
    acc = ""
    for p in parts:
        acc = str(Path(acc) / p) if acc else p
        breadcrumb.append({"name": p, "path": acc})
    return {"type": "dir", "project": project, "path": path, "breadcrumb": breadcrumb, "entries": entries}

@app.get("/api/fs/file")
def api_fs_file(project: str = Query(...), path: str = Query(...)):
    if not (PROJECTS / project).exists():
        raise HTTPException(404, "Projet inconnu")
    target = safe_resolve(project, path)
    if not target.exists() or not target.is_file():
        raise HTTPException(404, "Fichier introuvable")
    # size guard: 2MB text max
    size = target.stat().st_size
    if size > 2_000_000:
        return {"name": target.name, "path": path, "size": size, "truncated": True, "content": target.read_text(errors="ignore")[:20000] + "\n\n... (fichier trop volumineux, tronqué)"}
    suffix = target.suffix.lower()
    # binary detection
    if suffix in [".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".pdf"]:
        # return meta, content via preview route
        return {"name": target.name, "path": path, "size": size, "binary": True, "mime": mimetypes.guess_type(str(target))[0]}
    try:
        text = target.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        raise HTTPException(500, f"Lecture échouée: {e}")
    # detect markdown
    return {"name": target.name, "path": path, "size": size, "content": text, "ext": suffix}

# preview static serving - MUST be after api
@app.get("/preview/{project}/{path:path}")
def preview_serve(project: str, path: str):
    # empty path => try preview entry
    if not (PROJECTS / project).exists():
        raise HTTPException(404, "Projet inconnu")
    if not path or path.strip() == "":
        entry = detect_preview_entry(project)
        if entry:
            path = entry
        else:
            # list directory as fallback
            return RedirectResponse(url=f"/monorepo?project={project}")
    target = safe_resolve(project, path)
    if not target.exists():
        # try index.html fallback for SPA
        # if path without extension and not existing, try serving project dist/index.html?
        # For SPA routing, serve project entry
        entry = detect_preview_entry(project)
        if entry:
            fallback = PROJECTS / project / entry
            if fallback.exists():
                # ensure we don't infinite loop
                if path not in ["", "index.html"] and "." not in Path(path).name:
                    return FileResponse(str(fallback), media_type="text/html")
        raise HTTPException(404, f"Fichier preview introuvable: {path}")
    if target.is_dir():
        # try index.html inside
        idx = target / "index.html"
        if idx.exists():
            return FileResponse(str(idx), media_type="text/html")
        # otherwise list
        raise HTTPException(404, "Dossier sans index.html — navigue via l'explorateur")
    # file
    mime = mimetypes.guess_type(str(target))[0] or "application/octet-stream"
    # for html, ensure iframe allowed (no X-Frame-Options) is handled by not setting deny headers globally
    return FileResponse(str(target), media_type=mime)

@app.get("/preview/{project}")
def preview_root(project: str):
    return preview_serve(project, "")

# bundle download (if exists)
@app.get("/download/monorepo.bundle")
def download_bundle():
    bundle = BASE / "monorepo.bundle"
    if not bundle.exists():
        # try alternative location
        raise HTTPException(404, "Bundle non généré sur ce serveur — génère avec scripts/publish_monorepo.sh")
    return FileResponse(str(bundle), media_type="application/octet-stream", filename="monorepo.bundle")

# legacy picture etc.
@app.get("/api/manifest")
def api_manifest():
    if MANIFEST.exists():
        return JSONResponse(json.loads(MANIFEST.read_text()))
    raise HTTPException(404, "MANIFEST manquant")


# =========================================================================
# AGENT OFFICE — dashboard lecture seule (mission M-001)
# Règle : « montre sans stocker » — chaque requête lit les fichiers, rien n'est écrit.
# =========================================================================
import csv
import datetime as _dt

AGENT_OFFICE = BASE / "projects" / "agent-office"
AO_DATA = AGENT_OFFICE / "data"


def _read_json(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def office_state():
    today = _dt.date.today().isoformat()
    # Budget (mois courant)
    budget = {"revenus": 0.0, "depenses": 0.0, "restant": None, "mois": today[:7]}
    csvp = AO_DATA / "budget_transactions.csv"
    if csvp.exists():
        try:
            with open(csvp, newline="", encoding="utf-8") as f:
                for row in csv.DictReader(f):
                    if not row.get("date", "").startswith(today[:7]):
                        continue
                    try:
                        m = float(row.get("montant", 0))
                    except ValueError:
                        continue
                    if row.get("type") == "revenu":
                        budget["revenus"] += m
                    else:
                        budget["depenses"] += m
            budget["restant"] = round(budget["revenus"] - budget["depenses"], 2)
        except Exception:
            pass
    # Tâches
    tasks = _read_json(AO_DATA / "tasks.json", []) or []
    tasks = sorted(tasks, key=lambda t: (t.get("date", ""), t.get("heure", "")))
    upcoming = [t for t in tasks if t.get("date", "") >= today]
    # Journal (5 dernières)
    journal = _read_json(AO_DATA / "update_journal.json", []) or []
    journal_last = journal[-5:][::-1]
    # Prospects
    prospects = _read_json(AO_DATA / "prospects.json", []) or []
    # Social
    social = _read_json(AO_DATA / "social_calendar.json", []) or []
    # Services (registre)
    tools = _read_json(AGENT_OFFICE / "tools.json", {}) or {}
    services = tools.get("services", [])
    # Missions
    missions = []
    mdir = AGENT_OFFICE / "agents" / "missions"
    if mdir.exists():
        for m in sorted(mdir.glob("M-*.md")):
            titre, statut = m.stem, "?"
            try:
                for line in m.read_text(encoding="utf-8").splitlines():
                    if line.startswith("# Mission"):
                        titre = line.lstrip("# ").strip()
                    if line.strip().startswith("- statut"):
                        statut = line.split(":", 1)[-1].strip()
            except Exception:
                pass
            missions.append({"fichier": m.name, "titre": titre, "statut": statut})
    # Signaux Watchtower
    signaux = _read_json(BASE / "projects" / "watchtower" / "data" / "thau-signaux.json", []) or []
    return {
        "genere_le": _dt.datetime.now().strftime("%d/%m/%Y %H:%M"),
        "budget": budget,
        "taches": tasks,
        "taches_a_venir": upcoming,
        "journal": journal_last,
        "journal_total": len(journal),
        "prospects": prospects,
        "social": social,
        "services": services,
        "missions": missions,
        "signaux": signaux,
        "nb_docs": len([f for f in (BASE / "docs").glob("*.md")]) if (BASE / "docs").exists() else 0,
    }


@app.get("/api/office/state")
def api_office_state():
    """Lecture seule : état du système agent-office, régénéré à chaque appel."""
    return JSONResponse(office_state())


@app.get("/office", response_class=HTMLResponse)
def office_page(request: Request):
    return templates.TemplateResponse(request, "office.html", office_state())
