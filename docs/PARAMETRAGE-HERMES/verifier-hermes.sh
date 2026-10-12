#!/usr/bin/env bash
# verifier-hermes.sh — état des lieux du montage Hermes + OmniRoute + Ollama (Linux / macOS / WSL2)
#
# Usage :
#   bash verifier-hermes.sh            # état des lieux + `hermes doctor`
#   bash verifier-hermes.sh --quota    # + quota payant (openai-codex) si des identifiants existent
#   bash verifier-hermes.sh --log      # + ajoute une ligne à quota-log.csv (calibration)
#
# Codes de sortie : 0 = socle complet, 1 = au moins un élément manquant (règle n°8 de
# projects/watchtower/AGENTS.md : une vérification se termine par un code, jamais par un `| head`
# qui masque l'absence). Aucun secret n'est affiché : uniquement la PRÉSENCE des variables.

set -u

QUOTA=0
LOG=0
for arg in "$@"; do
  case "$arg" in
    --quota) QUOTA=1 ;;
    --log)   LOG=1; QUOTA=1 ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) echo "option inconnue: $arg (voir --help)" >&2; exit 2 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CSV="$SCRIPT_DIR/quota-log.csv"
PROBLEMES=0

ok()   { printf '  \033[32m[OK]\033[0m   %s\n' "$1"; }
ko()   { printf '  \033[31m[KO]\033[0m   %s\n' "$1"; PROBLEMES=$((PROBLEMES + 1)); }
warn() { printf '  \033[33m[?]\033[0m    %s\n' "$1"; }
titre(){ printf '\n== %s ==\n' "$1"; }

have() { command -v "$1" >/dev/null 2>&1; }

http_code() { # $1 = url
  if have curl; then
    curl -s -o /dev/null -m 3 -w '%{http_code}' "$1" 2>/dev/null || echo "000"
  else
    echo "nocurl"
  fi
}

port_open() { # $1 = port, $2 = hôte (défaut 127.0.0.1)
  (exec 3<>"/dev/tcp/${2:-127.0.0.1}/$1") >/dev/null 2>&1 && return 0 || return 1
}

titre "1. Hermes"
if have hermes; then
  ok "hermes présent : $(hermes --version 2>/dev/null | head -1)"
  CFG="$(hermes config path 2>/dev/null)"
  ENV_FILE="$(hermes config env-path 2>/dev/null)"
  [ -n "$CFG" ] && ok "config.yaml : $CFG" || warn "chemin de config non résolu (hermes config path)"
  [ -n "$ENV_FILE" ] && ok ".env : $ENV_FILE" || warn "chemin .env non résolu (hermes config env-path)"

  PROVIDER="$(hermes config get model.provider 2>/dev/null)"
  MODELE="$(hermes config get model.default 2>/dev/null)"
  printf '  route : provider=%s  modèle=%s\n' "${PROVIDER:-<vide>}" "${MODELE:-<vide>}"
  case "${PROVIDER:-}" in
    *omniroute*|custom*) ok "route principale = endpoint personnalisé (OmniRoute / local)" ;;
    ""|auto)             ko "route principale non définie (étape 2 du README)" ;;
    *)                   warn "route principale = $PROVIDER (le payant doit rester manuel)" ;;
  esac

  if hermes doctor >/tmp/hermes-doctor-$$.log 2>&1; then
    ok "hermes doctor : exit 0 (aucun problème non résolu)"
  else
    ko "hermes doctor : exit != 0 — $(tail -3 /tmp/hermes-doctor-$$.log | tr '\n' ' ')"
  fi
  rm -f /tmp/hermes-doctor-$$.log
else
  ko "commande \`hermes\` absente du PATH (relancer le shell après l'installation)"
fi

titre "2. OmniRoute (127.0.0.1:20128)"
if port_open 20128; then
  ok "port 20128 ouvert"
  CODE="$(http_code http://127.0.0.1:20128/v1/models)"
  case "$CODE" in
    200) ok "/v1/models répond 200" ;;
    401) warn "/v1/models répond 401 : la clé OmniRoute est requise (normal sans en-tête)" ;;
    000|nocurl) warn "port ouvert mais /v1/models injoignable (curl absent ?)" ;;
    *)   warn "/v1/models répond $CODE" ;;
  esac
  if have curl; then
    printf '  dashboard : http://127.0.0.1:20128  (Providers → connecter un fournisseur ; Endpoints → clé)\n'
  fi
else
  ko "port 20128 fermé (OmniRoute non démarré — étape 1)"
fi

titre "3. Ollama (127.0.0.1:11434)"
if port_open 11434; then
  ok "port 11434 ouvert"
  if have curl; then
    TAGS="$(curl -s -m 3 http://127.0.0.1:11434/api/tags 2>/dev/null)"
    if [ -n "$TAGS" ]; then
      if have python3; then
        MODELES="$(printf '%s' "$TAGS" | python3 -c 'import json,sys
try:
    d=json.load(sys.stdin)
except Exception:
    print("(illisible)"); raise SystemExit
names=[m.get("name","?") for m in d.get("models",[])]
print(", ".join(names) if names else "(aucun modèle installé)")' 2>/dev/null)"
      else
        MODELES="$(printf '%s' "$TAGS" | grep -o '"name":"[^"]*"' | cut -d'"' -f4 | tr '\n' ' ')"
      fi
      printf '  modèles : %s\n' "${MODELES:-?}"
      case "${MODELES:-}" in
        *none*|"(aucun modèle installé)"|"") ko "aucun modèle Ollama installé (ollama pull …)" ;;
        *) ok "au moins un modèle local disponible" ;;
      esac
    else
      warn "réponse /api/tags vide"
    fi
    have curl && have python3 && :
  fi
else
  ko "port 11434 fermé (Ollama non démarré — étape 3)"
fi

titre "4. Variables sensibles (présence seulement)"
if [ -n "${ENV_FILE:-}" ] && [ -f "${ENV_FILE:-/nonexistent}" ]; then
  PERM="$(stat -c '%a' "$ENV_FILE" 2>/dev/null || stat -f '%Lp' "$ENV_FILE" 2>/dev/null)"
  case "$PERM" in 600) ok ".env en 600" ;; *) warn ".env en $PERM — passer à 600 (chmod 600 \"$ENV_FILE\")" ;; esac
  for VAR in OMNIROUTE_API_KEY OPENAI_API_KEY OPENROUTER_API_KEY GOOGLE_API_KEY GROQ_API_KEY; do
    if grep -q "^${VAR}=" "$ENV_FILE" 2>/dev/null; then printf '  présent : %s\n' "$VAR"; else printf '  absent  : %s\n' "$VAR"; fi
  done
else
  warn "fichier .env non trouvé — les clés n'ont pas encore été posées"
fi

QUOTA_LIGNE=""
if [ "$QUOTA" = 1 ]; then
  titre "5. Quota payant (openai-codex)"
  if have hermes; then
    J="$(hermes usage --provider openai-codex --json 2>/dev/null)"
    if [ -n "$J" ] && have python3; then
      printf '%s' "$J" | python3 -c 'import json,sys
d=json.load(sys.stdin)
print("  plan :", d.get("plan"))
for w in d.get("windows") or []:
    up = w.get("used_percent")
    print("  {:<8} utilisé={}%  reset={}".format(w.get("label","?"), "?" if up is None else up, w.get("resets_at")))
if d.get("unavailable_reason"):
    print("  indisponible :", d["unavailable_reason"])' 2>/dev/null || printf '  %s\n' "$J"
      if have python3; then
        QUOTA_LIGNE="$(printf '%s' "$J" | python3 -c 'import json,sys
try:
    d=json.load(sys.stdin)
except Exception:
    raise SystemExit
ws={ (w.get("label") or "").lower(): w.get("used_percent") for w in (d.get("windows") or []) }
sess=next((v for k,v in ws.items() if "session" in k), "")
week=next((v for k,v in ws.items() if "week" in k), "")
print("{}\t{}".format("" if sess is None else sess, "" if week is None else week))' 2>/dev/null)"
      fi
    else
      warn "pas de réponse JSON (identifiants Codex absents, ou python3 indisponible)"
    fi
  else
    warn "hermes absent : quota non interrogé"
  fi
fi

if [ "$LOG" = 1 ]; then
  if [ ! -f "$CSV" ]; then printf 'date_utc\tsession_pct\tweekly_pct\tnode\n' > "$CSV"; fi
  HOST="$(hostname 2>/dev/null || echo '?')"
  if [ -n "$QUOTA_LIGNE" ]; then
    printf '%s\t%s\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$QUOTA_LIGNE" "$HOST" >> "$CSV"
    ok "ligne ajoutée à $CSV"
  else
    printf '%s\t\t\t%s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$HOST" >> "$CSV"
    warn "ligne sans quota ajoutée (quota indisponible) → $CSV"
  fi
fi

printf '\n===== VERDICT =====\n'
if [ "$PROBLEMES" -eq 0 ]; then
  printf 'socle complet : rien de manquant.\n'
  exit 0
else
  printf '%d élément(s) à corriger — voir les lignes [KO] ci-dessus.\n' "$PROBLEMES"
  exit 1
fi
