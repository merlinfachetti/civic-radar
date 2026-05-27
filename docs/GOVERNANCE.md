# Governance

> How decisions are made on CivicRadar, and how to become a maintainer.

---

## 🎯 Philosophy

CivicRadar is a **community-driven** project with low formal overhead. The goal is to keep contributions easy and decisions transparent, without unnecessary bureaucracy.

---

## 👥 Roles

### Contributors

Anyone opening an issue, a PR or participating in discussions. **All** contributions are valued.

### Maintainers

People with merge permission on `main`. Responsibilities:

- Review and merge PRs
- Triage issues
- Maintain quality and direction of the project
- Enforce the Code of Conduct

**Initial maintainers:**

- [@aldenfachetti](https://github.com/aldenfachetti)
- [@merlinfachetti](https://github.com/merlinfachetti)

### Core maintainers _(future)_

Subset of maintainers with additional permissions (admin, secrets, billing). Elected by consensus of current maintainers once the project grows.

---

## 🗳️ Decision-making process

### Lazy consensus (default)

For **most** decisions — code changes, features, bug fixes, refactors:

1. Open a PR or issue describing the change
2. Wait for feedback from maintainers (up to 7 days)
3. If no maintainer objects, it is considered approved
4. At least 1 maintainer performs the merge

**No formal vote is required** for small/medium decisions.

### Architecture Decision Records (ADRs)

Significant architectural decisions require an ADR:

- Stack change (language, framework, DB)
- License change
- Change to product principles
- Breaking change to the DB schema
- Adding a critical dependency

Process:

1. Open an issue labeled `adr-proposal` describing:
   - **Context** — Why is this being considered?
   - **Options** — Which alternatives were evaluated?
   - **Decision** — Proposal
   - **Consequences** — Accepted trade-offs
2. Open discussion for **at least 7 days**
3. Maintainers vote (👍 / 👎 / 🤔) on the issue
4. Approval requires a **simple majority of active maintainers** (>50%)
5. Once approved, the ADR is merged at `docs/adr/NNNN-title.md`

### Veto

Any maintainer can veto a decision citing:
- Conflict with the Code of Conduct
- Serious legal/ethical risk
- Violation of the principles in PRODUCT_FOUNDATION

A veto must include a public justification on the issue. It can be overridden by **2/3 of active maintainers**.

---

## 🚪 Becoming a maintainer

### Criteria

There is no rigid formula, but we generally look for:

- **Consistent contributions** over at least 2–3 months
- **Technical quality** demonstrated in PRs (not just quantity)
- **Good citizenship** — respectful feedback, patience with newcomers
- **Alignment** with the project's principles (traceability, open data, civic tech)

### Process

1. An existing maintainer nominates a candidate (self-nomination allowed)
2. Maintainers discuss privately (private Discussions or async)
3. On simple consensus → the new maintainer is added to the team
4. Public announcement

---

## 🚫 Removing a maintainer

Acceptable reasons:
- Inactivity for >12 months without notice
- Serious violation of the Code of Conduct
- Loss of community trust

Process:
1. A maintainer raises the question privately
2. Discussion among active maintainers
3. Majority vote (>50% of remaining active maintainers)
4. Decision communicated publicly

---

## 💰 Funding

CivicRadar is free and not-for-profit. If donations are ever received via [GitHub Sponsors](https://github.com/sponsors) or similar:

- Transparent use, with a public quarterly report
- Priority: hosting, domain, scanning/analysis tooling
- Never used for direct payments to maintainers (unless ratified by the whole community in a public decision)

---

## 📄 License and CLA

For now we **do not require a CLA** (Contributor License Agreement). Contributions are automatically licensed under AGPL-3.0 when merged.

If a future need arises (e.g. dual-licensing for enterprises), the change requires an approved ADR.

---

## 🤝 Disputes

Conflicts between contributors or between contributor and maintainer:

1. **Try to resolve directly**, respectfully
2. If unresolved: mention **2 maintainers** in a private comment/email to mediate
3. If still unresolved: bring it to an async maintainers meeting
4. The maintainers' final decision is binding, grounded on the Code of Conduct

---

## 📅 Meetings

No mandatory synchronous meetings. All communication is async via:

- **GitHub Issues** — concrete tasks
- **GitHub Discussions** — ideas, open questions
- **PR reviews** — technical discussion of code

If the community grows, we may add:
- Monthly office hours (optional)
- Quarterly planning meeting

---

## 🔄 Updating this document

Changes to this document require:
- A PR with the proposal
- A discussion of **at least 14 days**
- Approval by an **absolute majority** of active maintainers (>50%)
