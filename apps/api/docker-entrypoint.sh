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

echo "→ Starting Uvicorn on 0.0.0.0:8000"
exec uv run --no-dev uvicorn civic_radar.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --no-access-log
