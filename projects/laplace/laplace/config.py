"""Environment-based configuration with fail-closed Discord allowlists."""

from __future__ import annotations

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ConfigurationError(ValueError):
    """Raised when required configuration is missing or unsafe."""


def _required(env: Mapping[str, str], name: str) -> str:
    value = env.get(name, "").strip()
    if not value:
        raise ConfigurationError(f"{name} est requis; consulte .env.example.")
    return value


def _parse_ids(value: str, name: str, *, required: bool = False) -> frozenset[int]:
    raw_ids = [part.strip() for part in value.replace(";", ",").split(",") if part.strip()]
    parsed: set[int] = set()
    for raw in raw_ids:
        try:
            identifier = int(raw)
        except ValueError as exc:
            raise ConfigurationError(
                f"{name} doit contenir uniquement des IDs Discord numériques."
            ) from exc
        if identifier <= 0:
            raise ConfigurationError(f"{name} doit contenir des IDs Discord positifs.")
        parsed.add(identifier)
    if required and not parsed:
        raise ConfigurationError(f"{name} est requis et ne peut pas être vide.")
    return frozenset(parsed)


def _parse_bool(env: Mapping[str, str], name: str, default: bool) -> bool:
    value = env.get(name)
    if value is None or not value.strip():
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on", "oui"}:
        return True
    if normalized in {"0", "false", "no", "off", "non"}:
        return False
    raise ConfigurationError(f"{name} doit valoir true ou false.")


def _parse_int(
    env: Mapping[str, str], name: str, default: int, *, minimum: int, maximum: int
) -> int:
    raw = env.get(name, str(default)).strip()
    try:
        result = int(raw)
    except ValueError as exc:
        raise ConfigurationError(f"{name} doit être un entier.") from exc
    if not minimum <= result <= maximum:
        raise ConfigurationError(f"{name} doit être compris entre {minimum} et {maximum}.")
    return result


def _validate_base_url(value: str, name: str = "LLM_BASE_URL") -> str:
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ConfigurationError(f"{name} doit être une URL HTTP(S) valide.")
    if parsed.username or parsed.password:
        raise ConfigurationError(
            f"Ne place pas de secret dans {name}; utilise la variable API_KEY."
        )
    return value.rstrip("/")


@dataclass(frozen=True, slots=True)
class Settings:
    discord_bot_token: str
    allowed_guild_ids: frozenset[int]
    allowed_channel_ids: frozenset[int]
    owner_user_ids: frozenset[int]
    database_path: Path
    archive_retention_days: int
    private_responses: bool
    llm_provider: str
    llm_base_url: str
    llm_api_key: str
    llm_model: str
    vision_provider: str
    vision_base_url: str | None
    vision_api_key: str | None
    vision_model: str | None
    allow_external_vision: bool
    llm_timeout_seconds: int
    max_history_turns: int
    memory_top_k: int

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> Settings:
        if environ is None:
            load_dotenv(PROJECT_ROOT / ".env", override=False)
            env: Mapping[str, str] = os.environ
        else:
            env = environ

        token = _required(env, "DISCORD_BOT_TOKEN")
        guild_ids = _parse_ids(env.get("ALLOWED_GUILD_IDS", ""), "ALLOWED_GUILD_IDS", required=True)
        channel_ids = _parse_ids(env.get("ALLOWED_CHANNEL_IDS", ""), "ALLOWED_CHANNEL_IDS")
        owner_ids = _parse_ids(env.get("OWNER_USER_IDS", ""), "OWNER_USER_IDS", required=True)

        provider = env.get("LLM_PROVIDER", "ollama").strip().lower()
        if provider not in {"ollama", "openai_compatible"}:
            raise ConfigurationError("LLM_PROVIDER doit valoir ollama ou openai_compatible.")

        default_url = "http://127.0.0.1:11434/v1" if provider == "ollama" else ""
        base_url = _validate_base_url(env.get("LLM_BASE_URL", default_url).strip())
        api_key = env.get("LLM_API_KEY", "ollama" if provider == "ollama" else "").strip()
        if provider == "openai_compatible" and not api_key:
            raise ConfigurationError("LLM_API_KEY est requis pour le fournisseur API.")

        model = _required(env, "LLM_MODEL")
        if model.upper().startswith("REPLACE_"):
            raise ConfigurationError("Remplace LLM_MODEL par un modèle réellement disponible.")

        vision_model = env.get("VISION_MODEL", "").strip() or None
        vision_provider = env.get("VISION_PROVIDER", "ollama").strip().lower()
        if vision_provider not in {"ollama", "openai_compatible"}:
            raise ConfigurationError("VISION_PROVIDER doit valoir ollama ou openai_compatible.")
        allow_external_vision = _parse_bool(env, "ALLOW_EXTERNAL_VISION", False)
        vision_base_url: str | None = None
        vision_api_key: str | None = None
        if vision_model:
            if vision_provider == "openai_compatible":
                if not allow_external_vision:
                    raise ConfigurationError(
                        "Active ALLOW_EXTERNAL_VISION=true pour autoriser l'envoi d'images "
                        "à une API."
                    )
                vision_base_url = _validate_base_url(
                    _required(env, "VISION_BASE_URL"), "VISION_BASE_URL"
                )
                vision_api_key = _required(env, "VISION_API_KEY")
            else:
                vision_base_url = _validate_base_url(
                    env.get("VISION_BASE_URL", "http://127.0.0.1:11434/v1").strip(),
                    "VISION_BASE_URL",
                )
                vision_api_key = env.get("VISION_API_KEY", "ollama").strip() or "ollama"

        db_value = Path(env.get("DATABASE_PATH", "data/laplace.sqlite3").strip()).expanduser()
        database_path = db_value if db_value.is_absolute() else PROJECT_ROOT / db_value

        return cls(
            discord_bot_token=token,
            allowed_guild_ids=guild_ids,
            allowed_channel_ids=channel_ids,
            owner_user_ids=owner_ids,
            database_path=database_path,
            archive_retention_days=_parse_int(
                env, "ARCHIVE_RETENTION_DAYS", 30, minimum=0, maximum=3650
            ),
            private_responses=_parse_bool(env, "PRIVATE_RESPONSES", True),
            llm_provider=provider,
            llm_base_url=base_url,
            llm_api_key=api_key,
            llm_model=model,
            vision_provider=vision_provider,
            vision_base_url=vision_base_url,
            vision_api_key=vision_api_key,
            vision_model=vision_model,
            allow_external_vision=allow_external_vision,
            llm_timeout_seconds=_parse_int(env, "LLM_TIMEOUT_SECONDS", 90, minimum=5, maximum=300),
            max_history_turns=_parse_int(env, "MAX_HISTORY_TURNS", 6, minimum=0, maximum=20),
            memory_top_k=_parse_int(env, "MEMORY_TOP_K", 5, minimum=0, maximum=20),
        )
