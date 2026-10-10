#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

if ! command -v python3 >/dev/null; then
  echo "Installe Python 3.11+ puis relance."
  exit 1
fi

if [[ ! -x .venv/bin/python ]]; then
  echo "Création de l'environnement Bone..."
  python3 -m venv .venv
fi
# shellcheck disable=SC1091
source .venv/bin/activate
python -m pip install -q --upgrade pip
python -m pip install -q -r requirements.txt

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo
  echo "Ouvre .env et colle : DISCORD_TOKEN=ton_token"
  echo "Puis relance : ./lancer.sh"
  ${EDITOR:-nano} .env || true
  exit 0
fi

if ! grep -qE '^DISCORD_TOKEN=.+' .env; then
  echo "DISCORD_TOKEN est vide dans .env"
  ${EDITOR:-nano} .env || true
  exit 1
fi

echo "Bone démarre. Ctrl+C pour arrêter."
exec python discord_bot.py
