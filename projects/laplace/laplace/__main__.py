"""CLI entry point: python -m laplace."""

from __future__ import annotations

import logging
import sys

from .bot import build_bot
from .config import ConfigurationError, Settings


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    try:
        settings = Settings.from_env()
    except ConfigurationError as exc:
        print(f"Configuration invalide : {exc}", file=sys.stderr)
        raise SystemExit(2) from exc

    bot = build_bot(settings)
    # discord.py handles reconnects; the token is read only from the local environment.
    bot.run(settings.discord_bot_token, log_handler=None)


if __name__ == "__main__":
    main()
