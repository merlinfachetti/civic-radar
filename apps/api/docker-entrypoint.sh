#!/usr/bin/env bash
# CivicRadar API container entrypoint
set -euo pipefail

cd /app/apps/api

echo "→ Running database migrations..."
uv run --no-dev alembic upgrade head

if [[ "${CIVIC_RADAR_SEED_ON_STARTUP:-false}" == "true" ]] && [[ -f /seeds/opportunities_seed.json ]]; then
    echo "→ Seeding database..."
    uv run --no-dev civic_radar seed --file /seeds/opportunities_seed.json || true
fi

# Respect $PORT when the host (Railway, Heroku, Cloud Run, etc.) injects one;
# fall back to 8000 for local docker-compose / dev.
PORT="${PORT:-8000}"
echo "→ Starting Uvicorn on 0.0.0.0:${PORT}"
exec uv run --no-dev uvicorn civic_radar.main:app \
    --host 0.0.0.0 \
    --port "${PORT}" \
    --no-access-log
