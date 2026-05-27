# ADR 0003 — License: AGPL-3.0

**Status:** Accepted
**Date:** 2026-05-27
**Deciders:** Initial maintainers

## Context

We need to choose an open source license that:

- Keeps the project **open in practice** (not only in name)
- Prevents a closed competitor from forking the code, hosting it as SaaS and never giving back
- Allows personal, educational and governmental use without friction
- Is widely recognized (OSI-approved)

## Options considered

| License | Model | Strong copyleft | Network use | Enterprise-friendly |
|---|---|:---:|:---:|:---:|
| **AGPL-3.0** | Copyleft | ✅ | ✅ (requires source) | Medium |
| GPL-3.0 | Copyleft | ✅ | ❌ (SaaS loophole) | Medium |
| MPL-2.0 | Weak copyleft | Partial | ❌ | High |
| Apache-2.0 | Permissive | ❌ | ❌ | Very high |
| MIT | Permissive | ❌ | ❌ | Very high |
| BSL/SSPL | Source-available | ✅ | ✅ | Low (not OSI) |

**Network use clause** = requires that modified code be made available even when the "use" is purely network-based (SaaS).

## Decision

**AGPL-3.0** ([official text](https://www.gnu.org/licenses/agpl-3.0.txt)).

## Rationale

CivicRadar is a **civic-tech tool** that improves access to public information. AGPL-3.0:

1. **Protects the open ecosystem** — Closed SaaS forks are forced to publish their modifications
2. **Encourages contributions back** — Companies that want to use it commercially must contribute
3. **Stays aligned with the mission** — Open data should not become a closed product

## Consequences

### Positive

- SaaS-fork modifications must be open-source
- Community work is not "captured" by companies
- Aligned with the civic-tech / open data philosophy

### Negative / trade-offs

- **Reduced enterprise adoption** — Some companies forbid AGPL by policy. Acceptable: our focus is community, not enterprise.
- **Compatibility with other libs** — AGPL is strong; MIT/Apache libs can coexist, but mixing with GPL/LGPL needs attention.
- **Perceived complexity** — Harder to explain than MIT.

### Action items

- `LICENSE` at the root with the full AGPL-3.0 text
- License headers on critical files? **Not required** — `LICENSE` at the root is enough for AGPL
- `README.md` states the license and links to it
- Consider a CLA with dual-licensing later **only if** necessary (requires a new ADR)

## Re-evaluation

This decision can be revisited if:

- The community asks for it through a majority (open vote)
- A clear need for enterprise adoption shows up (rare for civic-tech)
- A future equivalent or stronger license appears (e.g. AGPL-4 if it ever exists)

Any license change requires a new ADR approved by an absolute majority of maintainers.
