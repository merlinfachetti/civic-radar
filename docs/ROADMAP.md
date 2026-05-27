# Roadmap

> Este documento espelha (em alto nível) os milestones do GitHub. Para o backlog vivo e issues atualizadas, veja [Milestones](https://github.com/merlinfachetti/civic-radar/milestones) e [Issues](https://github.com/merlinfachetti/civic-radar/issues).

---

## 🟢 M0 — Foundation _(initial commit)_

Estabelecer fundação técnica e estratégia open source.

- ✅ Estrutura monorepo
- ✅ LICENSE AGPL-3.0
- ✅ README detalhado
- ✅ PRODUCT_FOUNDATION & TECH_FOUNDATION
- ✅ CONTRIBUTING + CODE_OF_CONDUCT + SECURITY
- ✅ ADRs iniciais (FastAPI, SQLite-first, AGPL, shadcn/ui, uv)
- ✅ Docker Compose esqueleto
- ✅ 4 GitHub Actions workflows
- ✅ Issue templates + PR template + Dependabot
- 📋 Logo SVG _(good first issue)_

---

## 🚧 M1 — Ingestion MVP

Arquitetura de crawlers e parsers funcionando para 3 fontes.

- [x] Core plugin architecture (`BaseCrawler`, `BaseParser`, `Normalizer`)
- [x] Source: **Cebraspe** (crawler + parser + fixtures)
- [x] Source: **FGV** (crawler + parser + fixtures)
- [x] Source: **PCI Concursos** (crawler + parser + fixtures)
- [x] `RawSnapshotStore` para reprodutibilidade
- [ ] Parser PDF avançado (extração de requisitos)
- [ ] Scheduler de crawls (APScheduler) _(M2)_
- [ ] Source: Vunesp _(good first issue)_
- [ ] Source: FCC _(good first issue)_
- [ ] Source: IBFC _(good first issue)_

---

## 🚧 M2 — API MVP

FastAPI rico com OpenAPI navegável.

- [x] FastAPI skeleton
- [x] SQLAlchemy 2.0 async + Alembic
- [x] Modelos: Opportunity, Source, RawSnapshot
- [x] Endpoints: /health, /v1/opportunities, /v1/opportunities/{id}, /v1/sources, /v1/stats
- [x] Scalar UI em /docs
- [x] CLI Typer (`civic_radar seed`, `serve`, `crawl`)
- [x] Logging structlog
- [ ] Pagination cursor-based
- [ ] Rate limiting (slowapi)
- [ ] Cache headers (ETag, Cache-Control)
- [ ] `/v1/opportunities/{id}/history`
- [ ] `/v1/sources/{id}/health`
- [ ] OpenAPI examples por endpoint _(good first issue)_

---

## 🚧 M3 — Web MVP

Frontend moderno e responsivo.

- [x] Next.js 15 + App Router + TS strict
- [x] Tailwind v4 + shadcn/ui
- [x] Layout responsivo (mobile/tablet/desktop)
- [x] Dark/light theme com next-themes
- [x] Página /opportunities com filtros
- [x] Página /opportunities/[id]
- [x] Página /sources
- [x] Página /about, /contribute
- [ ] Landing page com hero animado
- [ ] OpportunityCard variante mobile
- [ ] CommandPalette (⌘K)
- [ ] FilterSheet (drawer mobile, sidebar desktop)
- [ ] i18n PT-BR/EN _(good first issue)_
- [ ] A11y audit + axe-core no CI
- [ ] SEO + sitemap

---

## 🔜 M4 — Match Engine

Profile matching determinístico e explicável.

- [ ] Pydantic `MatchProfile` schema
- [ ] Scoring determinístico (área 30, keyword 20, location 15, education 15, salary 10, status 10)
- [ ] Endpoint `POST /v1/match`
- [ ] Match reasons em PT-BR/EN
- [ ] Profile form no frontend (localStorage)
- [ ] Match explainability UI (radial + breakdown)
- [ ] Profile sharing via URL params

---

## 📋 M5 — Alerts

Notificações fora do app.

- [ ] RSS feed `/v1/feed.rss`
- [ ] Webhook subscription
- [ ] Email digest opt-in (SMTP self-hosted)
- [ ] Telegram bot _(good first issue)_
- [ ] Discord webhook _(good first issue)_
- [ ] Saved searches persistence

---

## 🔮 M6 — Intelligence Layer _(post-MVP)_

Inteligência adicional, com clear disclaimers de IA.

- [ ] Edital summarization (LLM-agnostic interface)
- [ ] Requirement extraction from PDF
- [ ] Deadline warning system
- [ ] Study plan generator (experimental)
- [ ] Historical salary analytics
- [ ] Semantic search sobre conteúdo de edital

---

## 🌀 Cross-cutting

Issues sem milestone fixo, sempre abertas:

- 📚 Documentation improvements _(good first issue)_
- 🌍 Translation: EN/ES UI _(good first issue)_
- ♿ Accessibility improvements _(good first issue)_
- 🧪 Test coverage gaps _(good first issue)_
- 🎨 UI polish (empty states, loading states, micro-animations)

---

## 📅 Cadência

Sem release schedule rígida pre-1.0. Quando M4 (Match) estiver concluído, faremos release `0.1.0` e ativaremos:

- Branch protection na `main`
- PRs obrigatórios para mudanças não-trivial
- CHANGELOG.md auto-gerado
- GitHub Releases

Após `1.0.0`, target de release minor a cada 6-8 semanas.
