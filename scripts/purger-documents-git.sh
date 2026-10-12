#!/usr/bin/env bash
# purger-documents-git.sh — retire des documents de TOUT l'historique d'un dépôt git.
#
# Pourquoi : passer un dépôt en privé arrête l'accès futur, mais ne supprime pas ce qui est déjà
# dans l'historique (et donc accessible par SHA). Pour des documents d'entreprise et surtout des
# données personnelles de tiers (CV, questionnaires), la suppression réelle demande une réécriture.
# Voir docs/PARAMETRAGE-HERMES/PURGE-HISTORIQUE.md
#
# GARANTIES DE SÉCURITÉ (c'est le point important) :
#   - le script ne touche JAMAIS ton clone de travail : il travaille sur un clone miroir à part ;
#   - sans --executer, il ne fait que compter et lister (--inventaire, --plan) ;
#   - il ne pousse rien sans --push ET --oui ;
#   - il refuse de démarrer s'il ne trouve pas git-filter-repo.
#
# Usage :
#   bash scripts/purger-documents-git.sh --inventaire
#   bash scripts/purger-documents-git.sh --plan
#   bash scripts/purger-documents-git.sh --executer --sortie "G:/PERSO/purge-2026-10-12"
#   bash scripts/purger-documents-git.sh --executer --sortie "…" --push --oui
#
# Motifs : fichier docs/PURGE-MOTIFS.txt (une ligne par motif, `#` pour commenter), préfixes :
#   glob:<motif>    → --path-glob  (le * traverse les /)
#   regex:<motif>   → --path-regex
#   path:<chemin>   → --path       (chemin exact)
#   <chemin nu>     → --path
# Sans ce fichier, la liste intégrée ci-dessous est utilisée.
#
# Codes de sortie : 0 = terminé, 1 = erreur/refus, 2 = mauvaise utilisation.

set -u

DEPOT="."
SORTIE=""
MOTIFS_FICHIER="docs/PURGE-MOTIFS.txt"
MODE=""
PUSH=0
OUI=0

MOTIFS_DEFAUT=(
  'regex:^[^/]+\.(pdf|xls|xlsx|xlsm|doc|docx|ppt|pptx|rtf)$'
  'glob:projects/*/raw/*'
)

while [ $# -gt 0 ]; do
  case "$1" in
    --inventaire|--plan|--executer) MODE="$1"; shift ;;
    --depot) DEPOT="$2"; shift 2 ;;
    --sortie) SORTIE="$2"; shift 2 ;;
    --motifs) MOTIFS_FICHIER="$2"; shift 2 ;;
    --push) PUSH=1; shift ;;
    --oui) OUI=1; shift ;;
    -h|--help) sed -n '2,29p' "$0"; exit 0 ;;
    *) echo "option inconnue : $1" >&2; exit 2 ;;
  esac
done

[ -n "$MODE" ] || { echo "il faut --inventaire, --plan ou --executer (voir --help)" >&2; exit 2; }
command -v git >/dev/null 2>&1 || { echo "git introuvable" >&2; exit 1; }

# --- motifs ------------------------------------------------------------------
MOTIFS=()
if [ -f "$MOTIFS_FICHIER" ]; then
  while IFS= read -r ligne; do
    [ -n "$ligne" ] || continue
    case "$ligne" in \#*) continue ;; esac
    MOTIFS+=("$ligne")
  done < "$MOTIFS_FICHIER"
  echo "motifs : $MOTIFS_FICHIER (${#MOTIFS[@]} motif(s) actif(s))"
else
  MOTIFS=("${MOTIFS_DEFAUT[@]}")
  echo "motifs : liste intégrée par défaut (${#MOTIFS[@]} motifs)"
fi

# extension « documentaire » (pour l'inventaire de reconnaissance uniquement)
motif_ext() { printf '%s' "$1" | grep -Eqi '\.(pdf|xls|xlsx|xlsm|doc|docx|ppt|pptx|rtf|odt|ods|dwg|dxf|zip|7z|rar|tif|tiff|jpg|jpeg|png|gif|bmp|webp|heic)$'; }

# le chemin correspond-il à un motif ACTIF (ce que la purge retirera réellement) ?
correspond_motif() { # $1 = chemin, $2 = motif
  case "$2" in
    regex:*) printf '%s' "$1" | grep -Eq "${2#regex:}" ;;
    glob:*)  [[ "$1" == ${2#glob:} ]] ;;
    path:*)  [ "$1" = "${2#path:}" ] ;;
    *)       [ "$1" = "$2" ] ;;
  esac
}

correspond_actifs() { # $1 = chemin
  [ "${#MOTIFS[@]}" -gt 0 ] || return 1
  local m
  for m in "${MOTIFS[@]}"; do correspond_motif "$1" "$m" && return 0; done
  return 1
}

# traduit un motif en arguments git-filter-repo
arg_motif() {
  case "$1" in
    glob:*)  printf '%s\n' "--path-glob" "${1#glob:}" ;;
    regex:*) printf '%s\n' "--path-regex" "${1#regex:}" ;;
    path:*)  printf '%s\n' "--path" "${1#path:}" ;;
    *)       printf '%s\n' "--path" "$1" ;;
  esac
}

chemins_historique() { # tous les chemins distincts de tout l'historique
  git -C "$RACINE" log --all --pretty=format: --name-only --diff-filter=ACMR 2>/dev/null | sed '/^$/d' | sort -u
}

# --- inventaire (lecture seule) ----------------------------------------------
if [ "$MODE" = "--inventaire" ]; then
  RACINE="$(git -C "$DEPOT" rev-parse --show-toplevel 2>/dev/null)" || { echo "pas un dépôt git : $DEPOT" >&2; exit 1; }
  echo
  echo "[reconnaissance] tous les fichiers binaires/documentaires suivis (HEAD), par dossier :"
  git -C "$RACINE" ls-files -z | tr '\0' '\n' | while IFS= read -r f; do
    motif_ext "$f" && dirname "$f"
  done | sort | uniq -c | sort -rn | head -25
  total="$(git -C "$RACINE" ls-files -z | tr '\0' '\n' | while IFS= read -r f; do motif_ext "$f" && echo "$f"; done | wc -l)"
  echo
  echo "TOTAL binaires suivis dans HEAD : $total"
  vise="$(git -C "$RACINE" ls-files -z | tr '\0' '\n' | while IFS= read -r f; do correspond_actifs "$f" && echo "$f"; done | wc -l)"
  echo "dont visés par les motifs ACTIFS  : $vise"
  echo
  echo "Chemins distincts visés présents dans TOUT l'historique (renommages et suppressions inclus) :"
  chemins_historique | while IFS= read -r f; do correspond_actifs "$f" && echo "$f"; done | wc -l
  exit 0
fi

# --- plan (lecture seule) ----------------------------------------------------
if [ "$MODE" = "--plan" ]; then
  RACINE="$(git -C "$DEPOT" rev-parse --show-toplevel 2>/dev/null)" || { echo "pas un dépôt git : $DEPOT" >&2; exit 1; }
  echo
  echo "Chemins visés par les motifs ACTIFS, présents quelque part dans l'historique :"
  chemins_historique | while IFS= read -r f; do correspond_actifs "$f" && echo "  $f"; done | head -40
  n="$(chemins_historique | while IFS= read -r f; do correspond_actifs "$f" && echo "$f"; done | wc -l)"
  echo
  echo "Total : $n chemin(s) à retirer de l'historique."
  echo "Dépôt : $(git -C "$RACINE" count-objects -vH | grep -E '^(size-pack|size):' | tr '\n' ' ')"
  echo
  echo "Commande qui serait lancée sur un clone miroir (sans --push, rien n'est publié) :"
  printf '  git filter-repo --invert-paths'
  for m in "${MOTIFS[@]}"; do
    while IFS= read -r a; do printf ' %q' "$a"; done < <(arg_motif "$m")
  done
  printf ' --force\n'
  echo
  echo "AVANT de lancer : copie les documents à garder depuis ton clone de travail vers priv\\,"
  echo "                  sinon ils ne seront plus dans le dépôt après le prochain clone."
  exit 0
fi

# --- exécution ---------------------------------------------------------------
if [ "$MODE" = "--executer" ]; then
  command -v git-filter-repo >/dev/null 2>&1 || {
    echo "git-filter-repo introuvable : pip install git-filter-repo" >&2; exit 1; }
  [ -n "$SORTIE" ] || { echo "--executer exige --sortie <dossier>" >&2; exit 2; }

  if [ -d "$DEPOT/.git" ]; then
    ORIGINE="$(git -C "$DEPOT" remote get-url origin 2>/dev/null || echo "$DEPOT")"
  else
    ORIGINE="$DEPOT"
  fi
  echo "origine : $ORIGINE"
  echo "sortie  : $SORTIE"

  mkdir -p "$SORTIE" || { echo "impossible de créer $SORTIE" >&2; exit 1; }
  MIROIR="$SORTIE/depot-mirror.git"
  [ -e "$MIROIR" ] && { echo "refus : $MIROIR existe déjà (garde la copie, choisis un autre --sortie)" >&2; exit 1; }

  echo
  echo "1/4  clone miroir (ton clone de travail n'est pas touché)…"
  git clone --mirror "$ORIGINE" "$MIROIR" || { echo "clone impossible" >&2; exit 1; }

  echo "2/4  taille avant : $(git -C "$MIROIR" count-objects -vH | grep '^size-pack' || true)"

  echo "3/4  réécriture de l'historique…"
  args=()
  for m in "${MOTIFS[@]}"; do
    while IFS= read -r a; do args+=("$a"); done < <(arg_motif "$m")
  done
  ( cd "$MIROIR" && git filter-repo --invert-paths "${args[@]}" --force ) || {
    echo "git filter-repo a échoué" >&2; exit 1; }

  ( cd "$MIROIR" && git reflog expire --expire=now --all && git gc --prune=now --aggressive ) >/dev/null 2>&1
  echo "     taille après : $(git -C "$MIROIR" count-objects -vH | grep '^size-pack' || true)"

  RACINE="$MIROIR"
  reste="$(chemins_historique | while IFS= read -r f; do correspond_actifs "$f" && echo "$f"; done | wc -l)"
  echo "     chemins visés encore présents dans l'historique : $reste"

  echo "4/4  publication"
  PUSH_CMD="git -C \"$MIROIR\" remote add origin \"$ORIGINE\" && git -C \"$MIROIR\" push --mirror origin"
  if [ "$PUSH" = 1 ] && [ "$OUI" = 1 ]; then
    echo "     envoi (--push --oui)…"
    ( cd "$MIROIR" && git remote remove origin 2>/dev/null; git remote add origin "$ORIGINE" && git push --mirror origin ) || {
      echo "push refusé — vérifie tes droits, puis relance à la main :" >&2; echo "  $PUSH_CMD" >&2; exit 1; }
    echo "     poussé. Sur CHAQUE machine : supprime l'ancien clone puis re-clone."
  else
    cat <<EOF
     Rien n'a été publié. Quand tu es prêt (seul à pousser, documents copiés dans priv\\) :

       $PUSH_CMD

     Puis, sur chaque machine : supprimer l'ancien clone et re-cloner.
     Enfin : GitHub Support → « removal of cached views » (dépôt + SHA concernés).
EOF
  fi
  exit 0
fi
