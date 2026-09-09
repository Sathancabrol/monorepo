"""Configuration centrale de NEXUS·OS (chemins, quotas, feature flags)."""
from __future__ import annotations

import os
from pathlib import Path

PKG = Path(__file__).resolve().parent
REPO_ROOT = PKG.parent

# --- Emplacements -----------------------------------------------------------
BUILTIN_SKILLS_DIR = PKG / "skills"
BUILTIN_AGENTS_DIR = PKG / "agents"
TEMPLATES_DIR = PKG / "templates"
STATIC_DIR = PKG / "static"

#: Racine "utilisateur" : base de données, mémoire, agents créés, fichiers produits.
#: Surchargeable via NEXUS_HOME (ex. pour les tests).
NEXUS_HOME = Path(os.environ.get("NEXUS_HOME", str(REPO_ROOT / ".nexus")))
DB_PATH = NEXUS_HOME / "nexus.sqlite3"
USER_AGENTS_DIR = NEXUS_HOME / "agents"
USER_SKILLS_DIR = NEXUS_HOME / "skills"
#: Sandbox : seuls les fichiers sous ce dossier peuvent être écrits par les outils.
WORKSPACE_DIR = NEXUS_HOME / "workspace"
MEMORY_FILE = NEXUS_HOME / "memory.json"

#: Racine lisible par les outils de lecture (le dépôt complet, en lecture seule).
READ_ROOT = REPO_ROOT


def env_flag(name: str, default: bool = False) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on", "oui"}


# --- Garde-fous -------------------------------------------------------------
#: Exécution shell/python par les agents. Désactivée par défaut : un agent ne
#: lance rien sur la machine tant que tu ne l'as pas explicitement autorisé.
ALLOW_SHELL = env_flag("NEXUS_ALLOW_SHELL", False)
#: Accès réseau sortant depuis les outils (http_get / web_search).
ALLOW_NETWORK = env_flag("NEXUS_ALLOW_NETWORK", True)
SHELL_TIMEOUT = int(os.environ.get("NEXUS_SHELL_TIMEOUT", "30"))
MAX_WRITE_BYTES = 2_000_000
MAX_READ_BYTES = 400_000

# --- Routeur ----------------------------------------------------------------
#: Quota de tokens par jour et par fournisseur (0 = illimité). Dépassement =>
#: bascule automatique sur le fournisseur suivant de la chaîne.
DAILY_TOKEN_BUDGET = int(os.environ.get("NEXUS_DAILY_TOKEN_BUDGET", "1_500_000"))
#: Préférer les modèles gratuits à capacité égale (comportement "OmniRoute").
PREFER_FREE = env_flag("NEXUS_PREFER_FREE", True)
REQUEST_TIMEOUT = int(os.environ.get("NEXUS_REQUEST_TIMEOUT", "60"))
#: Fichier où l'utilisateur peut poser ses clés sans passer par l'env.
SECRETS_FILE = NEXUS_HOME / "secrets.env"

# --- Runtime ----------------------------------------------------------------
MAX_AGENT_STEPS = int(os.environ.get("NEXUS_MAX_STEPS", "8"))
MAX_TOOL_RESULT_CHARS = 6000


def secret(key: str) -> str | None:
    """Clé API : variable d'environnement d'abord, puis .nexus/secrets.env."""
    val = os.environ.get(key)
    if val:
        return val.strip()
    if SECRETS_FILE.exists():
        for line in SECRETS_FILE.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            if k.strip() == key:
                return v.strip().strip("'\"") or None
    return None


def ensure_dirs() -> None:
    for d in (NEXUS_HOME, USER_AGENTS_DIR, USER_SKILLS_DIR, WORKSPACE_DIR):
        d.mkdir(parents=True, exist_ok=True)


ensure_dirs()
