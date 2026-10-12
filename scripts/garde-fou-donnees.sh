#!/usr/bin/env bash
# garde-fou-donnees.sh — hook pre-commit : refuse d'ajouter des documents à un dépôt git.
#
# Pourquoi : au 2026-10-12, `Sathancabrol/monorepo` (public) contenait 480 fichiers bureautiques
# suivis (DCE, devis, factures, recours, grilles de salaires) et `proto-cognitorium` des CV de tiers.
# Ce hook empêche la récidive : les documents vivent dans `prive\`, hors de tout dépôt.
# Voir docs/PARAMETRAGE-HERMES/ALERTE-VISIBILITE-DEPOTS.md
#
# Installation (une fois par clone) :
#   cp scripts/garde-fou-donnees.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
#
# Autoriser volontairement un fichier : ajouter son chemin (ou un motif glob) à
# `docs/PUBLIC-AUTORISE.txt`, un par ligne, `#` pour commenter.
#
# Dérogation exceptionnelle : GARDE_FOU_OK=1 git commit …   (ou `git commit --no-verify`)
# Code de sortie : 0 = rien à signaler, 1 = commit refusé (règle n°8 : une vérification
# se termine par un code de sortie, jamais par un `| head` qui masque le résultat).

set -u

if [ "${GARDE_FOU_OK:-0}" = "1" ]; then
  echo "garde-fou-donnees: dérogation GARDE_FOU_OK=1 — vérification ignorée" >&2
  exit 0
fi

RACINE="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
cd "$RACINE" || exit 0

ALLOWLIST="$RACINE/docs/PUBLIC-AUTORISE.txt"
ZONES_OK='^(docs/|projects/[^/]+/(docs|audit|figures|visuals)/)'
EXT_RISQUE='pdf|xls|xlsx|xlsm|doc|docx|ppt|pptx|rtf|odt|ods|dwg|dxf|zip|7z|rar|tif|tiff|jpg|jpeg|png|gif|bmp|webp|heic'

# allowlist → tableau (motifs comparés sans découpage de mots, donc les espaces sont conservés)
motifs=()
if [ -f "$ALLOWLIST" ]; then
  while IFS= read -r ligne; do
    [ -n "$ligne" ] || continue
    case "$ligne" in \#*) continue ;; esac
    motifs+=("$ligne")
  done < "$ALLOWLIST"
fi

violations=0
liste=""
while IFS= read -r f; do
  [ -n "$f" ] || continue

  ext="$(printf '%s' "${f##*.}" | tr '[:upper:]' '[:lower:]')"
  printf '%s' "$ext" | grep -Eq "^(${EXT_RISQUE})$" || continue

  # zone de documentation autorisée (docs/, projects/*/docs|audit|figures|visuals)
  printf '%s' "$f" | grep -Eq "$ZONES_OK" && continue

  # exception explicite
  if [ "${#motifs[@]}" -gt 0 ]; then
    autorise=0
    for m in "${motifs[@]}"; do
      if [[ "$f" == $m ]]; then autorise=1; break; fi
    done
    [ "$autorise" = 1 ] && continue
  fi

  violations=$((violations + 1))
  liste="${liste}
  - ${f}"
done <<< "$(git diff --cached --name-only --diff-filter=ACMR)"

if [ "$violations" -gt 0 ]; then
  cat >&2 <<EOF

⛔ garde-fou-donnees : ${violations} fichier(s) qui n'ont rien à faire dans un dépôt git :
${liste}

Où ils vont :  G:\\PERSO\\PROJET COGNITORIUM\\prive\\   (jamais dans git, même un dépôt privé :
l'historique survit à la suppression du fichier).

Trois issues :
  1. les sortir de l'index        : git restore --staged <fichier>
  2. les déplacer dans prive\\    : (hors du dépôt, puis retirer du suivi)
  3. autoriser volontairement     : ajouter le chemin à docs/PUBLIC-AUTORISE.txt
     dérogation ponctuelle       : GARDE_FOU_OK=1 git commit …

Rappel : docs/PARAMETRAGE-HERMES/ALERTE-VISIBILITE-DEPOTS.md
EOF
  exit 1
fi

exit 0
