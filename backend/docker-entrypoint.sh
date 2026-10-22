#!/bin/sh
# Container start-up: migrate, bootstrap admin (if configured), optionally seed, then serve.
set -e

alembic upgrade head

if [ -n "$ADMIN_USERNAME" ] && [ -n "$ADMIN_PASSWORD" ]; then
  python -m app.cli create-admin || echo "WARNING: admin bootstrap failed (see message above)."
else
  echo "ADMIN_USERNAME / ADMIN_PASSWORD not set: no admin account created."
fi

if [ "$SEED_ON_START" = "true" ]; then
  python -m app.cli seed
fi

exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers
