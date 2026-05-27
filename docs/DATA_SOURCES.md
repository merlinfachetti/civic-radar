# Data Sources

> Guia para entender, adicionar e manter fontes de dados no CivicRadar.

---

## 📡 Fontes Atualmente Suportadas

| Source ID | Nome | Tipo | Qualidade | Status |
|---|---|---|---|---|
| `cebraspe` | Cebraspe | Organizing Board | High | ✅ Active |
| `fgv` | FGV CONHECIMENTO | Organizing Board | High | ✅ Active |
| `pci-concursos` | PCI Concursos | Aggregator | Medium | ✅ Active |

---

## 🎯 Princípios para Fontes

1. **Oficiais primeiro** — Bancas organizadoras e sites de órgãos têm prioridade. Agregadores são complementares.
2. **Respeito a robots.txt** — Sempre. Se a fonte não permite, não crawleamos.
3. **Rate limiting** — Mínimo 5-10 segundos entre requests por fonte.
4. **Metadados, não cópias** — Armazenamos título, datas, link. Não republicamos conteúdo integral.
5. **Link para original** — Toda oportunidade exibe URL para fonte oficial.
6. **Rastreabilidade** — `parser_version`, `last_checked_at`, `confidence_level` sempre presentes.

---

## ➕ Como Adicionar uma Nova Fonte

### 1. Crie a estrutura

```bash
SOURCE_ID="vunesp"
mkdir -p crawlers/crawlers/sources/$SOURCE_ID/{fixtures,tests}
cd crawlers/crawlers/sources/$SOURCE_ID
touch __init__.py crawler.py parser.py config.yaml
touch tests/__init__.py tests/test_parser.py
touch fixtures/README.md
```

### 2. Defina o `config.yaml`

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

### 3. Implemente o Crawler

```python
# crawlers/crawlers/sources/vunesp/crawler.py
from crawlers.core.base import BaseCrawler, RawSnapshot

class VunespCrawler(BaseCrawler):
    source_id = "vunesp"

    async def fetch_list(self) -> list[RawSnapshot]:
        # Lógica para buscar página índice
        ...

    async def fetch_detail(self, snapshot: RawSnapshot) -> RawSnapshot:
        # Buscar página de detalhe
        ...
```

### 4. Implemente o Parser

```python
# crawlers/crawlers/sources/vunesp/parser.py
from crawlers.core.base import BaseParser, ParsedOpportunity

class VunespParser(BaseParser):
    source_id = "vunesp"
    parser_version = "1.0.0"

    def parse(self, snapshot: RawSnapshot) -> list[ParsedOpportunity]:
        # Use selectolax para HTML, pdfplumber para PDF
        # Deve ser determinístico
        ...
```

### 5. Capture fixtures

```bash
# Salve HTML/PDF reais que serão a base dos testes
curl -A "CivicRadar/1.0" https://www.vunesp.com.br/concursos/abertos > \
  crawlers/crawlers/sources/vunesp/fixtures/concursos_abertos.html
```

**Importante:** fixtures devem ser **representativas e estáveis**. Pelo menos:
- 1 fixture de lista (página índice com vários concursos)
- 2 fixtures de detalhe (concurso aberto + concurso encerrado)
- 1 fixture edge case (ex: salário com faixa, sem data definida, etc)

### 6. Adicione golden file

Para cada fixture, gere o output esperado em JSON:

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

### 7. Escreva os testes

```python
# crawlers/crawlers/sources/vunesp/tests/test_parser.py
import json
from pathlib import Path
from crawlers.sources.vunesp.parser import VunespParser

FIXTURES = Path(__file__).parent.parent / "fixtures"

def test_parser_extracts_concursos_abertos():
    html = (FIXTURES / "concursos_abertos.html").read_text()
    expected = json.loads((FIXTURES / "concursos_abertos.expected.json").read_text())

    parser = VunespParser()
    result = parser.parse(make_snapshot(html))

    assert len(result) == len(expected["opportunities"])
    # ... asserts campo a campo
```

### 8. Registre a fonte no DB seed

```python
# data/seeds/sources.py
SOURCES = [
    ...,
    {"source_id": "vunesp", "name": "Vunesp", ...},
]
```

### 9. Abra PR

PR com:
- Código do crawler + parser
- Pelo menos 3 fixtures HTML + golden files
- Tests passing
- Update em `docs/DATA_SOURCES.md` (esta tabela acima)
- Update no seed

---

## 🏷️ Source Quality Levels

| Level | Critério | Exemplos |
|---|---|---|
| **High** | Banca organizadora oficial, site institucional do órgão, com estrutura HTML/PDF previsível | Cebraspe, FGV, FCC, sites de tribunais |
| **Medium** | Portal público com informação verificável mas estrutura variável | Portais de prefeitura, agregadores conhecidos |
| **Low** | Agregador sem rastreabilidade clara, dados não verificáveis facilmente | Sites sem CNPJ visível, conteúdo copiado |

---

## ⏱️ Rate Limiting

Cada source declara `rate_limit_seconds` no `config.yaml`. O crawler base respeita isso automaticamente.

**Defaults sensatos:**
- Bancas grandes (Cebraspe, FGV): 10s
- Sites de órgãos: 15s
- PDFs grandes: 30s
- Agregadores: 5s (apenas se robots.txt permite)

---

## 🤖 robots.txt

Antes de crawlear, o `BaseCrawler` checa `/robots.txt` da source. Se o user-agent `CivicRadar` ou `*` for proibido para o path, o crawler **aborta silenciosamente** e loga warning.

Nunca tente burlar robots.txt. Se uma fonte importante bloqueia, abra issue para discutirmos alternativas (contato direto, API oficial, etc).

---

## 🩺 Parser Health

Cada parser reporta saúde em `/v1/sources/{id}/health`:

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

Se `items_extracted_last_run` é < 50% da média 7d, marcamos `anomaly_detected: true` — sinal de que o parser pode ter quebrado com mudança de layout.

---

## 🔄 Atualizando fixtures

Se a fonte mudou o layout:

1. Bump `parser_version` (SemVer minor)
2. Capture nova fixture com sufixo de data: `concursos_abertos_2026_05.html`
3. Mantenha fixture antiga para regression testing
4. Atualize parser para lidar com ambos os layouts (durante transição)
5. Após estabilizar, deprecate fixture antiga em release major

---

## ⚖️ Considerações Legais

- **Nunca** copie conteúdo integral de fontes privadas (PCI, agregadores comerciais) se houver Terms of Service vedando.
- **Sempre** identifique-se via User-Agent: `CivicRadar/1.0 (+https://github.com/merlinfachetti/civic-radar)`
- **Em dúvida?** Abra issue com label `legal-review` antes de mergear.

Maintainers podem rejeitar fontes que apresentem risco legal/ético elevado.

---

## 📝 Templates de Issue

- **"Add new source: <name>"** — para sugerir nova fonte
- **"Parser broken for <source>"** — quando parser para de extrair corretamente

Use `.github/ISSUE_TEMPLATE/` ao abrir.
