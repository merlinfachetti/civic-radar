# ADR 0006 — Plugin architecture for crawlers

**Status:** Accepted
**Date:** 2026-05-27
**Deciders:** Initial maintainers

## Context

CivicRadar precisa lidar com **muitas fontes heterogêneas** — bancas, prefeituras, portais, agregadores — cada uma com estrutura HTML/PDF própria. Princípio open source 6.5: "Contribution-friendly" — adicionar nova fonte deve ser PR auto-contido.

## Options Considered

| Option | Pros | Cons |
|---|---|---|
| **Plugin architecture (Protocol-based)** | Cada fonte é isolada, fácil contribuir, testável | Boilerplate mínimo por fonte |
| Single monolithic crawler | Menos código | Acoplamento absurdo, intestável, PRs gigantes |
| Config-driven (YAML rules) | Sem código por fonte | Rapidamente vira DSL ad-hoc, inflexível |
| External plugin loader (entry_points) | Plugin em pacote separado | Overkill para MVP, complica setup |

## Decision

**Plugin architecture in-repo, baseada em `Protocol`s do Python**, com cada fonte em `crawlers/sources/<source_id>/`.

### Estrutura

```
crawlers/
├── core/
│   ├── base.py           # BaseCrawler, BaseParser, Normalizer
│   ├── protocols.py      # Protocols (interface contracts)
│   ├── models.py         # RawSnapshot, ParsedOpportunity
│   ├── registry.py       # Auto-discovery por convenção
│   └── http_client.py    # httpx + rate limit + robots.txt
└── sources/
    └── <source_id>/
        ├── __init__.py
        ├── config.yaml   # metadados da fonte
        ├── crawler.py    # SourceCrawler implementation
        ├── parser.py     # SourceParser implementation
        ├── fixtures/     # HTML/PDF reais
        └── tests/        # tests determinísticos
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

`crawlers/core/registry.py` faz introspecção de `crawlers/sources/*/` e registra automaticamente cada fonte que tem `config.yaml` válido + `crawler.py` + `parser.py`.

CLI usa o registry: `civic_radar crawl --source cebraspe` resolve via registry.

## Consequences

### Positivas

- **PR para nova fonte é auto-contido** — toca apenas `crawlers/sources/<id>/` + atualiza `docs/DATA_SOURCES.md`
- **Tests isolados** — cada fonte testa seu parser sem afetar outras
- **Versionamento por parser** — `parser_version` em SemVer permite migrations futuras
- **Sem framework custom** — usa Protocol nativo do Python, zero magia

### Negativas / Trade-offs

- **Some duplication** — cada fonte tem boilerplate similar
  - **Mitigação:** `BaseCrawler` abstrai rate-limit, robots.txt, snapshot store
- **Sem isolation forte** — bug numa source pode crashar processo
  - **Mitigação:** Crawler orchestrator captura exceptions per-source; falha em uma fonte não afeta outras
- **Plugin discovery em runtime** — não compile-time
  - **Mitigação:** OK; CLI valida via registry no startup

### Action Items

- Criar `BaseCrawler` que cuida de:
  - HTTP client httpx pré-configurado
  - Rate limiting per-source
  - robots.txt check obrigatório
  - Logging structlog com contexto
  - Snapshot store
- Criar `BaseParser` abstract com helpers para HTML (selectolax) e PDF (pdfplumber)
- Registry com validation: source ID único, parser_version válido SemVer
- `docs/DATA_SOURCES.md` documenta workflow

## Re-evaluation

Quando tivermos >20 fontes ou plugin externos forem desejados, considerar evoluir para `entry_points` do setuptools. Mas isso é problema para o futuro.
