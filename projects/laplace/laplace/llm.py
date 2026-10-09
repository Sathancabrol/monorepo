"""OpenAI-compatible chat client (Ollama by default, cloud optional)."""

from __future__ import annotations

from typing import Any

from openai import APIError, AsyncOpenAI

from .config import Settings


class LLMError(RuntimeError):
    """Provider failure translated to a user-safe error."""


class LLMClient:
    def __init__(
        self,
        settings: Settings,
        *,
        model: str | None = None,
        base_url: str | None = None,
        api_key: str | None = None,
    ) -> None:
        self.model = model or settings.llm_model
        self.base_url = base_url or settings.llm_base_url
        self._client = AsyncOpenAI(
            base_url=self.base_url,
            api_key=api_key if api_key is not None else settings.llm_api_key,
            timeout=settings.llm_timeout_seconds,
            max_retries=1,
        )

    async def complete(self, messages: list[dict[str, Any]]) -> str:
        try:
            result = await self._client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.6,
                max_tokens=900,
            )
        except (APIError, TimeoutError) as exc:
            raise LLMError("Le fournisseur de modèle n'a pas répondu.") from exc
        except Exception as exc:  # network libraries expose several timeout types
            raise LLMError("Le fournisseur de modèle n'a pas répondu.") from exc

        content = result.choices[0].message.content if result.choices else None
        if not content or not content.strip():
            raise LLMError("Le modèle a renvoyé une réponse vide.")
        return content.strip()

    async def close(self) -> None:
        await self._client.close()
