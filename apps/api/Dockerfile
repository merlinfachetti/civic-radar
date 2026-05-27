# syntax=docker/dockerfile:1.7
# CivicRadar — API container.
#
# Build from the repo root so this Dockerfile can reach workspace siblings
# (apps/api, crawlers, the root pyproject.toml and README).

FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    UV_LINK_MODE=copy \
    UV_NO_PROGRESS=1

# Install uv (Astral static binary).
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

WORKDIR /app

# Workspace manifests first — these define the dependency graph.
COPY pyproject.toml uv.lock README.md ./
COPY apps/api/pyproject.toml ./apps/api/
COPY crawlers/pyproject.toml ./crawlers/

# uv resolves the workspace by reading every member's pyproject; the editable
# install also needs the actual package directories to exist on disk, so we
# copy the source trees up-front. This trades a bit of layer caching for build
# correctness — code-only changes still benefit from the apt/uv binary cache.
COPY apps/api/src ./apps/api/src
COPY crawlers/crawlers ./crawlers/crawlers

WORKDIR /app/apps/api

RUN uv sync --no-dev --frozen 2>/dev/null || uv sync --no-dev

# Remaining runtime assets.
COPY apps/api/alembic.ini ./
COPY data/seeds /seeds

# SQLite volume mount point (docker-compose attaches a named volume here).
RUN mkdir -p /data

EXPOSE 8000

COPY apps/api/docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh

CMD ["./docker-entrypoint.sh"]
