# Contributing to CivicRadar

Thanks for considering a contribution! 🙏 This project only makes sense as a community effort — every contribution counts, from fixing a typo, to adding a new source, improving accessibility, translating the UI or floating a fresh idea.

---

## 📋 Code of Conduct

Read the [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md) first. By participating you agree to follow it.

---

## 🚀 Local setup

### Prerequisites

- [**uv**](https://docs.astral.sh/uv/getting-started/installation/) — Python toolchain (installs Python 3.12+ automatically)
- [**pnpm**](https://pnpm.io/installation) — Node 20+ (we recommend [Volta](https://volta.sh/) or [fnm](https://github.com/Schniz/fnm))
- [**Docker**](https://docs.docker.com/get-docker/) + Docker Compose — optional but recommended

### Clone and bootstrap

```bash
git clone https://github.com/merlinfachetti/civic-radar.git
cd civic-radar

# Install pre-commit hooks
pre-commit install   # optional but recommended

# Backend
cd apps/api
uv sync               # creates .venv and installs everything
uv run alembic upgrade head
uv run civic_radar seed

# Frontend (in another terminal)
cd apps/web
pnpm install
pnpm dev
```

### Via Docker (simpler)

```bash
docker compose up -d
docker compose logs -f
```

---

## 🧪 Running tests

```bash
# Backend
cd apps/api
uv run pytest                          # all tests
uv run pytest tests/unit -v            # unit only
uv run pytest --cov                    # with coverage

# Frontend
cd apps/web
pnpm test                              # vitest watch
pnpm test:ci                           # one-shot with coverage

# Crawlers
cd crawlers
uv run pytest                          # parsers against fixtures
```

---

## ✨ Where to start?

### 🌱 First contribution

Look for issues labeled [`good first issue`](https://github.com/merlinfachetti/civic-radar/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22). They are deliberately scoped to be pickable without reading the whole project.

Great first paths:

- 📚 **Documentation** — typos, translations, clearer examples, screenshots
- 🌐 **i18n** — missing PT-BR/EN strings
- ♿ **Accessibility** — ARIA attributes, contrast, keyboard navigation
- 🧪 **Tests** — coverage gaps, edge cases
- 🎨 **UI polish** — micro-animations, empty states, loading states

### ➕ Adding a new source

See [`DATA_SOURCES.md`](./DATA_SOURCES.md) for the full walkthrough.

### 🔧 Fixing a broken parser

1. Reproduce with a fixture
2. Update the fixture if the source changed layout
3. Bump `parser_version`
4. Add a golden file
5. PR

---

## 🔀 PR workflow

> **Current state (pre-MVP):** direct commits to `main` are accepted for maintainers. Post-MVP, PRs will be required and branch protection enabled.

### For external contributors

1. **Fork** the repository
2. **Create a descriptive branch**: `feat/add-source-vunesp`, `fix/cebraspe-parser-edge-case`, `docs/improve-readme`
3. **Make your changes** following the conventions below
4. **Run tests locally** before pushing
5. **Open a PR** using the template, explaining _why_ as well as _what_

### Commit conventions

We use [**Conventional Commits**](https://www.conventionalcommits.org/):

```
<type>(<optional scope>): <short description>

[optional body]

[optional footer]
```

**Types:**

| Type | When to use |
|---|---|
| `feat` | New functionality |
| `fix` | Bug fix |
| `docs` | Documentation only |
| `style` | Formatting, no code change |
| `refactor` | Refactor without behavior change |
| `test` | Add or fix tests |
| `chore` | Maintenance, dependencies |
| `perf` | Performance |
| `ci` | CI/CD |

**Examples:**

```
feat(crawlers): add Vunesp source

Implements crawler + parser + 4 HTML fixtures for the Vunesp board.
Resolves #42
```

```
fix(api): cursor pagination with combined filters

Cursor was losing state when ?state and ?area were passed together.
```

```
docs(data-sources): clarify rate-limit policy
```

---

## 📐 Code standards

### Python (`apps/api/`, `crawlers/`)

- **Formatter**: [ruff](https://docs.astral.sh/ruff/) (replaces black + isort + flake8)
- **Linter**: ruff
- **Type checker**: mypy `--strict`
- **Line length**: 100
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Docstrings**: only when the "why" is non-obvious. Google or simple style.
- **Async**: prefer `async def` on I/O paths

```bash
uv run ruff check --fix .       # automatic fix
uv run ruff format .            # formatting
uv run mypy src/                # type check
```

### TypeScript (`apps/web/`)

- **Formatter**: Prettier
- **Linter**: ESLint (Next.js config + custom rules)
- **`strict: true`** in tsconfig
- **Naming**: camelCase for variables/functions, PascalCase for components/types
- **Imports**: ordered (lib → external → internal → relative)
- **Components**: function components, hooks, prefer composition over complex props

```bash
pnpm lint                       # eslint
pnpm format                     # prettier
pnpm typecheck                  # tsc --noEmit
```

### Tests

- **Descriptive names**: `test_parser_extracts_salary_when_only_max_is_present`
- **AAA pattern**: Arrange, Act, Assert
- **Fixtures > mocks** when possible
- **No sleep, no real HTTP** — use freezegun/respx

---

## 🏷️ Labels and issue types

Use the templates when opening an issue. Common labels:

| Label | Meaning |
|---|---|
| `good first issue` | Ideal for a first contribution |
| `help wanted` | Maintainers want external help |
| `source` | Related to data sources |
| `parser` | Related to parsers |
| `frontend` | Web app |
| `backend` | API |
| `documentation` | Docs |
| `bug` | Incorrect behavior |
| `enhancement` | Improvement |
| `legal-review` | Needs legal/ethical review |
| `data-quality` | Quality of extracted data |
| `accessibility` | a11y |
| `performance` | Perf |
| `security` | Security (use [SECURITY.md](./SECURITY.md) for vulnerabilities) |

---

## 🌍 Translation

CivicRadar is primarily **PT-BR** (Brazilian audience), with **EN** as the secondary fallback.

Translation files live under `apps/web/src/i18n/`. Translation PRs are very welcome!

**Note:** Engineering artifacts (docs, comments, commit messages, PR descriptions, issues) are always written in **English**. Only product-facing UI strings follow the i18n strategy.

---

## 🎯 PR principles

### Do

✅ Small, focused changes (1 PR = 1 logical change)
✅ Tests for new code
✅ Update docs when applicable
✅ Explain _why_ in the PR description
✅ Link the related issue
✅ Respond to feedback respectfully

### Avoid

❌ Huge PRs mixing features/refactors/docs
❌ Reformatting unrelated files
❌ Adding a dependency without justification
❌ Reverting a decision without an ADR
❌ Aggressive crawling without a rate limit
❌ Republishing full third-party content

---

## 💬 Communication

- **Open discussion:** [GitHub Discussions](https://github.com/merlinfachetti/civic-radar/discussions)
- **Bugs/features:** [GitHub Issues](https://github.com/merlinfachetti/civic-radar/issues)
- **Security vulnerabilities:** [SECURITY.md](./SECURITY.md) (never a public issue)

---

## 🙏 Acknowledgements

Every contribution — however small — gets recorded in `CONTRIBUTORS.md` (coming soon, automatically generated).

Thanks for being part of this! 🚀
