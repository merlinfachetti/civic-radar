# ADR 0004 — Frontend UI: shadcn/ui + Tailwind v4 + Framer Motion

**Status:** Accepted
**Date:** 2026-05-27
**Deciders:** Initial maintainers

## Context

We need to pick a UI approach for the Next.js frontend. Goals:

- A **modern, tech-forward** look, far from the bureaucratic style of Brazilian government tools
- **Accessible-by-default** components (WCAG AA)
- **Full customization** without fighting the framework
- Fast development pace
- Solid dark mode
- Long-term maintainability for an open source project

## Options considered

| Option | Pros | Cons |
|---|---|---|
| **shadcn/ui + Tailwind v4 + Framer Motion** | _Owned_ components (copied, not a dependency), Radix UI a11y, modern Tailwind v4, total customization | Some upfront setup, requires Tailwind familiarity |
| Mantine v7 | Rich ready-to-use components (DatePicker, etc.), good a11y | Strong coupling, more limited customization |
| Chakra UI v3 | Pleasant API | Larger bundle, smaller ecosystem than shadcn |
| Material UI | Mature, complete | Strong "Google" look, expensive to restyle |
| Tailwind without libs | Maximum freedom | Everything from scratch, a11y on us |
| Radix + custom CSS | Accessible, lightweight | Tailwind + Radix essentially = shadcn |

## Decision

**shadcn/ui + Tailwind CSS v4 + Framer Motion**, with `next-themes` for dark/light.

### Visual stack in full

| Layer | Pick |
|---|---|
| Base components | shadcn/ui (Radix UI + Tailwind classes) |
| Utility CSS | Tailwind CSS v4 |
| Animations | Framer Motion |
| Theme | next-themes (default: dark) |
| Icons | lucide-react |
| Toasts | sonner |
| Command Palette | cmdk |
| Fonts | Geist Sans (UI) + JetBrains Mono (code/numbers) |
| Server state | TanStack Query (React Query) |
| Client state | Zustand (only if needed; prefer React state) |
| Forms | React Hook Form + Zod |

## Rationale

### "You own the code" — the decisive win

shadcn/ui is not an npm dependency; it is a **generator** that copies Radix+Tailwind components into `src/components/ui/`. Benefits:

- **No silent breaking changes** — Updates are opt-in via command
- **Customization without a fork** — It is your code
- **Perfect tree-shaking** — Only what you use
- **Radix a11y** — Focus visible, keyboard support, ARIA — all for free

### Tailwind v4

v4 is fully CSS-based (`@theme`, native CSS variables), with simpler config and better performance. It is the 2025–2026 default.

### Framer Motion

Enables micro-animations that give the product life — layout transitions, staggered lists, gestures — without reinventing the wheel.

## Consequences

### Positive

- Components that **look expensive** without the maintenance cost of a framework
- Accessibility by default (Radix)
- First-class dark mode
- Setup familiar to many contributors

### Negative / trade-offs

- **More code in the repo** — components live with us instead of being lib imports
  - **Mitigation:** Accepted — preferable to vendor lock-in
- **Initial curve** — Devs need to know Tailwind
  - **Mitigation:** Internal docs in `docs/CONTRIBUTING.md`
- **shadcn does not ship everything** (e.g. rich DatePicker)
  - **Mitigation:** Use Radix primitives + Tailwind when needed; or react-day-picker

### Action items

- `pnpm dlx shadcn@latest init` for initial setup
- Configure theme tokens in `app/globals.css` (Tailwind v4 syntax)
- Base components: Button, Card, Input, Select, Sheet, Dialog, Badge, Skeleton, Toast
- Custom components in `components/` (not `components/ui/`)
- Fonts via `next/font/local` or Google
- Document the pattern in `docs/CONTRIBUTING.md`
