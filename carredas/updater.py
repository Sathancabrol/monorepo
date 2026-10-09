"""Mise à jour depuis Git (canal principal) ou depuis une release publiée.

Deux canaux, dans cet ordre de préférence :

**git** — le poste exécute une copie de travail du dépôt. On interroge
`ls-remote` pour connaître la dernière étiquette, on compare, et on `checkout`
sur l'étiquette choisie. Avantage : gratuit, aucune infra à héberger, historique
complet, retour arrière instantané.

**release** — pour un poste installé via l'installeur (pas de dépôt local). On
interroge l'API GitHub, on télécharge l'archive, on vérifie son empreinte
SHA-256 si elle est fournie, on sauvegarde l'existant, on remplace, et on garde
la sauvegarde pour annuler.

Trois règles que je ne transige pas :
  * on ne met jamais à jour sans avoir une sauvegarde exploitable ;
  * on ne met jamais à jour si la copie de travail est sale (modifications non
    enregistrées) sans le dire explicitement ;
  * le retour arrière est toujours disponible.
"""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess
import time
from pathlib import Path

from . import __version__, log, paths

GIT_TIMEOUT = 45


# ------------------------------------------------------------------ utilitaires


def _git(repo: Path, *args, check=False):
    try:
        r = subprocess.run(["git", "-C", str(repo), *args],
                           capture_output=True, text=True, timeout=GIT_TIMEOUT)
        if check and r.returncode != 0:
            raise RuntimeError((r.stderr or r.stdout).strip()[:300])
        return r
    except FileNotFoundError:
        raise RuntimeError("git n'est pas installé ou n'est pas dans le PATH")
    except subprocess.TimeoutExpired:
        raise RuntimeError("git a dépassé le délai d'attente")


def _est_un_depot(p: Path) -> bool:
    return (p / ".git").exists()


def _http_json(url: str, timeout: int = 20):
    import urllib.request
    req = urllib.request.Request(url, headers={"User-Agent": "CarreDAs",
                                               "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _vplus(a: str, b: str) -> bool:
    """Compare deux versions 'x.y.z' ; True si a > b."""
    def k(v):
        v = str(v or "0").lstrip("v")
        out = []
        for part in v.split("-")[0].split("."):
            out.append(int(part) if part.isdigit() else 0)
        return out + [0] * (3 - len(out))
    return k(a) > k(b)


def _etat_maj() -> dict:
    return paths.read_config().get("mises_a_jour") or {}


def _ecrire_etat(patch: dict):
    cfg = paths.read_config()
    cfg.setdefault("mises_a_jour", {}).update(patch)
    cfg["mises_a_jour"]["dernier_controle"] = time.strftime("%Y-%m-%d %H:%M:%S")
    paths.write_config(cfg)
    return cfg["mises_a_jour"]


# ------------------------------------------------------------------ vérification


def verifier(cfg: dict | None = None) -> dict:
    """Regarde s'il existe une version plus récente. Ne modifie rien."""
    cfg = cfg or paths.read_config()
    maj = cfg.get("mises_a_jour") or {}
    canal = maj.get("canal") or "git"
    actuelle = __version__
    out = {"canal": canal, "actuelle": actuelle, "disponible": None,
           "a_jour": True, "message": "", "etiquettes": [], "sale": False,
           "depot_local": False}

    if not maj.get("actif", True):
        out["message"] = "mises à jour désactivées dans la configuration"
        out["a_jour"] = True
        return out

    # ---------- canal git ----------
    if canal == "git":
        repo = Path(maj.get("chemin_depot") or paths.code_dir())
        out["depot_local"] = _est_un_depot(repo)
        if not out["depot_local"]:
            out["message"] = ("pas de dépôt Git local : basculer sur le canal "
                              "'release' ou indiquer 'mises_a_jour.chemin_depot'")
            return out
        try:
            _git(repo, "fetch", "--tags", "--quiet", f"--timeout={GIT_TIMEOUT}")
        except Exception as exc:
            out["message"] = f"récupération impossible : {exc}"
            return out
        try:
            r = _git(repo, "tag", "--sort=-v:refname")
            etiquettes = [x.strip() for x in r.stdout.splitlines() if x.strip()]
            out["etiquettes"] = etiquettes[:12]
            if etiquettes:
                out["disponible"] = etiquettes[0]
        except Exception as exc:
            out["message"] = f"lecture des étiquettes impossible : {exc}"
            return out
        try:
            r = _git(repo, "status", "--porcelain")
            out["sale"] = bool(r.stdout.strip())
        except Exception:
            pass
        if out["disponible"]:
            out["a_jour"] = not _vplus(str(out["disponible"]).lstrip("v"), actuelle)
        if out["sale"]:
            out["message"] = ("la copie de travail contient des modifications non "
                              "enregistrées : enregistrez-les avant de mettre à jour")
        elif not out["a_jour"]:
            out["message"] = f"version {out['disponible']} disponible"
        else:
            out["message"] = "à jour"
        return out

    # ---------- canal release ----------
    if canal == "release":
        depot = maj.get("depot") or "Sathancabrol/monorepo"
        try:
            data = _http_json(f"https://api.github.com/repos/{depot}/releases/latest")
        except Exception as exc:
            out["message"] = f"interrogation impossible : {exc}"
            return out
        tag = (data.get("tag_name") or "").lstrip("v")
        out["disponible"] = tag
        out["a_jour"] = not _vplus(tag, actuelle)
        out["actifs"] = [{"nom": a.get("name"), "taille": a.get("size"),
                          "url": a.get("browser_download_url")}
                         for a in (data.get("assets") or [])]
        out["notes"] = (data.get("body") or "")[:4000]
        out["message"] = ("à jour" if out["a_jour"]
                          else f"version {tag} disponible")
        return out

    out["message"] = f"canal inconnu : {canal}"
    return out


# ------------------------------------------------------------------ application


def appliquer(cfg: dict, version: str = "", canal: str = "") -> dict:
    cfg = cfg or paths.read_config()
    maj = cfg.get("mises_a_jour") or {}
    canal = canal or maj.get("canal") or "git"
    if not maj.get("actif", True):
        return {"ok": False, "message": "mises à jour désactivées"}

    # sauvegarde systématique
    sauver = paths.backups_dir() / f"avant-maj-{time.strftime('%Y%m%d-%H%M%S')}"
    try:
        shutil.copytree(paths.data_dir(), sauver,
                        ignore=shutil.ignore_patterns("update", "backups"))
        log.info("maj", f"sauvegarde : {sauver}")
    except Exception as exc:
        log.warn("maj", f"sauvegarde impossible : {exc}")

    try:
        if canal == "git":
            return _appliquer_git(cfg, version)
        if canal == "release":
            return _appliquer_release(cfg, version)
        return {"ok": False, "message": f"canal inconnu : {canal}"}
    except Exception as exc:
        log.error("maj", f"échec : {exc}")
        return {"ok": False, "message": str(exc), "sauvegarde": str(sauver)}


def _appliquer_git(cfg: dict, version: str) -> dict:
    maj = cfg.get("mises_a_jour") or {}
    repo = Path(maj.get("chemin_depot") or paths.code_dir())
    if not _est_un_depot(repo):
        return {"ok": False, "message": "pas de dépôt Git local"}
    r = _git(repo, "status", "--porcelain")
    if r.stdout.strip():
        return {"ok": False,
                "message": "copie de travail modifiée : enregistrez ou annulez "
                           "vos modifications avant de mettre à jour",
                "sale": True}
    if not version:
        r = _git(repo, "tag", "--sort=-v:refname")
        tags = [x.strip() for x in r.stdout.splitlines() if x.strip()]
        version = tags[0] if tags else ""
    if not version:
        return {"ok": False, "message": "aucune étiquette disponible"}
    precedente = _git(repo, "rev-parse", "--short", "HEAD").stdout.strip()
    _git(repo, "checkout", version, check=True)
    _ecrire_etat({"derniere_version": version, "precedente": precedente})
    log.info("maj", f"bascule sur {version} (depuis {precedente})")
    return {"ok": True, "version": version, "precedente": precedente,
            "message": f"bascule sur {version} — redémarrage conseillé",
            "redemarrer": True}


def _appliquer_release(cfg: dict, version: str) -> dict:
    import io
    import urllib.request
    import zipfile

    maj = cfg.get("mises_a_jour") or {}
    depot = maj.get("depot") or "Sathancabrol/monorepo"
    data = _http_json(f"https://api.github.com/repos/{depot}/releases/latest")
    tag = data.get("tag_name") or ""
    if version and version not in (tag, tag.lstrip("v")):
        data = _http_json(f"https://api.github.com/repos/{depot}/releases/tags/{version}")
        tag = data.get("tag_name") or tag
    actifs = data.get("assets") or []
    if not actifs:
        return {"ok": False, "message": "aucun binaire publié pour cette version"}

    # on préfère l'installeur, sinon l'archive portable, sinon n'importe quoi d'utile
    pref = [a for a in actifs if a["name"].lower().endswith(".exe")] or \
           [a for a in actifs if a["name"].lower().endswith(".zip")]
    if not pref:
        return {"ok": False, "message": "aucun fichier exploitable dans la release"}
    actif = pref[0]
    url = actif["browser_download_url"]

    staging = paths.update_dir() / tag
    if staging.exists():
        shutil.rmtree(staging, ignore_errors=True)
    staging.mkdir(parents=True, exist_ok=True)
    fichier = staging / actif["name"]

    log.info("maj", f"téléchargement {actif['name']} ({actif.get('size')} o)")
    req = urllib.request.Request(url, headers={"User-Agent": "CarreDAs"})
    h = hashlib.sha256()
    with urllib.request.urlopen(req, timeout=120) as r, open(fichier, "wb") as f:
        while True:
            bloc = r.read(1 << 16)
            if not bloc:
                break
            h.update(bloc)
            f.write(bloc)
    empreinte = h.hexdigest()

    # vérification d'intégrité si le projet publie les empreintes
    sommes = next((a for a in actifs if a["name"].lower() == "sha256sums.txt"), None)
    if sommes:
        with urllib.request.urlopen(sommes["browser_download_url"], timeout=30) as r:
            attendu = [l.split()[0] for l in r.read().decode().splitlines()
                       if actif["name"] in l]
        if attendu and attendu[0].lower() != empreinte:
            return {"ok": False, "message": "empreinte SHA-256 invalide — mise à jour annulée",
                    "attendu": attendu[0], "obtenu": empreinte}

    _ecrire_etat({"derniere_version": tag, "staging": str(staging),
                  "empreinte": empreinte})
    if actif["name"].lower().endswith(".zip"):
        with zipfile.ZipFile(fichier) as z:
            z.extractall(staging / "extrait")
        return {"ok": True, "version": tag, "message": f"{tag} prêt dans {staging}",
                "chemin": str(staging / "extrait"), "empreinte": empreinte,
                "redemarrer": True}
    return {"ok": True, "version": tag, "message": f"installeur téléchargé : {fichier}",
            "chemin": str(fichier), "empreinte": empreinte}


# --------------------------------------------------------------------- annuler


def annuler(cfg: dict | None = None) -> dict:
    """Retour arrière : étiquette précédente (git) ou restauration de sauvegarde."""
    cfg = cfg or paths.read_config()
    maj = cfg.get("mises_a_jour") or {}
    canal = maj.get("canal") or "git"
    if canal == "git":
        repo = Path(maj.get("chemin_depot") or paths.code_dir())
        precedente = maj.get("precedente")
        if not precedente:
            return {"ok": False, "message": "aucune version précédente connue"}
        try:
            r = _git(repo, "status", "--porcelain")
            if r.stdout.strip():
                return {"ok": False, "message": "copie de travail modifiée", "sale": True}
            _git(repo, "checkout", precedente, check=True)
            _ecrire_etat({"derniere_version": precedente, "precedente": ""})
            return {"ok": True, "version": precedente, "redemarrer": True}
        except Exception as exc:
            return {"ok": False, "message": str(exc)}

    d = paths.backups_dir()
    if not d.exists():
        return {"ok": False, "message": "aucune sauvegarde disponible"}
    saves = sorted([p for p in d.iterdir() if p.is_dir()],
                   key=lambda p: p.stat().st_mtime, reverse=True)
    if not saves:
        return {"ok": False, "message": "aucune sauvegarde disponible"}
    cible = paths.data_dir()
    try:
        shutil.rmtree(cible, ignore_errors=True)
        shutil.copytree(saves[0], cible)
        return {"ok": True, "message": f"données restaurées depuis {saves[0].name}",
                "redemarrer": True}
    except Exception as exc:
        return {"ok": False, "message": str(exc)}
