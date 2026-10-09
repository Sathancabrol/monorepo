from __future__ import annotations

import pytest

from laplace.config import ConfigurationError, Settings


def valid_env(**overrides: str) -> dict[str, str]:
    values = {
        "DISCORD_BOT_TOKEN": "test-token-not-a-real-secret",
        "ALLOWED_GUILD_IDS": "123456789012345678",
        "OWNER_USER_IDS": "234567890123456789",
        "LLM_MODEL": "test-model",
    }
    values.update(overrides)
    return values


def test_settings_defaults_to_local_ollama_and_private_replies() -> None:
    settings = Settings.from_env(valid_env())
    assert settings.llm_provider == "ollama"
    assert settings.llm_base_url == "http://127.0.0.1:11434/v1"
    assert settings.private_responses is True
    assert settings.archive_retention_days == 30
    assert settings.allowed_guild_ids == frozenset({123456789012345678})
    assert settings.vision_model is None
    assert settings.allow_external_vision is False


def test_guild_and_owner_allowlists_are_required() -> None:
    with pytest.raises(ConfigurationError, match="ALLOWED_GUILD_IDS"):
        Settings.from_env(valid_env(ALLOWED_GUILD_IDS=""))
    with pytest.raises(ConfigurationError, match="OWNER_USER_IDS"):
        Settings.from_env(valid_env(OWNER_USER_IDS=""))


def test_invalid_provider_and_api_without_key_fail_closed() -> None:
    with pytest.raises(ConfigurationError, match="LLM_PROVIDER"):
        Settings.from_env(valid_env(LLM_PROVIDER="unknown"))
    with pytest.raises(ConfigurationError, match="LLM_API_KEY"):
        Settings.from_env(
            valid_env(
                LLM_PROVIDER="openai_compatible",
                LLM_BASE_URL="https://api.example.invalid/v1",
            )
        )


def test_url_credentials_are_not_accepted() -> None:
    with pytest.raises(ConfigurationError, match="secret"):
        Settings.from_env(valid_env(LLM_BASE_URL="https://user:password@example.invalid/v1"))


def test_retention_and_private_response_values_are_validated() -> None:
    with pytest.raises(ConfigurationError, match="ARCHIVE_RETENTION_DAYS"):
        Settings.from_env(valid_env(ARCHIVE_RETENTION_DAYS="4000"))
    with pytest.raises(ConfigurationError, match="PRIVATE_RESPONSES"):
        Settings.from_env(valid_env(PRIVATE_RESPONSES="maybe"))


def test_external_vision_requires_explicit_opt_in() -> None:
    settings = valid_env(
        VISION_PROVIDER="openai_compatible",
        VISION_BASE_URL="https://vision.example.invalid/v1",
        VISION_API_KEY="local-test-key",
        VISION_MODEL="vision-test",
    )
    with pytest.raises(ConfigurationError, match="ALLOW_EXTERNAL_VISION"):
        Settings.from_env(settings)

    configured = Settings.from_env({**settings, "ALLOW_EXTERNAL_VISION": "true"})
    assert configured.vision_provider == "openai_compatible"
    assert configured.vision_model == "vision-test"
    assert configured.allow_external_vision is True
