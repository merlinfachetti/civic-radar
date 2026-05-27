# Roadmap

> This document mirrors (at a high level) the GitHub milestones. For the live backlog and up-to-date issues, see [Milestones](https://github.com/merlinfachetti/civic-radar/milestones) and [Issues](https://github.com/merlinfachetti/civic-radar/issues).

---

## 🟢 M0 — Foundation _(initial commit)_

Establish the technical foundation and open source strategy.

- ✅ Monorepo structure
- ✅ AGPL-3.0 LICENSE
- ✅ Detailed README
- ✅ PRODUCT_FOUNDATION & TECH_FOUNDATION
- ✅ CONTRIBUTING + CODE_OF_CONDUCT + SECURITY
- ✅ Initial ADRs (FastAPI, SQLite-first, AGPL, shadcn/ui, uv)
- ✅ Docker Compose skeleton
- ✅ 4 GitHub Actions workflows
- ✅ Issue templates + PR template + Dependabot
- 📋 Project logo SVG _(good first issue)_

---

## 🚧 M1 — Ingestion MVP

Crawler/parser architecture working across 3 sources.

- [x] Core plugin architecture (`BaseCrawler`, `BaseParser`, `Normalizer`)
- [x] Source: **Cebraspe** (crawler + parser + fixtures)
- [x] Source: **FGV** (crawler + parser + fixtures)
- [x] Source: **PCI Concursos** (crawler + parser + fixtures)
- [x] `RawSnapshotStore` for reproducibility
- [ ] Advanced PDF parser (requirement extraction)
- [ ] Crawl scheduler (APScheduler) _(M2)_
- [ ] Source: Vunesp _(good first issue)_
- [ ] Source: FCC _(good first issue)_
- [ ] Source: IBFC _(good first issue)_

---

## 🚧 M2 — API MVP

Rich FastAPI with navigable OpenAPI.

- [x] FastAPI skeleton
- [x] SQLAlchemy 2.0 async + Alembic
- [x] Models: Opportunity, Source, RawSnapshot
- [x] Endpoints: /health, /v1/opportunities, /v1/opportunities/{id}, /v1/sources, /v1/stats
- [x] Scalar UI at /docs
- [x] Typer CLI (`civic_radar seed`, `serve`, `crawl`)
- [x] structlog logging
- [ ] Cursor-based pagination
- [ ] Rate limiting (slowapi)
- [ ] Cache headers (ETag, Cache-Control)
- [ ] `/v1/opportunities/{id}/history`
- [ ] `/v1/sources/{id}/health`
- [ ] OpenAPI examples for every endpoint _(good first issue)_

---

## 🚧 M3 — Web MVP

Modern, responsive frontend.

- [x] Next.js 15 + App Router + TS strict
- [x] Tailwind v4 + shadcn/ui
- [x] Responsive layout (mobile/tablet/desktop)
- [x] Dark/light theme via next-themes
- [x] /opportunities page with filters
- [x] /opportunities/[id] page
- [x] /sources page
- [x] /about, /contribute pages
- [ ] Landing page with animated hero
- [ ] OpportunityCard mobile variant
- [ ] CommandPalette (⌘K)
- [ ] FilterSheet (drawer on mobile, sidebar on desktop)
- [ ] i18n PT-BR/EN _(good first issue)_
- [ ] A11y audit + axe-core in CI
- [ ] SEO + sitemap

---

## 🔜 M4 — Match Engine

Deterministic, explainable profile matching.

- [ ] Pydantic `MatchProfile` schema
- [ ] Deterministic scoring (area 30, keyword 20, location 15, education 15, salary 10, status 10)
- [ ] `POST /v1/match` endpoint
- [ ] Match reasons in PT-BR/EN
- [ ] Profile form on the frontend (localStorage)
- [ ] Match explainability UI (radial + breakdown)
- [ ] Profile sharing via URL params

---

## 📋 M5 — Alerts

Notifications outside the app.

- [ ] RSS feed `/v1/feed.rss`
- [ ] Webhook subscription
- [ ] Email digest opt-in (self-hosted SMTP)
- [ ] Telegram bot _(good first issue)_
- [ ] Discord webhook _(good first issue)_
- [ ] Saved searches persistence

---

## 🔮 M6 — Intelligence Layer _(post-MVP)_

Additional intelligence, with clear AI disclaimers.

- [ ] Edital summarization (LLM-agnostic interface)
- [ ] Requirement extraction from PDF
- [ ] Deadline warning system
- [ ] Study plan generator (experimental)
- [ ] Historical salary analytics
- [ ] Semantic search over edital content

---

## 🌀 Cross-cutting

Issues without a fixed milestone, always open:

- 📚 Documentation improvements _(good first issue)_
- 🌍 Translation: EN/ES UI _(good first issue)_
- ♿ Accessibility improvements _(good first issue)_
- 🧪 Test coverage gaps _(good first issue)_
- 🎨 UI polish (empty states, loading states, micro-animations)

---

## 📅 Cadence

No strict release schedule before 1.0. Once M4 (Match) is shipped, we will tag `0.1.0` and turn on:

- Branch protection on `main`
- Required PRs for non-trivial changes
- Auto-generated `CHANGELOG.md`
- GitHub Releases

After `1.0.0`, the target is a minor release every 6–8 weeks.
