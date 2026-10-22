#!/bin/sh
# Creates .env from .env.example with random secrets and a random admin password.
# Usage: ./scripts/setup-env.sh   (refuses to overwrite an existing .env)
set -e
cd "$(dirname "$0")/.."

if [ -f .env ]; then
  echo ".env already exists — nothing changed. Delete it first if you want a fresh one."
  exit 0
fi

rand() { LC_ALL=C tr -dc 'A-Za-z0-9' </dev/urandom | head -c "$1"; }
DB_PASSWORD=$(rand 24)
SECRET_KEY=$(rand 64)
ADMIN_PASSWORD="Adm-$(rand 16)"

sed \
  -e "s|^POSTGRES_PASSWORD=.*|POSTGRES_PASSWORD=$DB_PASSWORD|" \
  -e "s|esw:change-me@|esw:$DB_PASSWORD@|g" \
  -e "s|^SECRET_KEY=.*|SECRET_KEY=$SECRET_KEY|" \
  -e "s|^ADMIN_USERNAME=.*|ADMIN_USERNAME=admin|" \
  -e "s|^ADMIN_PASSWORD=.*|ADMIN_PASSWORD=$ADMIN_PASSWORD|" \
  .env.example > .env

echo "Created .env"
echo "  Admin login:    admin"
echo "  Admin password: $ADMIN_PASSWORD   (also stored in .env)"
