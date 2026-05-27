# Security Policy

## 🛡️ Supported versions

While CivicRadar is in MVP/pre-1.0, only the latest `main` receives security updates.

| Version | Supported |
|---|:---:|
| `main` (latest) | ✅ |
| Pre-releases | ❌ |

---

## 🚨 Reporting a vulnerability

**Do not open public issues for security vulnerabilities.**

Use one of the private channels below, in order of preference:

### 1. GitHub Security Advisory (preferred)

Use the [**Report a vulnerability**](https://github.com/merlinfachetti/civic-radar/security/advisories/new) link in the repository's Security tab. This creates a private advisory only maintainers can see.

### 2. Direct email

Send to **security@civic-radar.dev** (placeholder; the real channel will be published soon). Use PGP if you prefer (public key will be published).

### 3. Last resort

If none of the above work, open a **minimal and vague** issue ("found a vulnerability, how do I report?") and a maintainer will reach out via a secure channel.

---

## 📋 What to include in the report

To help us investigate quickly, please include:

- **Clear description** of the vulnerability
- **Steps to reproduce** (ideally a minimal PoC)
- **Impact** (what could an attacker do?)
- **Affected version** (commit SHA preferred)
- **Environment** (Python/Node versions, OS, relevant configs)
- **Suggested mitigation**, if any

---

## ⏱️ Our commitment

- **Acknowledgement** within **72 hours**
- **Initial assessment** within **7 days**
- **Fix plan** within **14 days** for confirmed vulnerabilities
- **Coordinated public disclosure** after the patch is released

---

## 🏆 Responsible disclosure

We are grateful to researchers who report responsibly. We commit to:

- Keep you informed throughout the process
- Credit you in the advisory (unless you prefer to remain anonymous)
- List you in `SECURITY_HALL_OF_FAME.md` (coming soon)

---

## 🔒 Project security practices

- **Dependabot** active — weekly scan of vulnerable dependencies
- **CodeQL** — automatic static analysis
- **Secret scanning** — GitHub Advanced Security + gitleaks in pre-commit
- **No PII storage** — match profiles are request-scoped, not persisted
- **HTTPS only** in production
- **Rate limiting** on the API
- **Security headers** (HSTS, CSP, X-Frame-Options, etc.)

---

## 🚫 Out of scope

These are **not** considered vulnerabilities for the purposes of this program:

- Issues requiring MITM on an attacker-controlled insecure network
- Self-XSS without amplification
- Missing rate limits on non-critical endpoints (report anyway)
- Old/unofficial forks
- Vulnerabilities in dependencies already flagged by Dependabot

---

## 🤝 Coordinated disclosure

For vulnerabilities in critical dependencies, we will coordinate disclosure with:
- Maintainers of the affected dependency
- The reporting researcher
- CERT.br or similar bodies where applicable

---

Thanks for helping keep CivicRadar safe for everyone. 🛡️
