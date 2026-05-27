# Architecture

> Data flow diagrams and architectural decisions for CivicRadar.

For technical principles and an overall view, see [`TECH_FOUNDATION.md`](./TECH_FOUNDATION.md).
For specific decisions, see [`adr/`](./adr/).

---

## 🏛️ Macro view

```mermaid
flowchart TB
    subgraph Public["🌐 Public Sources"]
        F1[Cebraspe]
        F2[FGV]
        F3[PCI Concursos]
        F4[Future sources]
    end

    subgraph Ingest["🔄 Ingestion"]
        I1[Async Crawler]
        I2[Raw Snapshot Store]
        I3[Parser]
        I4[Normalizer]
    end

    subgraph Core["💾 Core"]
        D1[(SQLite/Postgres)]
        D2[Migrations]
    end

    subgraph Service["📡 Service Layer"]
        S1[FastAPI]
        S2[Match Engine]
        S3[OpenAPI 3.1]
        S4[Scalar UI]
        S5[Typer CLI]
    end

    subgraph Client["🎨 Client"]
        C1[Next.js 15]
        C2[shadcn/ui]
        C3[React Query]
        C4[Mobile/Tablet/Desktop]
    end

    F1 & F2 & F3 & F4 -.scheduled.-> I1
    I1 --> I2
    I1 --> I3
    I3 --> I4
    I4 --> D1
    I2 --> D1
    D1 --> S1
    S1 --> S2
    S1 --> S3 --> S4
    S1 --> C1
    S5 --> D1
    C1 --> C2
    C1 --> C3
    C1 --> C4
```

---

## 🔄 Ingestion flow

```mermaid
sequenceDiagram
    participant CR as Cron / CLI
    participant CRW as Crawler
    participant SRC as Source (e.g., Cebraspe)
    participant RSS as RawSnapshotStore
    participant PRS as Parser
    participant NRM as Normalizer
    participant DB as Database

    CR->>CRW: crawl --source cebraspe
    CRW->>SRC: GET /concursos/abertos (rate-limited)
    SRC-->>CRW: HTML
    CRW->>RSS: save snapshot (hash, captured_at)
    CRW->>PRS: parse(snapshot)
    PRS-->>CRW: list[ParsedOpportunity]
    CRW->>NRM: normalize each
    NRM-->>CRW: list[Opportunity]
    CRW->>DB: upsert opportunities
    Note over DB: confidence_level + last_checked_at
    CRW-->>CR: report (X new, Y updated, Z gone)
```

**Key points:**
- The crawler **never** writes to the DB directly; it always goes through the normalizer
- Raw snapshots enable **retroactive re-parsing** if the parser improves
- `content_hash` avoids unnecessary re-parsing (skip if unchanged)
- Upsert by `(source_id, source_url)` prevents duplicates

---

## 🌊 Request flow (API)

```mermaid
sequenceDiagram
    participant U as User Browser
    participant N as Next.js (SSR)
    participant API as FastAPI
    participant DB as Database
    participant M as Match Engine

    U->>N: GET /opportunities?state=SP
    N->>API: GET /v1/opportunities?state=SP
    API->>API: validate query params (Pydantic)
    API->>DB: SELECT ... WHERE state='SP' (indexed)
    DB-->>API: rows
    API-->>N: JSON { items, pagination }
    N->>N: hydrate React components
    N-->>U: HTML + JSON for hydration

    Note over U: Later: client-side filter change
    U->>N: client-side update
    N->>API: GET /v1/opportunities?state=SP&area=ti
    API-->>N: JSON
    N-->>U: re-render via React Query cache
```

---

## 🎯 Match flow

```mermaid
sequenceDiagram
    participant U as User
    participant W as Web (/profile-match)
    participant API as FastAPI
    participant M as Match Engine
    participant DB as Database

    U->>W: fills the MatchProfile form
    W->>W: persists to localStorage
    W->>API: POST /v1/match { profile }
    API->>DB: SELECT opportunities WHERE status='open'
    DB-->>API: candidates
    API->>M: score(profile, candidate) for each
    M-->>API: list[MatchResult { score, reasons }]
    API-->>W: ordered by score desc
    W-->>U: render cards with radial + reasons
```

**Characteristics:**
- **Stateless** — Profile is not persisted server-side
- **Deterministic** — Same input → same output
- **Explainable** — Every score comes with a breakdown
- **Limited** — Only considers `status='open'` (active openings)

---

## 📊 Data model

```mermaid
erDiagram
    Source ||--o{ Opportunity : provides
    Source ||--o{ RawSnapshot : captured
    Opportunity ||--o| RawSnapshot : derived_from
    Opportunity ||--o{ OpportunityVerification : has_history

    Source {
        UUID id PK
        string source_id UK
        string name
        string type
        string base_url
        string quality_level
        bool enabled
        string parser_name
        int rate_limit_seconds
        datetime created_at
        datetime updated_at
    }

    Opportunity {
        UUID id PK
        UUID source_id FK
        string title
        text description
        string organization
        string board
        string area
        string position_name
        string education_level
        decimal salary_min
        decimal salary_max
        int vacancies
        string state
        string city
        string status
        date registration_start_date
        date registration_end_date
        date exam_date
        string source_url
        string confidence_level
        datetime last_checked_at
    }

    RawSnapshot {
        UUID id PK
        UUID source_id FK
        string url
        string content_hash
        string content_type
        text raw_content_path
        datetime captured_at
        string parser_version
    }

    OpportunityVerification {
        UUID id PK
        UUID opportunity_id FK
        datetime checked_at
        string check_result
        text notes
    }
```

---

## 🧩 Plugin architecture (crawlers)

```mermaid
classDiagram
    class BaseCrawler {
        <<abstract>>
        +str source_id
        +int rate_limit_seconds
        +fetch_list() list~RawSnapshot~
        +fetch_detail(snapshot) RawSnapshot
        #_respect_robots_txt()
        #_rate_limited_get(url)
    }

    class BaseParser {
        <<protocol>>
        +str source_id
        +str parser_version
        +parse(snapshot) list~ParsedOpportunity~
    }

    class CebraspeCrawler {
        +source_id = "cebraspe"
    }
    class FGVCrawler {
        +source_id = "fgv"
    }
    class PCICrawler {
        +source_id = "pci-concursos"
    }

    class CebraspeParser
    class FGVParser
    class PCIParser

    class Normalizer {
        +normalize(parsed) Opportunity
    }

    BaseCrawler <|-- CebraspeCrawler
    BaseCrawler <|-- FGVCrawler
    BaseCrawler <|-- PCICrawler
    BaseParser <|.. CebraspeParser
    BaseParser <|.. FGVParser
    BaseParser <|.. PCIParser
    CebraspeCrawler ..> CebraspeParser
    FGVCrawler ..> FGVParser
    PCICrawler ..> PCIParser
    CebraspeParser --> Normalizer
    FGVParser --> Normalizer
    PCIParser --> Normalizer
```

For implementation details, see [`DATA_SOURCES.md`](./DATA_SOURCES.md).

---

## 🎨 Frontend architecture

```mermaid
flowchart LR
    subgraph App["Next.js 15 App Router"]
        L[layout.tsx]
        P1["/page.tsx (landing)"]
        P2["/opportunities/page.tsx"]
        P3["/opportunities/[id]/page.tsx"]
        P4["/profile-match/page.tsx"]
        P5["/sources/page.tsx"]
    end

    subgraph Lib["lib/"]
        AC[api-client.ts]
        Q[react-query setup]
        Z[zod schemas]
    end

    subgraph UI["components/"]
        OC[OpportunityCard]
        FS[FilterSheet]
        CP[CommandPalette]
        MS[MatchScoreVisual]
        SC[SourceConfidenceBadge]
        SH[shadcn/ui base]
    end

    subgraph Style["styles/"]
        T[tailwind.config.ts]
        TK[design tokens]
        TH[theme provider]
    end

    L --> P1 & P2 & P3 & P4 & P5
    P2 --> OC & FS
    P3 --> SC & MS
    P4 --> MS
    OC & FS & CP & MS & SC --> SH
    P1 & P2 & P3 --> AC
    AC --> Q
    AC --> Z
    SH --> T
    L --> TH
    T --> TK
```

---

## 🚦 Opportunity states

```mermaid
stateDiagram-v2
    [*] --> Draft : crawler discovered but fields missing
    Draft --> Open : registration_start_date <= today <= registration_end_date
    Draft --> Closed : registration_end_date < today
    Open --> Closed : registration_end_date < today
    Open --> Cancelled : cancellation detected at source
    Closed --> [*]
    Cancelled --> [*]
```

---

## 📦 Container architecture (Docker Compose)

```mermaid
flowchart LR
    subgraph DC[docker-compose.yml]
        API["api (FastAPI)<br/>:8000"]
        WEB["web (Next.js)<br/>:3000"]
        VOL[("data/<br/>SQLite volume")]
    end

    Internet[👤 User] --> WEB
    WEB -->|GET /v1/*| API
    API --> VOL
```

In **production**, this architecture expands with:
- Reverse proxy (Caddy / Nginx)
- Standalone Postgres
- Redis for cache
- Crawler worker in its own container

---

## 🔗 Links

- [`PRODUCT_FOUNDATION.md`](./PRODUCT_FOUNDATION.md) — Vision, scope, principles
- [`TECH_FOUNDATION.md`](./TECH_FOUNDATION.md) — Stack, contracts, testing
- [`DATA_SOURCES.md`](./DATA_SOURCES.md) — Adding new sources
- [`API.md`](./API.md) — Endpoint reference
- [`adr/`](./adr/) — Specific architecture decisions
