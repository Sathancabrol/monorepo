#!/usr/bin/env bash
set -euo pipefail
# Rebuild previews + push monorepo (utilise le remote déjà configuré)
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
echo "→ rebuild previews (base=./) ..."
for p in animation-chronos proto-cognitorium watchtower; do
  if [ -d "projects/$p" ]; then
    echo "  $p: npm ci + vite build --base=./"
    (cd "projects/$p" && npm ci --silent && npx vite build --base=./ --logLevel warn)
  fi
done
echo "→ git status"
git status --short
echo "→ git add"
git add -A
if git diff --cached --quiet; then
  echo "rien à committer"
else
  git commit -m "monorepo: sync projects + rebuild previews $(date -u +%Y-%m-%dT%H:%M:%SZ)"
fi
echo "→ push"
git push origin HEAD
echo "✓ done"
