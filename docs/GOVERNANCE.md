# Governance

> Como decisões são tomadas no CivicRadar, e como você pode se tornar maintainer.

---

## 🎯 Filosofia

CivicRadar é um projeto **community-driven** de baixo formalismo. Nosso objetivo é manter contribuições fáceis e decisões transparentes, sem burocracia desnecessária.

---

## 👥 Roles

### Contributors

Qualquer pessoa que abra issue, PR, ou participe de discussões. **Todas** contribuições são valorizadas.

### Maintainers

Pessoas com permissão de merge na `main`. Responsabilidades:

- Revisar e mergear PRs
- Triagem de issues
- Manter qualidade e direção do projeto
- Garantir aderência ao Code of Conduct

**Maintainers iniciais:**

- [@aldenfachetti](https://github.com/aldenfachetti)
- [@merlinfachetti](https://github.com/merlinfachetti)

### Core Maintainers _(futuro)_

Subset de maintainers com permissões adicionais (admin, secrets, billing). Eleitos por consenso dos maintainers atuais quando o projeto crescer.

---

## 🗳️ Processo de Decisão

### Lazy Consensus (default)

Para a **maioria** das decisões — mudanças de código, features, bug fixes, refactors:

1. Abra PR ou issue propondo a mudança
2. Aguarde feedback dos maintainers (até 7 dias)
3. Se nenhum maintainer objetar, considera-se aprovado
4. Pelo menos 1 maintainer faz merge

**Não é necessário voto formal** para decisões pequenas/médias.

### Architecture Decision Records (ADRs)

Decisões arquiteturais **significativas** requerem ADR:

- Mudança de stack (linguagem, framework, DB)
- Mudança de licença
- Mudança nos princípios de produto
- Mudança no schema do banco (breaking)
- Adição de dependência crítica

Processo:

1. Abra issue com label `adr-proposal` descrevendo:
   - **Context** — Por que estamos considerando essa mudança?
   - **Options** — Quais alternativas foram avaliadas?
   - **Decision** — Proposta
   - **Consequences** — Trade-offs aceitos
2. Discussão aberta por **mínimo 7 dias**
3. Maintainers votam (👍 / 👎 / 🤔) na issue
4. Aprovação requer **maioria simples dos maintainers ativos** (>50%)
5. Após aprovação, ADR é mergeado em `docs/adr/NNNN-titulo.md`

### Veto

Qualquer maintainer pode vetar uma decisão alegando:
- Conflito com Code of Conduct
- Risco legal/ético sério
- Quebra de princípios do PRODUCT_FOUNDATION

Veto requer justificativa pública na issue. Pode ser overridden por **2/3 dos maintainers ativos**.

---

## 🚪 Como se tornar maintainer

### Critérios

Não há fórmula rígida, mas geralmente buscamos:

- **Contribuições consistentes** ao longo de pelo menos 2-3 meses
- **Qualidade técnica** demonstrada em PRs (não apenas quantidade)
- **Bom convivente** — feedback respeitoso, paciência com novatos
- **Alinhamento** com princípios do projeto (rastreabilidade, open data, civic tech)

### Processo

1. Maintainer existente nomeia candidato (pode ser self-nomination)
2. Maintainers discutem em privado (Discussions privadas ou async)
3. Consenso simples → nova maintainer adicionada à equipe
4. Anúncio público

---

## 🚫 Removendo um maintainer

Razões aceitáveis:
- Inatividade por > 12 meses sem aviso
- Violação grave do Code of Conduct
- Quebra de confiança da comunidade

Processo:
1. Maintainer levanta a questão privadamente
2. Discussão entre maintainers ativos
3. Votação majoritária (>50% dos demais ativos)
4. Decisão comunicada publicamente

---

## 💰 Financiamento

CivicRadar é gratuito e sem fins lucrativos. Se eventualmente receber doações via [GitHub Sponsors](https://github.com/sponsors) ou similar:

- Uso transparente, com relatório público trimestral
- Prioridade: hospedagem, domínio, ferramentas de scan/análise
- Nunca usado para pagamento direto a maintainers (a menos que ratificado por toda comunidade em decisão pública)

---

## 📄 Licença e CLA

Por enquanto, **não exigimos CLA** (Contributor License Agreement). Contribuições são automaticamente licenciadas sob a AGPL-3.0 ao serem mergeadas.

Caso futuramente haja necessidade (ex: dual-license para empresas), a mudança requer ADR aprovado.

---

## 🤝 Disputas

Conflitos entre contribuidores ou entre contribuidor e maintainer:

1. **Tente resolver diretamente**, com respeito
2. Se não resolver: mencione **2 maintainers** em comentário privado/email para mediar
3. Se ainda não resolver: traga para reunião async de maintainers
4. Decisão final dos maintainers é definitiva, com base no Code of Conduct

---

## 📅 Reuniões

Sem reuniões síncronas obrigatórias. Toda comunicação async via:

- **GitHub Issues** — tarefas concretas
- **GitHub Discussions** — ideias, perguntas abertas
- **PR reviews** — discussão técnica de código

Se a comunidade crescer, podemos adicionar:
- Office hours mensais (opcional)
- Reunião de planejamento trimestral

---

## 🔄 Atualizando este documento

Mudanças neste documento requerem:
- PR com proposta
- Discussão de **mínimo 14 dias**
- Aprovação de **maioria absoluta** dos maintainers ativos (>50%)
