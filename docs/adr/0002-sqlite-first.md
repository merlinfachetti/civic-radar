# ADR 0002 — SQLite-first, Postgres in production

**Status:** Accepted
**Date:** 2026-05-27
**Deciders:** Initial maintainers

## Context

CivicRadar is open source and needs to be **trivial to run locally** (principle 6.4 in PRODUCT_FOUNDATION). Contributors should not have to set up Postgres, create databases or manage credentials just to run the tests.

In production we still want a robust DB that handles concurrency, advanced full-text search and backups.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| **SQLite locally + Postgres in prod** | Trivial local setup, robust Postgres in prod | Small SQL divergences between engines |
| Postgres everywhere (Docker) | Total consistency | Docker required, slower tests |
| SQLite everywhere | Maximum simplicity | Poor concurrency in prod, limited FTS |
| MySQL/MariaDB | Familiar | No clear advantage over Postgres |

## Decision

- **Local dev:** SQLite (`data/civic_radar.db`)
- **Tests:** SQLite in-memory (`:memory:`)
- **Production:** PostgreSQL 16

The connection is configured via `DATABASE_URL` in env. Alembic migrations are written using SQLAlchemy 2.0 syntax to stay dialect-agnostic where possible.

## Consequences

### Positive

- `git clone && docker compose up` boots in ~30 seconds
- Contributors only need Docker (or uv) — nothing else
- Fast tests with `:memory:`
- Postgres only in production, where concurrency matters

### Negative / trade-offs

- **Drift risk:** engine-specific SQL can break on the other side
  - **Mitigation:** Use SQLAlchemy Core/ORM only. CI runs tests on both engines (optional job).
- **FTS5 (SQLite) vs tsvector (Postgres):** different behavior
  - **Mitigation:** Abstract search through a service layer. SQLite uses FTS5, Postgres uses GIN+tsvector.
- **Migrations tested on both:** add a CI job that applies migrations to Postgres too

### Action items

- `apps/api/src/civic_radar/db/__init__.py` detects the dialect and configures accordingly
- CI runs backend tests on SQLite (default) and Postgres (optional matrix job)
- Document in the README: "default = SQLite; export DATABASE_URL=postgresql://... for Postgres"
