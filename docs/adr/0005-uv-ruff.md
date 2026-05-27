# ADR 0005 — Python tooling: uv + ruff + mypy + pytest

**Status:** Accepted
**Date:** 2026-05-27
**Deciders:** Initial maintainers

## Context

Tooling Python tradicional (`pip` + `virtualenv` + `setup.py` + `black` + `isort` + `flake8` + `pytest`) é fragmentado e lento. Projetos open source modernos (2025-2026) estão consolidando em alternativas Rust-based muito mais rápidas e melhor integradas.

Para CivicRadar, queremos setup local em segundos para contribuidores.

## Options Considered

### Package management & venv

| Tool | Speed | Ecosystem | Modern |
|---|---|---|---|
| **uv** | 10-100× pip | Crescendo rápido | ⭐⭐⭐ |
| Poetry | ~pip | Maduro | ⭐⭐ |
| pip + venv | Lento | Padrão | ⭐ |
| Rye | Rápido | Em transição para uv | ⭐⭐ |
| pdm | Rápido | Pequeno | ⭐⭐ |

### Linter & Formatter

| Tool | Substitui | Speed |
|---|---|---|
| **ruff** | black, isort, flake8, pylint (parcial), pydocstyle, pyupgrade | 10-100× |
| black + isort + flake8 | — | Lento |

### Type checker

| Tool | Notes |
|---|---|
| **mypy** | Maduro, padrão |
| pyright | Rápido (Rust), mas ecosystem menor |
| pyre | Facebook, complexo |

### Test runner

| Tool | Notes |
|---|---|
| **pytest** | Padrão indiscutível |

## Decision

| Camada | Escolha |
|---|---|
| Package manager + venv | **uv** |
| Lint + format | **ruff** (`check` + `format`) |
| Type check | **mypy** (strict mode) |
| Test runner | **pytest** + pytest-asyncio + pytest-cov |
| Coverage | **coverage.py** (via pytest-cov) |
| Mock HTTP | **respx** (para httpx) |
| Time mocking | **freezegun** |

## Rationale

### uv

- Escrito em Rust pela [Astral](https://astral.sh/) (criadores do ruff)
- `uv sync` em segundos onde Poetry leva minutos
- Suporte nativo a `pyproject.toml`
- Pode instalar Python automaticamente (`uv python install 3.12`)
- Workspaces para monorepo
- Active development; já é stable

### ruff

- Substitui 5+ ferramentas em um único binário
- Configuração unificada no `pyproject.toml`
- Auto-fix poderoso
- Format compatível com black

### mypy `--strict`

- Padrão da comunidade
- Pyright seria mais rápido mas mypy tem ecosystem maduro
- Strict mode pega ~95% de erros de tipo em tempo de dev

## Consequences

### Positivas

- **Setup local em ~5 segundos** (`uv sync`)
- Um único comando para lint: `uv run ruff check --fix .`
- Pre-commit hooks rápidos
- CI lint job em segundos

### Negativas / Trade-offs

- **uv ainda em rápida evolução** — Pode ter quebra de compatibilidade em majors
  - **Mitigação:** Pin uv version em CI; documentar versão recomendada
- **Devs sem familiaridade com uv** — Curva curta mas existe
  - **Mitigação:** Comandos básicos em CONTRIBUTING.md
- **Ruff não substitui mypy** — Type checking ainda requer mypy
  - **Mitigação:** OK, ruff + mypy é stack padrão

### Action Items

- `pyproject.toml` na raiz com `[tool.uv.workspace]` para monorepo
- `[tool.ruff]` config compartilhada
- `[tool.mypy]` strict
- `[tool.pytest.ini_options]` com `--cov-fail-under=70`
- Documentar comandos em README e CONTRIBUTING
- Pre-commit hook para `ruff check --fix && ruff format`
