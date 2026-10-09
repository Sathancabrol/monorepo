#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Carré d'As — point d'entrée unique.

    python main.py                  ouvre la fenêtre du bureau
    python main.py --serve          sert l'interface (défaut : 127.0.0.1:8733)
    python main.py --port 8000      …sur un port précis
    python main.py --no-open        …sans ouvrir de navigateur
    python main.py --maj            vérifie et applique une mise à jour
    python main.py --verif-maj      vérifie seulement
    python main.py --version
    python main.py --donnees        ouvre le dossier de données

Aucune dépendance obligatoire : tout tourne avec la bibliothèque standard.
"""

from __future__ import annotations

import argparse
import os
import sys
import threading
import time
import webbrowser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from carredas import __version__, log, paths  # noqa: E402
from carredas.httpsrv import serve  # noqa: E402
from carredas.server import build  # noqa: E402

PORT_PAR_DEFAUT = 8733


def _ouvrir(url: str):
    time.sleep(0.6)
    try:
        webbrowser.open(url)
    except Exception:
        pass


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="carre-d-as",
        description="Carré d'As — point d'accès aux modules du monorepo")
    p.add_argument("--serve", action="store_true", help="servir l'interface sans fenêtre dédiée")
    p.add_argument("--port", type=int, default=PORT_PAR_DEFAUT)
    p.add_argument("--host", default="127.0.0.1",
                   help="127.0.0.1 par défaut ; 0.0.0.0 pour exposer sur le réseau local")
    p.add_argument("--no-open", action="store_true", help="ne pas ouvrir de navigateur")
    p.add_argument("--maj", action="store_true", help="vérifier puis appliquer la mise à jour")
    p.add_argument("--verif-maj", action="store_true", help="vérifier seulement")
    p.add_argument("--annuler-maj", action="store_true", help="revenir à la version précédente")
    p.add_argument("--version", action="store_true")
    p.add_argument("--donnees", action="store_true", help="ouvrir le dossier de données")
    p.add_argument("--config", action="store_true", help="afficher la configuration")
    p.add_argument("--verbose", "-v", action="store_true")
    a = p.parse_args(argv)

    if a.version:
        print(f"Carré d'As {__version__}")
        return 0
    if a.donnees:
        d = str(paths.data_dir())
        print(d)
        if os.name == "nt":
            os.startfile(d)  # noqa: S606
        return 0
    if a.config:
        import json
        print(json.dumps(paths.read_config(), ensure_ascii=False, indent=2))
        return 0

    cfg = paths.read_config()

    if a.verif_maj or a.maj or a.annuler_maj:
        from carredas import updater
        if a.annuler_maj:
            print(updater.annuler(cfg))
            return 0
        etat = updater.verifier(cfg)
        print(f"canal       : {etat['canal']}")
        print(f"actuelle    : {etat['actuelle']}")
        print(f"disponible  : {etat.get('disponible') or '—'}")
        print(f"message     : {etat['message']}")
        if a.verif_maj or etat.get("a_jour"):
            return 0
        if etat.get("sale"):
            print("\nCopie de travail modifiée — mise à jour refusée.")
            return 2
        print("\nApplication…")
        print(updater.appliquer(cfg, version=etat.get("disponible")))
        return 0

    router = build(cfg, verbose=a.verbose)
    url = None
    pret = threading.Event()

    def _pret(port):
        nonlocal url
        url = f"http://127.0.0.1:{port}/"
        pret.set()

    serve(router, host=a.host, port=a.port, ready=_pret, block=False)
    pret.wait(5)
    port_affiche = url.rsplit(":", 1)[-1].rstrip("/")
    print(f"\n  Carré d'As {__version__}")
    print(f"  Interface : {url}")
    print(f"  Données   : {paths.data_dir()}")
    print(f"  Ctrl+C pour arrêter\n")
    if url:
        try:
            from carredas.server import ICI
            ctx_path = paths.data_dir() / "derniere-url.txt"
            ctx_path.write_text(url, encoding="utf-8")
        except Exception:
            pass

    if a.serve:
        if not a.no_open:
            threading.Thread(target=_ouvrir, args=(url,), daemon=True).start()
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            print("\nArrêt.")
        return 0

    # mode bureau
    from carredas import desktop
    mode, proc = desktop.fenetre(url, "Carré d'As")
    if mode == "echec":
        print("  Impossible d'ouvrir une fenêtre :", url)
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            pass
        return 1
    if mode != "pywebview":
        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            print("\nArrêt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
