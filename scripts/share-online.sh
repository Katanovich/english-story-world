#!/bin/sh
# Shares the app running on this computer via a free Cloudflare quick tunnel.
# Usage: ./scripts/share-online.sh      (stop with Ctrl+C)
#
# - Starts the Docker containers if they are not running.
# - Keeps the Mac awake (caffeinate) while the tunnel is open.
# - Prints a public https://….trycloudflare.com link. The link CHANGES every time.
set -e
cd "$(dirname "$0")/.."

command -v cloudflared >/dev/null || { echo "Install cloudflared first: brew install cloudflared"; exit 1; }
docker info >/dev/null 2>&1 || { echo "Start Docker Desktop first."; exit 1; }

docker compose up -d
echo "Waiting for the app…"
i=0
until curl -sf http://localhost:3000/api/v1/health >/dev/null; do
  i=$((i + 1)); [ $i -gt 60 ] && { echo "App did not start. See: docker compose logs"; exit 1; }
  sleep 2
done

LOG=$(mktemp)
echo "Opening the tunnel… (Ctrl+C to stop sharing)"
caffeinate -dims cloudflared tunnel --no-autoupdate --url http://localhost:3000 >"$LOG" 2>&1 &
PID=$!
trap 'kill $PID 2>/dev/null; rm -f "$LOG"; echo; echo "Sharing stopped."' INT TERM EXIT

URL=""
i=0
while [ -z "$URL" ] && [ $i -lt 60 ]; do
  URL=$(grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' "$LOG" | head -1 || true)
  i=$((i + 1)); sleep 1
done
[ -z "$URL" ] && { echo "Could not open the tunnel:"; cat "$LOG"; exit 1; }

echo
echo "========================================================"
echo "  Your app is online at:  $URL"
echo "  Send this link to students. Keep this window open."
echo "========================================================"
wait $PID
