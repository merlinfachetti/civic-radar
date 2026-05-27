# ADR 0003 — License: AGPL-3.0

**Status:** Accepted
**Date:** 2026-05-27
**Deciders:** Initial maintainers

## Context

Precisamos escolher uma licença open source que:

- Mantenha o projeto **aberto na prática** (não apenas no nome)
- Não permita que um competidor fechado pegue o código, hospede como SaaS e nunca contribua de volta
- Permita uso pessoal/educacional/governamental sem fricção
- Seja amplamente reconhecida (OSI approved)

## Options Considered

| Licença | Modelo | Strong copyleft | Network use | Empresa-friendly |
|---|---|:---:|:---:|:---:|
| **AGPL-3.0** | Copyleft | ✅ | ✅ (require source) | Médio |
| GPL-3.0 | Copyleft | ✅ | ❌ (SaaS escape) | Médio |
| MPL-2.0 | Weak copyleft | Parcial | ❌ | Alto |
| Apache-2.0 | Permissive | ❌ | ❌ | Muito alto |
| MIT | Permissive | ❌ | ❌ | Muito alto |
| BSL/SSPL | Source-available | ✅ | ✅ | Baixo (não OSI) |

**Network use clause** = exige que código modificado seja disponibilizado mesmo quando "uso" é apenas via rede (SaaS).

## Decision

**AGPL-3.0** ([texto oficial](https://www.gnu.org/licenses/agpl-3.0.txt)).

## Rationale

CivicRadar é uma **ferramenta de civic-tech** que melhora acesso a informação pública. A licença AGPL-3.0:

1. **Protege o ecossistema aberto** — Forks SaaS fechados são obrigados a publicar modificações
2. **Encoraja contribuição de volta** — Empresas que querem usar comercialmente precisam contribuir
3. **Mantém alinhamento com a missão** — Open data não deve virar produto fechado

## Consequences

### Positivas

- Modificações em fork SaaS devem ser open-source
- Trabalho da comunidade não é "capturado" por empresa
- Alinha com filosofia de civic-tech / open data

### Negativas / Trade-offs

- **Adoção empresarial reduzida** — Algumas empresas vetam AGPL por política. Aceitável: nosso foco é comunidade, não enterprise.
- **Compatibilidade com outras libs** — AGPL é forte; algumas libs MIT/Apache podem coexistir, mas mistura com GPL/LGPL requer cuidado.
- **Complexidade percebida** — Mais difícil de explicar que MIT.

### Action Items

- `LICENSE` no root com texto completo AGPL-3.0
- Headers de licença em arquivos críticos? **Não obrigatório** — `LICENSE` no root é suficiente para AGPL
- `README.md` declara licença e link
- Considerar dual-license CLA no futuro **apenas** se necessário (requer novo ADR)

## Re-evaluation

Esta decisão pode ser revisitada se:

- Comunidade pedir maioritariamente (votação aberta)
- Necessidade clara de adoção empresarial (raro para civic-tech)
- Substituição por licença equivalente ou mais protetora (ex: AGPL-4 se um dia existir)

Mudança de licença requer novo ADR aprovado por maioria absoluta de maintainers.
