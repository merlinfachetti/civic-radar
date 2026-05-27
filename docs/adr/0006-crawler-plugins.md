# ADR 0006 — Plugin architecture for crawlers

**Status:** Accepted
**Date:** 2026-05-27
**Deciders:** Initial maintainers

## Context

CivicRadar needs to deal with **many heterogeneous sources** — boards, city halls, portals, aggregators — each with its own HTML/PDF structure. Open source principle 6.5 says: "Contribution-friendly" — adding a new source must be a self-contained PR.

## Options considered

| Option | Pros | Cons |
|---|---|---|
| **In-repo plugin architecture (Protocol-based)** | Each source is isolated, easy to contribute, testable | Minimal boilerplate per source |
| Single monolithic crawler | Less code | Wild coupling, untestable, gigantic PRs |
| Config-driven (YAML rules) | No code per source | Quickly turns into an ad-hoc DSL, inflexible |
| External plugin loader (entry_points) | Plugin in a separate package | Overkill for the MVP, complicates setup |

## Decision

**In-repo plugin architecture, built on Python `Protocol`s**, with each source living in `crawlers/crawlers/sources/<id>/`.

### Structure

```
crawlers/
├── pyproject.toml
└── crawlers/                          # the actual package
    ├── core/
    │   ├── base.py           # BaseCrawler, BaseParser, Normalizer
    │   ├── protocols.py      # Protocols (interface contracts)
    │   ├── models.py         # RawSnapshot, ParsedOpportunity
    │   ├── registry.py       # auto-discovery by convention
    │   └── http_client.py    # httpx + rate limit + robots.txt
    └── sources/
        └── <source_id>/
            ├── __init__.py
            ├── config.yaml   # source metadata
            ├── crawler.py    # SourceCrawler implementation
            ├── parser.py     # SourceParser implementation
            ├── fixtures/     # real HTML/PDF
            └── tests/        # deterministic tests
```

### Contracts

```python
class SourceCrawler(Protocol):
    source_id: str
    rate_limit_seconds: int

    async def fetch_list(self) -> list[RawSnapshot]: ...
    async def fetch_detail(self, snapshot: RawSnapshot) -> RawSnapshot: ...


class SourceParser(Protocol):
    source_id: str
    parser_version: str  # SemVer

    def parse(self, snapshot: RawSnapshot) -> list[ParsedOpportunity]: ...
```

### Auto-discovery

`crawlers/crawlers/core/registry.py` walks `crawlers/sources/*/` and automatically registers every source that has a valid `config.yaml` + `crawler.py` + `parser.py`.

The CLI uses the registry: `civic_radar crawl --source cebraspe` resolves through it.

## Consequences

### Positive

- **A PR for a new source is self-contained** — touches only `crawlers/sources/<id>/` plus `docs/DATA_SOURCES.md`
- **Isolated tests** — each source tests its parser without affecting the others
- **Per-parser versioning** — SemVer `parser_version` enables future migrations
- **No custom framework** — uses native Python Protocols, zero magic

### Negative / trade-offs

- **Some duplication** — each source carries similar boilerplate
  - **Mitigation:** `BaseCrawler` abstracts rate-limiting, robots.txt and the snapshot store
- **No hard isolation** — a bug in one source can crash the process
  - **Mitigation:** The crawler orchestrator catches exceptions per source; one failure does not affect the others
- **Discovery at runtime** — not at compile-time
  - **Mitigation:** OK; the CLI validates via the registry at startup

### Action items

- Build a `BaseCrawler` that handles:
  - A pre-configured httpx client
  - Per-source rate limiting
  - Mandatory robots.txt check
  - structlog logging with context
  - The snapshot store
- Build an abstract `BaseParser` with helpers for HTML (selectolax) and PDF (pdfplumber)
- Registry with validation: unique source ID, valid SemVer `parser_version`
- `docs/DATA_SOURCES.md` documents the workflow

## Re-evaluation

Once we have >20 sources, or external plugins are desired, consider moving to setuptools `entry_points`. That is a problem for future-us.
