# Data Sources

> Guide for understanding, adding and maintaining data sources in CivicRadar.

---

## 📡 Currently supported sources

| Source ID | Name | Type | Quality | Status |
|---|---|---|---|---|
| `cebraspe` | Cebraspe | Organizing Board | High | ✅ Active |
| `fgv` | FGV CONHECIMENTO | Organizing Board | High | ✅ Active |
| `pci-concursos` | PCI Concursos | Aggregator | Medium | ✅ Active |

---

## 🎯 Source principles

1. **Official first** — Organizing boards and agency sites take priority. Aggregators are complementary.
2. **Respect robots.txt** — Always. If the source forbids us, we do not crawl.
3. **Rate limiting** — Minimum 5–10 seconds between requests per source.
4. **Metadata, not copies** — We store title, dates and links. We do not republish full content.
5. **Link to the original** — Every opportunity surfaces its official source URL.
6. **Traceability** — `parser_version`, `last_checked_at`, `confidence_level` are always present.

---

## ➕ How to add a new source

### 1. Create the structure

```bash
SOURCE_ID="vunesp"
mkdir -p crawlers/crawlers/sources/$SOURCE_ID/{fixtures,tests}
cd crawlers/crawlers/sources/$SOURCE_ID
touch __init__.py crawler.py parser.py config.yaml
touch tests/__init__.py tests/test_parser.py
touch fixtures/README.md
```

### 2. Define `config.yaml`

```yaml
id: vunesp
name: Vunesp
type: organizing_board       # agency | board | portal | aggregator
base_url: https://www.vunesp.com.br/
enabled: true
robots_policy_required: true
rate_limit_seconds: 10
parser: vunesp_v1
parser_version: "1.0.0"
quality_level: high          # high | medium | low
maintainer: "@username"
```

### 3. Implement the crawler

```python
# crawlers/crawlers/sources/vunesp/crawler.py
from crawlers.core.base import BaseCrawler
from crawlers.core.models import RawSnapshot


class VunespCrawler(BaseCrawler):
    source_id = "vunesp"

    async def fetch_list(self) -> list[RawSnapshot]:
        # Logic to fetch the index page
        ...

    async def fetch_detail(self, snapshot: RawSnapshot) -> RawSnapshot:
        # Fetch the detail page
        ...
```

### 4. Implement the parser

```python
# crawlers/crawlers/sources/vunesp/parser.py
from crawlers.core.base import BaseParser
from crawlers.core.models import ParsedOpportunity, RawSnapshot


class VunespParser(BaseParser):
    source_id = "vunesp"
    parser_version = "1.0.0"

    def parse(self, snapshot: RawSnapshot) -> list[ParsedOpportunity]:
        # Use selectolax for HTML, pdfplumber for PDF.
        # Must be deterministic.
        ...
```

### 5. Capture fixtures

```bash
# Save real HTML/PDF pages that will back the tests
curl -A "CivicRadar/1.0" https://www.vunesp.com.br/concursos/abertos > \
  crawlers/crawlers/sources/vunesp/fixtures/concursos_abertos.html
```

**Important:** fixtures must be **representative and stable**. At minimum:
- 1 list fixture (index with multiple openings)
- 2 detail fixtures (open + closed tender)
- 1 edge case fixture (e.g. salary range, no defined date, etc.)

### 6. Add the golden file

For every fixture, generate the expected JSON output:

```bash
# fixtures/concursos_abertos.expected.json
{
  "opportunities": [
    {
      "title": "Concurso para Analista de Sistemas",
      "organization": "Tribunal X",
      "salary_min": 8500.00,
      ...
    }
  ]
}
```

### 7. Write the tests

```python
# crawlers/crawlers/sources/vunesp/tests/test_parser.py
import json
from pathlib import Path

from crawlers.sources.vunesp.parser import Parser

FIXTURES = Path(__file__).parent.parent / "fixtures"


def test_parser_extracts_concursos_abertos():
    html = (FIXTURES / "concursos_abertos.html").read_text()
    expected = json.loads((FIXTURES / "concursos_abertos.expected.json").read_text())

    parser = Parser()
    result = parser.parse(make_snapshot(html))

    assert len(result) == len(expected["opportunities"])
    # ... per-field asserts
```

### 8. Register the source in the seed

```python
# data/seeds/sources.py
SOURCES = [
    ...,
    {"source_id": "vunesp", "name": "Vunesp", ...},
]
```

### 9. Open a PR

The PR should include:
- Crawler + parser code
- At least 3 HTML fixtures + golden files
- Tests passing
- An update in `docs/DATA_SOURCES.md` (the table above)
- An update in the seed

---

## 🏷️ Source quality levels

| Level | Criteria | Examples |
|---|---|---|
| **High** | Official organizing board or agency site with predictable HTML/PDF structure | Cebraspe, FGV, FCC, court sites |
| **Medium** | Public portal with verifiable information but variable structure | City-hall portals, well-known aggregators |
| **Low** | Aggregator without clear traceability, hard-to-verify data | Sites without visible CNPJ, copied content |

---

## ⏱️ Rate limiting

Every source declares `rate_limit_seconds` in `config.yaml`. The base crawler respects it automatically.

**Sensible defaults:**
- Large boards (Cebraspe, FGV): 10s
- Agency sites: 15s
- Large PDFs: 30s
- Aggregators: 5s (only if robots.txt permits)

---

## 🤖 robots.txt

Before crawling, `BaseCrawler` checks `/robots.txt` for the source. If the `CivicRadar` user-agent (or `*`) is disallowed for the path, the crawler **silently aborts** and logs a warning.

Never try to bypass robots.txt. If an important source is blocked, open an issue so we can discuss alternatives (direct contact, official API, etc.).

---

## 🩺 Parser health

Every parser reports health at `/v1/sources/{id}/health`:

```json
{
  "source_id": "cebraspe",
  "parser_version": "1.2.3",
  "last_successful_run": "2026-05-27T14:00:00Z",
  "last_run_status": "success",
  "items_extracted_last_run": 47,
  "items_extracted_7d_avg": 52,
  "anomaly_detected": false
}
```

When `items_extracted_last_run` falls below 50% of the 7-day average, we flag `anomaly_detected: true` — a signal that the parser may have broken with a layout change.

---

## 🔄 Updating fixtures

When the source changes its layout:

1. Bump `parser_version` (SemVer minor)
2. Capture a new fixture with a date suffix: `concursos_abertos_2026_05.html`
3. Keep the old fixture for regression testing
4. Update the parser to support both layouts (during transition)
5. After stabilization, deprecate the old fixture in a major release

---

## ⚖️ Legal considerations

- **Never** copy full content from private sources (PCI, commercial aggregators) when their Terms of Service forbid it.
- **Always** identify yourself via User-Agent: `CivicRadar/1.0 (+https://github.com/merlinfachetti/civic-radar)`
- **In doubt?** Open an issue with the `legal-review` label before merging.

Maintainers can reject sources that pose elevated legal or ethical risk.

---

## 📝 Issue templates

- **"Add new source: <name>"** — to suggest a new source
- **"Parser broken for <source>"** — when a parser stops extracting correctly

Use `.github/ISSUE_TEMPLATE/` when opening one.
