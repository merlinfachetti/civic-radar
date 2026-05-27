# ADR 0001 — Use FastAPI for the backend

**Status:** Accepted
**Date:** 2026-05-27
**Deciders:** Initial maintainers

## Context

We need a Python web framework that delivers:

- An idiomatic HTTP API
- Automatic input/output validation
- Native OpenAPI documentation (no manual upkeep)
- Async support (crawlers do a lot of I/O)
- A good developer experience for contributors

## Options considered

| Option | Pros | Cons |
|---|---|---|
| **FastAPI** | Native OpenAPI, Pydantic v2, async-first, large ecosystem, excellent docs | Relatively young (~6 years) |
| Django + DRF | Huge ecosystem, ready-made admin, mature ORM | Async still transitional, OpenAPI needs external libs, more boilerplate |
| Flask + extensions | Flexible, well-known | OpenAPI/validation require extra libs, sync by default |
| Pure Starlette | Minimal, async-native | Everything manual, no validation/docs out of the box |
| Litestar | Modern, good performance | Smaller community than FastAPI |

## Decision

**Use FastAPI** as the backend framework.

## Consequences

### Positive

- OpenAPI 3.1 generated automatically from the code (zero drift)
- Pydantic v2 enforces type safety at runtime
- `async def` feels natural for crawlers + DB calls
- Scalar UI / ReDoc / Swagger UI plug-and-play
- Plenty of contributors are already familiar with FastAPI

### Negative / trade-offs

- No native admin (we will decide later whether to build one)
- Coupling to Starlette (not an issue in practice)
- Slightly lower pure performance than tiny async-only frameworks — irrelevant at our scale

### Action items

- Modular structure per router (`/v1/opportunities.py`, etc.)
- Pydantic schemas kept separate from SQLAlchemy models
- Scalar UI at `/docs` (instead of the default Swagger UI)
- Every endpoint has rich `summary`, `description`, `responses`
