# syntax=docker/dockerfile:1.7
# CivicRadar — API container.

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_LINK_MODE=copy

# Install uv (the Astral installer drops static binaries in /root/.local/bin).
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Copy lockfile + manifest first for layer caching.
COPY apps/api/pyproject.toml apps/api/README.md ./apps/api/
COPY pyproject.toml ./
COPY crawlers/pyproject.toml ./crawlers/
COPY crawlers/core/__init__.py ./crawlers/core/

WORKDIR /app/apps/api

RUN uv sync --no-dev --frozen 2>/dev/null || uv sync --no-dev

# Copy source last.
COPY apps/api/src ./src
COPY apps/api/alembic.ini ./
COPY data/seeds /seeds

# Create data dir for SQLite (mounted as volume in docker-compose).
RUN mkdir -p /data

EXPOSE 8000

# Entrypoint: apply migrations + (optional) seed + serve.
COPY apps/api/docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh

CMD ["./docker-entrypoint.sh"]
