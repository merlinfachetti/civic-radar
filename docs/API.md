# API Reference

> **Live docs:** http://localhost:8000/docs (Scalar UI) · http://localhost:8000/redoc (ReDoc) · http://localhost:8000/openapi.json
> Este documento é um quick reference. A fonte de verdade é o OpenAPI 3.1 gerado pelo FastAPI.

---

## 📡 Base URL

| Ambiente | URL |
|---|---|
| Local dev | `http://localhost:8000` |
| Production | _TBD (futuro)_ |

Toda API é versionada via path: `/v1/...`. Versões major futuras virão em `/v2/...`.

---

## 🔓 Autenticação

**Não há autenticação obrigatória.** Todos endpoints são públicos.

Rate limits anônimos:
- `60 req/min` por IP

Cabeçalhos opcionais:
- `X-Request-Id` — Para correlation; servidor ecoa de volta

---

## 🩺 Meta Endpoints

### `GET /health`

Status do serviço.

**Response 200:**

```json
{
  "status": "ok",
  "version": "0.1.0",
  "database": {
    "status": "connected",
    "migrations": "current"
  },
  "last_crawl": {
    "source": "cebraspe",
    "completed_at": "2026-05-27T14:23:00Z",
    "items_extracted": 47
  },
  "uptime_seconds": 12345
}
```

### `GET /v1/stats`

Estatísticas públicas agregadas.

**Response 200:**

```json
{
  "total_opportunities": 287,
  "open_opportunities": 124,
  "closed_opportunities": 163,
  "by_state": { "SP": 78, "RJ": 45, "DF": 32, "...": 0 },
  "by_area": { "tecnologia": 56, "administrativo": 89, "...": 0 },
  "by_education_level": { "superior": 198, "medio": 89 },
  "last_7_days": {
    "new_opportunities": 23,
    "closed_opportunities": 12
  },
  "sources": {
    "total": 3,
    "healthy": 3
  }
}
```

---

## 💼 Opportunities

### `GET /v1/opportunities`

Lista paginada de oportunidades.

**Query params:**

| Param | Type | Description |
|---|---|---|
| `q` | string | Full-text search (título + descrição + cargo) |
| `state` | string | Filtro por UF (`SP`, `RJ`, etc) — múltiplos: `?state=SP&state=RJ` |
| `city` | string | Cidade exata |
| `area` | string | Área de interesse (`tecnologia`, `administrativo`, ...) |
| `education_level` | string | `fundamental`, `medio`, `superior`, `pos_graduacao` |
| `salary_min` | number | Salário mínimo desejado (filtra `salary_max >= X` OR `salary_min >= X`) |
| `status` | string | `open`, `closed`, `draft`, `cancelled` — default: `open` |
| `board` | string | Banca organizadora (`cebraspe`, `fgv`, etc) |
| `organization` | string | Órgão (busca parcial) |
| `cursor` | string | Cursor de paginação (opaco) |
| `limit` | int | 1-100, default 20 |
| `sort` | string | `-registration_end_date` (default), `salary_max`, `-created_at`, etc |

**Response 200:**

```json
{
  "items": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Concurso Tribunal X — Analista de Sistemas",
      "organization": "Tribunal Regional X",
      "board": "cebraspe",
      "area": "tecnologia",
      "position_name": "Analista de Sistemas",
      "education_level": "superior",
      "salary_min": 8500.00,
      "salary_max": 12500.00,
      "vacancies": 15,
      "state": "SP",
      "city": "São Paulo",
      "status": "open",
      "registration_start_date": "2026-05-20",
      "registration_end_date": "2026-06-30",
      "exam_date": "2026-09-15",
      "source_url": "https://www.cebraspe.org.br/concursos/...",
      "confidence_level": "high",
      "last_checked_at": "2026-05-27T14:23:00Z"
    }
  ],
  "pagination": {
    "next_cursor": "eyJpZCI6IjU1MGU4NDAwIn0=",
    "has_more": true,
    "total_count": 124
  }
}
```

### `GET /v1/opportunities/{id}`

Detalhe completo de uma oportunidade.

**Response 200:** Estrutura igual ao item acima + campos extras:

```json
{
  ...same as item...,
  "description": "Texto completo extraído do edital...",
  "raw_snapshot_id": "...",
  "verification_history": [
    {
      "checked_at": "2026-05-27T14:23:00Z",
      "check_result": "unchanged",
      "notes": null
    }
  ]
}
```

**Response 404:** Oportunidade não encontrada.

---

## 📡 Sources

### `GET /v1/sources`

Lista de fontes monitoradas.

**Response 200:**

```json
{
  "items": [
    {
      "source_id": "cebraspe",
      "name": "Cebraspe",
      "type": "organizing_board",
      "quality_level": "high",
      "enabled": true,
      "last_successful_check_at": "2026-05-27T14:00:00Z",
      "items_count": 47
    },
    ...
  ]
}
```

### `GET /v1/sources/{source_id}`

Detalhe de uma fonte.

---

## 🎯 Match

### `POST /v1/match`

Calcula score de compatibilidade entre perfil e oportunidades. **Stateless** — perfil não persiste.

**Request body:**

```json
{
  "areas": ["tecnologia", "administrativo"],
  "states": ["SP", "RJ", "PR"],
  "cities": [],
  "education_level": "superior",
  "minimum_salary": 6000,
  "keywords": ["analista de sistemas", "desenvolvedor"],
  "include_remote": true
}
```

**Response 200:**

```json
{
  "matches": [
    {
      "opportunity_id": "550e8400-...",
      "opportunity": { "...resumo da opportunity..." },
      "score": 87,
      "max_score": 100,
      "reasons": [
        {
          "criterion": "area",
          "points": 30,
          "weight": 30,
          "explanation": "Área 'tecnologia' compatível com perfil"
        },
        {
          "criterion": "salary",
          "points": 10,
          "weight": 10,
          "explanation": "Salário R$ 8.500-12.500 acima do mínimo R$ 6.000"
        },
        {
          "criterion": "location",
          "points": 15,
          "weight": 15,
          "explanation": "Localização SP está no perfil"
        },
        {
          "criterion": "education",
          "points": 15,
          "weight": 15,
          "explanation": "Escolaridade 'superior' compatível"
        },
        {
          "criterion": "keyword",
          "points": 17,
          "weight": 20,
          "explanation": "Match em 'analista de sistemas' (case-insensitive)"
        },
        {
          "criterion": "status",
          "points": 0,
          "weight": 10,
          "explanation": "Inscrições encerram em 3 dias (status: open, mas curto prazo)"
        }
      ]
    }
  ],
  "total_evaluated": 124,
  "total_returned": 50
}
```

---

## 📄 OpenAPI / Docs

| Endpoint | Description |
|---|---|
| `GET /docs` | Scalar UI (interface moderna) |
| `GET /redoc` | ReDoc (alternativa) |
| `GET /openapi.json` | OpenAPI 3.1 spec raw |

---

## ⚠️ Error Format (RFC 7807)

Todos os erros seguem [RFC 7807 Problem Details](https://datatracker.ietf.org/doc/html/rfc7807):

```json
{
  "type": "https://civic-radar.dev/errors/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "Field 'state' must be a 2-letter UF code",
  "instance": "/v1/opportunities",
  "errors": [
    {
      "loc": ["query", "state"],
      "msg": "expected length 2",
      "input": "SPP"
    }
  ]
}
```

| Status | Significado |
|---|---|
| `400` | Bad request (malformed) |
| `404` | Not found |
| `422` | Validation error (Pydantic) |
| `429` | Rate limit exceeded |
| `500` | Internal error |
| `503` | Service unavailable (ex: DB down) |

---

## 🧪 Examples (curl)

```bash
# Health
curl http://localhost:8000/health | jq

# Opportunities filtradas
curl "http://localhost:8000/v1/opportunities?state=SP&area=tecnologia&salary_min=6000" | jq

# Match
curl -X POST http://localhost:8000/v1/match \
  -H "Content-Type: application/json" \
  -d '{
    "areas": ["tecnologia"],
    "states": ["SP"],
    "education_level": "superior",
    "minimum_salary": 6000,
    "keywords": ["analista"]
  }' | jq
```

---

## 🔮 Roadmap da API

- [ ] `GET /v1/opportunities/{id}/history` — Histórico completo
- [ ] `GET /v1/sources/{id}/health` — Parser health
- [ ] `GET /v1/feed.rss` — RSS feed
- [ ] `POST /v1/webhooks` — Webhook subscription
- [ ] `GET /v1/areas` — Lista de áreas conhecidas
- [ ] `GET /v1/boards` — Lista de bancas conhecidas
