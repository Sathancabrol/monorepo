"""Registre de modules : plug in / plug out.

Un module = un dossier avec un `module.json` (métadonnées + contrat) et un
`router.py` exposant `register(router, ctx)`. Rien d'autre n'est requis.
Pour désactiver un module : `module.json → {"actif": false}` ou suppression
du dossier. Le cœur ne connaît aucun module par son nom.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path
from types import ModuleType

from .. import log

MODULES_DIR = Path(__file__).parent


class Module:
    def __init__(self, dossier: Path):
        self.dossier = dossier
        self.manifest_path = dossier / "module.json"
        self.manifest: dict = {}
        self.error: str | None = None
        self._code: ModuleType | None = None
        if self.manifest_path.exists():
            try:
                self.manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
            except Exception as exc:
                self.error = f"module.json illisible : {exc}"

    # ---------- identité ----------
    @property
    def id(self) -> str:
        return self.manifest.get("id") or self.dossier.name

    @property
    def titre(self) -> str:
        return self.manifest.get("titre") or self.id

    @property
    def actif(self) -> bool:
        return bool(self.manifest.get("actif", True))

    @property
    def priorite(self) -> int:
        return int(self.manifest.get("priorite", 50))

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "titre": self.titre,
            "icone": self.manifest.get("icone", "◻"),
            "resume": self.manifest.get("resume", ""),
            "version": self.manifest.get("version", "0.0.0"),
            "actif": self.actif,
            "priorite": self.priorite,
            "obligatoire": bool(self.manifest.get("obligatoire", False)),
            "palier": self.manifest.get("palier", "P1"),
            "routes": self.manifest.get("routes", []),
            "erreur": self.error,
        }

    # ---------- chargement ----------
    def load(self) -> ModuleType | None:
        if not (self.dossier / "router.py").exists():
            self.error = "router.py absent"
            return None
        if self._code is not None:
            return self._code
        # le nom doit être assez profond pour que les imports relatifs
        # ('from ...store import …') remontent jusqu'au paquet carredas
        name = f"carredas.modules.{self.dossier.name}.router"
        try:
            spec = importlib.util.spec_from_file_location(name, self.dossier / "router.py")
            mod = importlib.util.module_from_spec(spec)
            sys.modules[name] = mod
            spec.loader.exec_module(mod)
            self._code = mod
            return mod
        except Exception as exc:
            self.error = f"échec au chargement : {exc}"
            log.error("modules", f"{self.id} : {exc}")
            return None

    def register(self, router, ctx) -> bool:
        code = self.load()
        if code is None or not hasattr(code, "register"):
            return False
        try:
            code.register(router, ctx)
            return True
        except Exception as exc:
            self.error = f"échec au câblage : {exc}"
            log.error("modules", f"{self.id} : {exc}")
            return False


def discover(root: Path = MODULES_DIR) -> list[Module]:
    out = []
    if not root.exists():
        return out
    for d in sorted(root.iterdir()):
        if not d.is_dir() or d.name.startswith(("_", ".")):
            continue
        if not (d / "module.json").exists():
            continue
        out.append(Module(d))
    out.sort(key=lambda m: (m.priorite, m.id))
    return out


def load_all(router, ctx, root: Path = MODULES_DIR) -> list[dict]:
    etat = []
    for m in discover(root):
        if not m.actif:
            log.info("modules", f"{m.id} désactivé")
            etat.append(m.to_dict())
            continue
        ok = m.register(router, ctx)
        info = m.to_dict()
        info["charge"] = ok
        etat.append(info)
        log.info("modules", f"{m.id} {'câblé' if ok else 'EN ÉCHEC'} — {m.titre}")
    return etat
