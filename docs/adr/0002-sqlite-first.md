# ADR 0002 — SQLite-first, Postgres in production

**Status:** Accepted
**Date:** 2026-05-27
**Deciders:** Initial maintainers

## Context

Projeto é open source e precisa ser **trivial de rodar localmente** (princípio 6.4 do PRODUCT_FOUNDATION). Contribuidores não devem precisar configurar Postgres, criar DBs, gerenciar credenciais só para rodar testes.

Por outro lado, em produção precisamos de um DB robusto que suporte concorrência, full-text search avançado, e backups.

## Options Considered

| Option | Pros | Cons |
|---|---|---|
| **SQLite local + Postgres prod** | Setup trivial local, Postgres robusto em prod | Pequenas divergências de SQL entre engines |
| Postgres em tudo (com Docker) | Consistência total | Docker obrigatório, lentidão em testes |
| SQLite em tudo | Máxima simplicidade | Concorrência ruim em prod, FTS limitado |
| MySQL/MariaDB | Familiar | Não traz vantagem clara sobre Postgres |

## Decision

- **Dev local:** SQLite (`data/civic_radar.db`)
- **Tests:** SQLite in-memory (`:memory:`)
- **Production:** PostgreSQL 16

Conexão configurada via `DATABASE_URL` em env. Alembic migrations escritas em SQLAlchemy 2.0 syntax para serem dialect-agnostic onde possível.

## Consequences

### Positivas

- `git clone && docker compose up` funciona em 30 segundos
- Contribuidores não precisam configurar nada além de Docker (ou uv)
- Tests rápidos com `:memory:`
- Postgres apenas em produção, onde concorrência importa

### Negativas / Trade-offs

- **Risco de drift:** SQL específico de um engine pode quebrar no outro
  - **Mitigação:** Usar SQLAlchemy Core/ORM apenas. CI roda testes em ambos os engines (job opcional).
- **FTS5 (SQLite) vs tsvector (Postgres):** Comportamentos diferentes
  - **Mitigação:** Abstrair search via service layer. Em SQLite usa FTS5, em Postgres usa GIN+tsvector.
- **Migrations testadas em ambos:** Adicionar job CI que aplica migrations em Postgres também

### Action Items

- `apps/api/src/civic_radar/db/__init__.py` detecta dialect e configura adequadamente
- CI roda backend tests em SQLite (default) e em Postgres (matrix job opcional)
- Documentar em README: "default = SQLite; export DATABASE_URL=postgresql://... para Postgres"
