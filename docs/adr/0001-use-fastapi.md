# ADR 0001 — Use FastAPI for backend

**Status:** Accepted
**Date:** 2026-05-27
**Deciders:** Initial maintainers

## Context

Precisamos escolher framework Python para backend que ofereça:

- API HTTP idiomática
- Validação automática de input/output
- Documentação OpenAPI nativa (sem manutenção manual)
- Suporte async (crawlers fazem muito I/O)
- Boa ergonomia para contribuidores

## Options Considered

| Option | Pros | Cons |
|---|---|---|
| **FastAPI** | OpenAPI nativo, Pydantic v2, async-first, ecosystem grande, docs excelentes | Relativamente novo (~6 anos) |
| Django + DRF | Ecossistema enorme, admin pronto, ORM maduro | Async ainda em transição, OpenAPI requer libs externas, mais boilerplate |
| Flask + extensões | Flexível, conhecido | OpenAPI/validação requerem libs separadas, sync por padrão |
| Starlette puro | Mínimo, async-native | Tudo manual, sem validação/docs automáticos |
| Litestar | Moderno, performance | Comunidade menor |

## Decision

**Usar FastAPI** como framework backend.

## Consequences

### Positivas

- OpenAPI 3.1 gerada automaticamente do código (zero drift)
- Pydantic v2 forçando type safety em runtime
- `async def` natural para crawlers + DB calls
- Scalar UI / ReDoc / Swagger UI plug-and-play
- Contributors familiares com FastAPI são abundantes

### Negativas / Trade-offs

- Sem admin nativo (decidiremos depois se vale construir)
- Acoplamento com Starlette (não é problema na prática)
- Performance pura levemente abaixo de frameworks puramente async pequenos — irrelevante para nossa escala

### Action Items

- Estrutura modular por router (`/v1/opportunities.py`, etc)
- Pydantic schemas separados de models SQLAlchemy
- Scalar UI em `/docs` (em vez do Swagger UI padrão)
- Todos endpoints com `summary`, `description`, `responses` ricos
