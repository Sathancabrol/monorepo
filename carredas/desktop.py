"""Lancement en fenêtre de bureau.

Trois stratégies, essayées dans l'ordre ; aucune n'est obligatoire :

1. **pywebview** si installé (`pip install pywebview`) : vraie fenêtre native,
   WebView2 sous Windows. C'est le mode recommandé.
2. **Mode application d'Edge ou de Chrome** : `--app=<url>` avec un profil
   dédié. Zéro dépendance, rendu identique à une application, barre d'outils
   masquée. Excellent repli, et suffisant pour un usage quotidien.
3. **Navigateur par défaut** : dernier recours, mais l'application reste
   entièrement utilisable ainsi — c'est la même interface.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

from . import log, paths

CANDIDATS_NAVIGATEURS = [
    ("Microsoft Edge",
     r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
     r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
    ("Google Chrome",
     r"C:\Program Files\Google\Chrome\Application\chrome.exe",
     r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
]

# navigateurs connus hors Windows (utile pour les tests et pour Linux/macOS)
CANDIDATS_POSIX = [
    ("Microsoft Edge", ["microsoft-edge", "microsoft-edge-stable"]),
    ("Google Chrome", ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser"]),
]


def _trouver_navigateur():
    if os.name == "nt":
        for nom, *chemins in CANDIDATS_NAVIGATEURS:
            for c in chemins:
                if Path(c).exists():
                    return nom, c
    else:
        for nom, binaires in CANDIDATS_POSIX:
            for b in binaires:
                p = shutil.which(b)
                if p:
                    return nom, p
    return None, None


def ouvrir_navigateur_app(url: str, titre: str = "Carré d'As") -> subprocess.Popen | None:
    nom, exe = _trouver_navigateur()
    if not exe:
        return None
    profil = paths.data_dir() / "profil-navigateur"
    profil.mkdir(parents=True, exist_ok=True)
    args = [exe, f"--app={url}", "--window-size=1440,940", "--window-position=60,40",
            f"--user-data-dir={profil}", "--no-first-run", "--no-default-browser-check",
            "--disable-features=Translate,TranslateUI",
            f"--app-id=carredas-local", "--allow-insecure-localhost"]
    if nom == "Microsoft Edge":
        args.append("--edge-skip-compat-check")
    try:
        p = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        log.info("bureau", f"fenêtre « {titre} » ouverte via {nom}")
        return p
    except Exception as exc:
        log.warn("bureau", f"ouverture impossible via {nom} : {exc}")
        return None


def ouvrir_defaut(url: str) -> bool:
    try:
        if os.name == "nt":
            os.startfile(url)  # noqa: S606
        elif sys.platform == "darwin":
            subprocess.Popen(["open", url])
        else:
            subprocess.Popen(["xdg-open", url])
        return True
    except Exception as exc:
        log.warn("bureau", f"ouverture par défaut impossible : {exc}")
        return False


def fenetre(url: str, titre: str = "Carré d'As", largeur=1440, hauteur=940):
    """Ouvre une vraie fenêtre. Rend `('pywebview'|'app'|'defaut'|'echec', proc)`."""
    try:
        import webview  # type: ignore
    except Exception:
        webview = None

    if webview is not None:
        try:
            webview.create_window(titre, url, width=largeur, height=hauteur,
                                  min_size=(1024, 640), background_color="#050508")
            webview.start(private_mode=False)
            return "pywebview", None
        except Exception as exc:
            log.warn("bureau", f"pywebview indisponible : {exc}")

    p = ouvrir_navigateur_app(url, titre)
    if p is not None:
        return "app", p

    if ouvrir_defaut(url):
        return "defaut", None
    return "echec", None
