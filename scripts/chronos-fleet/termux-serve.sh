#!/data/data/com.termux/files/usr/bin/bash
# Usage: bash termux-serve.sh /chemin/model.gguf 8084 192.168.x.y
# Security: bind the Wi-Fi/private VPN address only, NEVER public Internet.
set -euo pipefail
MODEL="${1:?Usage: $0 MODEL.GGUF PORT LOCAL_PRIVATE_IP}"
PORT="${2:?Specify port}"
IP="${3:?Specify private Wi-Fi/VPN IP}"
case "$IP" in 10.*|192.168.*|172.16.*|172.17.*|172.18.*|172.19.*|172.2[0-9].*|172.3[01].*) ;; *) echo 'Adresse privee requise (pas de 0.0.0.0 ni IP publique)' >&2; exit 2;; esac
command -v llama-server >/dev/null || { echo 'llama-server absent: verifier paquet Termux llama.cpp' >&2; exit 2; }
[ -f "$MODEL" ] || { echo "Modele absent: $MODEL" >&2; exit 2; }
KEY_FILE="$HOME/.config/cronos-fleet/llama-key"
mkdir -p "$(dirname "$KEY_FILE")"
chmod 700 "$(dirname "$KEY_FILE")"
if [ ! -s "$KEY_FILE" ]; then
  umask 077
  head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n' > "$KEY_FILE"
  chmod 600 "$KEY_FILE"
fi
printf 'Cle locale enregistree dans %s (a copier dans CRONOS_*_KEY sur la tour)\n' "$KEY_FILE"
exec llama-server --model "$MODEL" --host "$IP" --port "$PORT" --ctx-size 2048 --threads 4 --api-key "$(cat "$KEY_FILE")"