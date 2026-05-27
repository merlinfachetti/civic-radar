# Security Policy

## 🛡️ Versões suportadas

Como o CivicRadar está em fase MVP/pre-1.0, apenas a versão mais recente da `main` recebe atualizações de segurança.

| Version | Supported |
|---|:---:|
| `main` (latest) | ✅ |
| Pre-releases | ❌ |

---

## 🚨 Reportando uma vulnerabilidade

**Não abra issues públicas para vulnerabilidades de segurança.**

Use um dos canais privados abaixo, em ordem de preferência:

### 1. GitHub Security Advisory (preferido)

Use o link [**Report a vulnerability**](https://github.com/merlinfachetti/civic-radar/security/advisories/new) na aba Security do repositório. Isso cria um advisory privado que apenas maintainers podem ver.

### 2. Email direto

Envie para **security@civic-radar.dev** (placeholder; canal real será adicionado em breve). Use PGP se desejar (chave pública será publicada).

### 3. Em último caso

Se nenhuma das opções acima funcionar, abra um issue **mínimo e vago** ("encontrei uma vulnerabilidade, como reporto?") e um maintainer responderá com canal seguro.

---

## 📋 O que incluir no report

Para ajudar a investigar rapidamente, inclua:

- **Descrição clara** da vulnerabilidade
- **Steps to reproduce** (idealmente um PoC mínimo)
- **Impacto** (o que um atacante poderia fazer?)
- **Versão afetada** (commit SHA preferencialmente)
- **Ambiente** (versão Python/Node, OS, configs relevantes)
- **Sugestão de mitigação**, se tiver

---

## ⏱️ Nosso compromisso

- **Acknowledgement** em até **72 horas**
- **Avaliação inicial** em até **7 dias**
- **Plano de fix** em até **14 dias** para vulnerabilidades confirmadas
- **Disclosure pública coordenada** após patch released

---

## 🏆 Responsible Disclosure

Agradecemos pesquisadores que reportam responsavelmente. Pretendemos:

- Manter você informado durante o processo
- Creditar você no advisory (a menos que prefira anonimato)
- Listar em `SECURITY_HALL_OF_FAME.md` (em breve)

---

## 🔒 Práticas de segurança do projeto

- **Dependabot** ativo — semanal scan de dependências vulneráveis
- **CodeQL** — análise estática automática
- **Secrets scanning** — GitHub Advanced Security + gitleaks no pre-commit
- **No PII storage** — perfis de match são request-scoped, não persistem
- **HTTPS only** em produção
- **Rate limiting** na API
- **Headers de segurança** (HSTS, CSP, X-Frame-Options, etc)

---

## 🚫 Fora do escopo

Estes **não** são considerados vulnerabilidades para fins deste programa:

- Issues que requerem MITM em rede insegura controlada pelo atacante
- Self-XSS sem amplificação
- Falta de rate limiting em endpoints não críticos (mas avise mesmo assim)
- Versões antigas/forks não oficiais
- Vulnerabilidades em dependências já reportadas pelo Dependabot

---

## 🤝 Coordinated Disclosure

Para vulnerabilidades em dependências críticas, vamos coordenar disclosure com:
- Maintainers da dependência afetada
- Pesquisador
- Eventualmente CERT.br ou similar se aplicável

---

Obrigado por ajudar a manter o CivicRadar seguro para todos. 🛡️
