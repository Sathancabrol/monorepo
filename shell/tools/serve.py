#!/usr/bin/env python3
"""Sert le dépôt en local pour regarder l'interface.

    python3 shell/tools/serve.py            # puis ouvrir http://localhost:8000
    python3 shell/tools/serve.py 9000       # autre port

« / » redirige vers la page d'accès (squelette, maquettes, ateliers).
Aucune dépendance : bibliothèque standard uniquement. À utiliser pour voir
les pages qui chargent des fichiers voisins (le double-clic `file://`
fonctionne aussi pour `shell/index.html`, qui est autonome).
"""
from __future__ import annotations

import os
import sys
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]   # la racine du dépôt
ENTRY = "/index-acces.html"


class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):  # noqa: N802 (nom imposé par la bibliothèque)
        if self.path in ("/", "/index.html"):
            self.send_response(302)
            self.send_header("Location", ENTRY)
            self.end_headers()
            return
        super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):  # journal discret
        if "404" in (fmt % args):
            super().log_message(fmt, *args)


def main() -> int:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    os.chdir(ROOT)
    with ThreadingHTTPServer(("0.0.0.0", port), partial(Handler, directory=str(ROOT))) as httpd:
        print(f"Carré d'As — accès : http://localhost:{port}{ENTRY}")
        print(f"racine servie : {ROOT}   (Ctrl+C pour arrêter)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\narrêt.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
