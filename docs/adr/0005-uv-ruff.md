# ADR 0005 — Python tooling: uv + ruff + mypy + pytest

**Status:** Accepted
**Date:** 2026-05-27
**Deciders:** Initial maintainers

## Context

Traditional Python tooling (`pip` + `virtualenv` + `setup.py` + `black` + `isort` + `flake8` + `pytest`) is fragmented and slow. Modern open source projects (2025–2026) are consolidating around Rust-based alternatives that are much faster and better integrated.

For CivicRadar we want sub-second local setup for contributors.

## Options considered

### Package management & venv

| Tool | Speed | Ecosystem | Modern |
|---|---|---|---|
| **uv** | 10-100× pip | Growing fast | ⭐⭐⭐ |
| Poetry | ~pip | Mature | ⭐⭐ |
| pip + venv | Slow | Standard | ⭐ |
| Rye | Fast | Migrating to uv | ⭐⭐ |
| pdm | Fast | Small | ⭐⭐ |

### Linter & formatter

| Tool | Replaces | Speed |
|---|---|---|
| **ruff** | black, isort, flake8, pylint (partial), pydocstyle, pyupgrade | 10-100× |
| black + isort + flake8 | — | Slow |

### Type checker

| Tool | Notes |
|---|---|
| **mypy** | Mature, standard |
| pyright | Fast (Rust), but smaller ecosystem |
| pyre | Facebook, complex |

### Test runner

| Tool | Notes |
|---|---|
| **pytest** | Undisputed standard |

## Decision

| Layer | Pick |
|---|---|
| Package manager + venv | **uv** |
| Lint + format | **ruff** (`check` + `format`) |
| Type check | **mypy** (strict mode) |
| Test runner | **pytest** + pytest-asyncio + pytest-cov |
| Coverage | **coverage.py** (via pytest-cov) |
| HTTP mock | **respx** (for httpx) |
| Time mocking | **freezegun** |

## Rationale

### uv

- Rust binary from [Astral](https://astral.sh/) (the ruff authors)
- `uv sync` in seconds where Poetry takes minutes
- Native `pyproject.toml` support
- Can install Python automatically (`uv python install 3.12`)
- Workspaces for monorepos
- Active development; already stable

### ruff

- Replaces 5+ tools with a single binary
- Unified configuration in `pyproject.toml`
- Powerful auto-fix
- Format compatible with black

### mypy `--strict`

- Community standard
- Pyright would be faster but mypy has the richer ecosystem
- Strict mode catches ~95% of type errors at development time

## Consequences

### Positive

- **Local setup in ~5 seconds** (`uv sync`)
- A single command lints everything: `uv run ruff check --fix .`
- Fast pre-commit hooks
- CI lint job runs in seconds

### Negative / trade-offs

- **uv still evolves fast** — Possible compatibility breaks in major versions
  - **Mitigation:** Pin uv version in CI; document the recommended version
- **Devs unfamiliar with uv** — Short but real learning curve
  - **Mitigation:** Cheat sheet in CONTRIBUTING.md
- **Ruff does not replace mypy** — Type checking still requires mypy
  - **Mitigation:** OK, ruff + mypy is the modern standard pair

### Action items

- `pyproject.toml` at the root with `[tool.uv.workspace]` for the monorepo
- Shared `[tool.ruff]` config
- Strict `[tool.mypy]`
- `[tool.pytest.ini_options]` with `--cov-fail-under=70`
- Document commands in README and CONTRIBUTING
- Pre-commit hook for `ruff check --fix && ruff format`
