# Contributing to CivicRadar

Obrigado por considerar contribuir! 🙏 Este projeto só faz sentido como esforço comunitário, e toda contribuição é valiosa — desde corrigir um typo, adicionar uma nova fonte, melhorar acessibilidade, traduzir UI, ou propor uma ideia nova.

---

## 📋 Code of Conduct

Antes de tudo, leia o [`CODE_OF_CONDUCT.md`](./CODE_OF_CONDUCT.md). Ao participar, você concorda em respeitá-lo.

---

## 🚀 Setup local

### Pré-requisitos

- [**uv**](https://docs.astral.sh/uv/getting-started/installation/) — Python toolchain (instala Python 3.12+ automaticamente)
- [**pnpm**](https://pnpm.io/installation) — Node 20+ (recomendado via [Volta](https://volta.sh/) ou [fnm](https://github.com/Schniz/fnm))
- [**Docker**](https://docs.docker.com/get-docker/) + Docker Compose — opcional mas recomendado

### Clone e setup

```bash
git clone https://github.com/merlinfachetti/civic-radar.git
cd civic-radar

# Instala pre-commit hooks
pre-commit install   # opcional mas recomendado

# Backend
cd apps/api
uv sync               # cria .venv e instala tudo
uv run alembic upgrade head
uv run civic_radar seed

# Frontend (em outro terminal)
cd apps/web
pnpm install
pnpm dev
```

### Via Docker (mais simples)

```bash
docker compose up -d
docker compose logs -f
```

---

## 🧪 Rodando testes

```bash
# Backend
cd apps/api
uv run pytest                          # todos os testes
uv run pytest tests/unit -v            # apenas unit
uv run pytest --cov                    # com coverage

# Frontend
cd apps/web
pnpm test                              # vitest watch
pnpm test:ci                           # one-shot com coverage

# Crawlers
cd crawlers
uv run pytest                          # parsers contra fixtures
```

---

## ✨ Onde começar?

### 🌱 Primeira contribuição

Procure issues marcadas com [`good first issue`](https://github.com/merlinfachetti/civic-radar/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22). Essas são deliberadamente delimitadas para ser fáceis de pegar sem precisar entender o projeto todo.

Bons primeiros caminhos:

- 📚 **Documentação** — typos, traduções, exemplos mais claros, screenshots
- 🌐 **i18n** — strings PT-BR/EN faltando
- ♿ **Acessibilidade** — atributos ARIA, contraste, navegação por teclado
- 🧪 **Testes** — coverage gaps, edge cases
- 🎨 **UI polish** — micro-animações, empty states, loading states

### ➕ Adicionar nova fonte

Veja [`DATA_SOURCES.md`](./DATA_SOURCES.md) para o passo-a-passo completo.

### 🔧 Corrigir parser quebrado

1. Reproduza com fixture
2. Atualize fixture se a fonte mudou
3. Bump `parser_version`
4. Adicione golden file
5. PR

---

## 🔀 Workflow de PRs

> **Estado atual (pré-MVP):** commits diretos para `main` são aceitos para maintainers. Post-MVP, PRs serão obrigatórios e usaremos branch protection.

### Para contribuidores externos

1. **Fork** o repositório
2. **Crie uma branch** descritiva: `feat/adicionar-fonte-vunesp`, `fix/parser-cebraspe-edge-case`, `docs/melhorar-readme`
3. **Faça suas mudanças** seguindo as convenções abaixo
4. **Rode testes localmente** antes de push
5. **Abra um PR** usando o template, explicando _why_ além de _what_

### Convenções de commit

Usamos [**Conventional Commits**](https://www.conventionalcommits.org/pt-br/v1.0.0/):

```
<tipo>(<escopo opcional>): <descrição curta>

[corpo opcional]

[footer opcional]
```

**Tipos:**

| Tipo | Quando usar |
|---|---|
| `feat` | Nova funcionalidade |
| `fix` | Correção de bug |
| `docs` | Apenas documentação |
| `style` | Formatação, sem mudança de código |
| `refactor` | Refactor sem mudança de comportamento |
| `test` | Adicionar/corrigir testes |
| `chore` | Tarefas de manutenção, deps |
| `perf` | Performance |
| `ci` | CI/CD |

**Exemplos:**

```
feat(crawlers): adicionar fonte Vunesp

Implementa crawler + parser + 4 fixtures HTML para a banca Vunesp.
Resolves #42
```

```
fix(api): paginação cursor com filtros combinados

Cursor estava perdendo state quando ?state e ?area eram passados juntos.
```

```
docs(data-sources): clarificar política de rate-limit
```

---

## 📐 Padrões de código

### Python (`apps/api/`, `crawlers/`)

- **Formatter**: [ruff](https://docs.astral.sh/ruff/) (substitui black + isort + flake8)
- **Linter**: ruff
- **Type checker**: mypy `--strict`
- **Line length**: 100
- **Naming**: snake_case para funções/variáveis, PascalCase para classes
- **Docstrings**: apenas quando o "porquê" não é óbvio. Estilo Google ou simples.
- **Async**: prefira `async def` em I/O paths

```bash
uv run ruff check --fix .       # fix automático
uv run ruff format .            # formatação
uv run mypy src/                # type check
```

### TypeScript (`apps/web/`)

- **Formatter**: Prettier
- **Linter**: ESLint (Next.js config + custom rules)
- **`strict: true`** no tsconfig
- **Naming**: camelCase para variáveis/funções, PascalCase para componentes/types
- **Imports**: ordenados (lib → external → internal → relative)
- **Componentes**: function components, hooks, prefer composição sobre props complexas

```bash
pnpm lint                       # eslint
pnpm format                     # prettier
pnpm typecheck                  # tsc --noEmit
```

### Testes

- **Nome descritivo**: `test_parser_extracts_salary_when_only_max_is_present`
- **AAA pattern**: Arrange, Act, Assert
- **Fixtures > mocks** quando possível
- **No sleep, no HTTP real** — use freezegun/respx

---

## 🏷️ Labels e Issue Types

Quando abrir uma issue, use os templates disponíveis. Labels comuns:

| Label | Significado |
|---|---|
| `good first issue` | Ideal para primeira contribuição |
| `help wanted` | Maintainers buscam ajuda externa |
| `source` | Relacionado a fontes de dados |
| `parser` | Relacionado a parsers |
| `frontend` | Web app |
| `backend` | API |
| `documentation` | Docs |
| `bug` | Comportamento incorreto |
| `enhancement` | Melhoria |
| `legal-review` | Precisa análise legal/ética |
| `data-quality` | Qualidade dos dados extraídos |
| `accessibility` | A11y |
| `performance` | Perf |
| `security` | Segurança (use [SECURITY.md](./SECURITY.md) para vulnerabilidades) |

---

## 🌍 Tradução

CivicRadar é primariamente em **PT-BR** (público brasileiro), com **EN** como fallback secundário.

Arquivos de tradução em `apps/web/src/i18n/`. PRs de tradução são muito bem-vindos!

---

## 🎯 Princípios para PRs

### Faça

✅ Mudanças pequenas e focadas (1 PR = 1 mudança lógica)
✅ Testes para novo código
✅ Atualizar docs se aplicável
✅ Explicar _why_ no PR description
✅ Linkar issue relacionada
✅ Responder a feedback respeitosamente

### Evite

❌ PRs gigantes misturando features/refactor/docs
❌ Mudar formatação de arquivos não relacionados
❌ Adicionar dependência sem justificativa
❌ Reverter decisão sem ADR
❌ Crawling agressivo sem rate limit
❌ Republicar conteúdo integral de terceiros

---

## 💬 Comunicação

- **Discussões abertas:** [GitHub Discussions](https://github.com/merlinfachetti/civic-radar/discussions)
- **Bugs/features:** [GitHub Issues](https://github.com/merlinfachetti/civic-radar/issues)
- **Vulnerabilidades de segurança:** [SECURITY.md](./SECURITY.md) (não use issue pública)

---

## 🙏 Agradecimentos

Toda contribuição — mesmo a menor — é registrada em `CONTRIBUTORS.md` (em breve, gerado automaticamente).

Obrigado por fazer parte! 🚀
