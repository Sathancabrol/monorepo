"""Chargement de la configuration : fichier .env + config JSON.

Variables d'environnement attendues (via .env ou exportées) :
  MAIL_HOST            imap.gmail.com | outlook.office365.com | …
  MAIL_USER            adresse e-mail complète
  MAIL_APP_PASSWORD    mot de passe d'application (jamais le mot de passe normal)
  MAIL_PORT            (optionnel, défaut 993)
  MAIL_LIMIT           (optionnel, max de messages traités par passe)

Le config JSON définit les règles de tri ; à défaut de fichier, la
configuration par défaut (celle de config.example.json) est utilisée.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path

from .rules import Rule

MODULE_DIR = Path(__file__).resolve().parent.parent

DEFAULT_CONFIG_PATH = MODULE_DIR / "config.json"
EXAMPLE_CONFIG_PATH = MODULE_DIR / "config.example.json"
ENV_PATH = MODULE_DIR / ".env"

DEFAULT_SOURCE_FOLDER = "INBOX"
DEFAULT_FOLDER = "À trier"


def load_env_file(path: Path | str) -> None:
    """Charge un fichier .env simple (KEY=VALUE) sans écraser l'existant."""
    path = Path(path)
    if not path.is_file():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


@dataclass
class Settings:
    host: str
    user: str
    password: str
    port: int = 993
    source_folder: str = DEFAULT_SOURCE_FOLDER
    default_folder: str = DEFAULT_FOLDER
    rules: list[Rule] = field(default_factory=list)


def _load_rules_payload(path: Path | None) -> dict:
    candidates = [p for p in (path, DEFAULT_CONFIG_PATH, EXAMPLE_CONFIG_PATH) if p]
    for cand in candidates:
        cand = Path(cand)
        if cand.is_file():
            return json.loads(cand.read_text(encoding="utf-8"))
    return {"rules": [], "default_folder": DEFAULT_FOLDER}


def load_settings(config_path: Path | str | None = None,
                  env_path: Path | str | None = None) -> Settings:
    """Construit les Settings ; lève une erreur claire si credentials absentes."""
    load_env_file(env_path or ENV_PATH)

    host = os.environ.get("MAIL_HOST", "").strip()
    user = os.environ.get("MAIL_USER", "").strip()
    password = os.environ.get("MAIL_APP_PASSWORD", "").strip()

    missing = [name for name, val in (
        ("MAIL_HOST", host), ("MAIL_USER", user), ("MAIL_APP_PASSWORD", password),
    ) if not val]
    if missing:
        raise SystemExit(
            "Erreur : variables manquantes : " + ", ".join(missing) + "\n"
            f"Créez un fichier {ENV_PATH} contenant :\n"
            "  MAIL_HOST=imap.gmail.com            # ou outlook.office365.com\n"
            "  MAIL_USER=votre.adresse@gmail.com\n"
            "  MAIL_APP_PASSWORD=mot-de-passe-application\n"
            "(Voir README.md : comment générer un mot de passe d'application.)"
        )

    payload = _load_rules_payload(Path(config_path) if config_path else None)
    rules = [Rule.from_dict(r) for r in payload.get("rules", []) if "folder" in r]

    return Settings(
        host=host,
        user=user,
        password=password,
        port=int(os.environ.get("MAIL_PORT", "993")),
        source_folder=payload.get("source_folder", DEFAULT_SOURCE_FOLDER),
        default_folder=payload.get("default_folder", DEFAULT_FOLDER),
        rules=rules,
    )
