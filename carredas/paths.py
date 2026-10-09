"""Chemins, configuration et détection d'environnement.

Trois modes :
  * **portable**  : un fichier `PORTABLE` à côté du code → les données vivent dans
    `./data` (clé USB, dossier partagé).
  * **installé**  : données dans `%LOCALAPPDATA%\\CarreDAs` (Windows) ou
    `~/.local/share/CarreDAs` (Linux/macOS).
  * **dev**       : variable d'environnement `CARREDAS_DATA`.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

APP_NAME = "CarreDAs"
APP_TITLE = "Carré d'As"
CONFIG_FILE = "config.json"
PORTABLE_MARKER = "PORTABLE"


def is_frozen() -> bool:
    """True si l'on tourne dans un exécutable gelé (PyInstaller/Nuitka)."""
    return bool(getattr(sys, "frozen", False))


def code_dir() -> Path:
    """Dossier où vit le code (lecture seule en mode installé)."""
    if is_frozen():
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent.parent


def ui_dir() -> Path:
    return Path(__file__).resolve().parent / "ui"


def is_portable() -> bool:
    return (code_dir() / PORTABLE_MARKER).exists()


def data_dir() -> Path:
    env = os.environ.get("CARREDAS_DATA")
    if env:
        p = Path(env).expanduser()
    elif is_portable():
        p = code_dir() / "data"
    elif os.name == "nt":
        base = os.environ.get("LOCALAPPDATA") or str(Path.home() / "AppData" / "Local")
        p = Path(base) / APP_NAME
    else:
        base = os.environ.get("XDG_DATA_HOME") or str(Path.home() / ".local" / "share")
        p = Path(base) / APP_NAME
    p.mkdir(parents=True, exist_ok=True)
    return p


def update_dir() -> Path:
    p = data_dir() / "update"
    p.mkdir(parents=True, exist_ok=True)
    return p


def backups_dir() -> Path:
    p = data_dir() / "backups"
    p.mkdir(parents=True, exist_ok=True)
    return p


DEFAULT_CONFIG = {
    "version": 1,
    "profil": "agglo-thau",
    "territoire": {
        "nom": "Sète Agglopôle Méditerranée — Bassin de Thau",
        "communes": [
            "Sète", "Frontignan", "Balaruc-les-Bains", "Balaruc-le-Vieux",
            "Bouzigues", "Gigean", "Loupian", "Marseillan", "Mèze", "Mireval",
            "Montbazin", "Poussan", "Vic-la-Gardiole", "Villeveyrac",
        ],
        "population": 131000,
        "aire_scot_ha": 37340,
    },
    "llm": {
        "provider": "auto",          # auto | ollama | openai | none
        "ollama_url": "http://127.0.0.1:11434",
        "ollama_model": "qwen2.5:7b-instruct",
        "openai_url": "https://api.openai.com/v1",
        "openai_model": "gpt-4o-mini",
        "openai_key_env": "OPENAI_API_KEY",
        "timeout_s": 20,
    },
    "stt": {
        "provider": "auto",          # auto | whisper-cli | none
        "command": "",
        "model": "small",
        "langue": "fr",
    },
    "mises_a_jour": {
        "actif": True,
        "canal": "git",              # git | release | desactive
        "depot": "Sathancabrol/monorepo",
        "branche": "main",
        "verifier_au_demarrage": True,
    },
    "ui": {"theme": "nuit", "densite": "confortable"},
}


def _deep_merge(base: dict, over: dict) -> dict:
    out = dict(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def config_path() -> Path:
    return data_dir() / CONFIG_FILE


def read_config() -> dict:
    p = config_path()
    cfg = _deep_merge(DEFAULT_CONFIG, {})
    if p.exists():
        try:
            cfg = _deep_merge(DEFAULT_CONFIG, json.loads(p.read_text(encoding="utf-8")))
        except Exception:
            pass
    return cfg


def write_config(cfg: dict) -> dict:
    p = config_path()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(cfg, ensure_ascii=False, indent=2), encoding="utf-8")
    return cfg


def patch_config(fragment: dict) -> dict:
    return write_config(_deep_merge(read_config(), fragment))


def runtime_info() -> dict:
    import platform

    return {
        "app": APP_TITLE,
        "version_code": __import__("carredas").__version__,
        "python": platform.python_version(),
        "systeme": f"{platform.system()} {platform.release()}",
        "machine": platform.machine(),
        "gele": is_frozen(),
        "portable": is_portable(),
        "dossier_code": str(code_dir()),
        "dossier_donnees": str(data_dir()),
    }
