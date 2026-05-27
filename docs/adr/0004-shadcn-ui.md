# ADR 0004 — Frontend UI: shadcn/ui + Tailwind v4 + Framer Motion

**Status:** Accepted
**Date:** 2026-05-27
**Deciders:** Initial maintainers

## Context

Precisamos escolher abordagem para UI do frontend Next.js. Objetivos:

- Visual **moderno e tech-forward**, longe da estética burocrática de ferramentas governamentais
- Componentes **acessíveis por default** (WCAG AA)
- **Customização total** sem brigar com framework
- Velocidade de desenvolvimento
- Dark mode bem-feito
- Manutenibilidade a longo prazo em projeto open source

## Options Considered

| Option | Pros | Cons |
|---|---|---|
| **shadcn/ui + Tailwind v4 + Framer Motion** | Componentes _owned_ (copiados, não dependência), Radix UI a11y, Tailwind v4 moderno, customização total | Setup inicial leva tempo, requer conhecer Tailwind |
| Mantine v7 | Componentes ricos prontos (DatePicker, etc), boa a11y | Acoplamento forte, customização mais limitada |
| Chakra UI v3 | API agradável | Bundle maior, ecossistema menor que shadcn |
| Material UI | Maduro, completo | Visual "Google" forte, customização cara |
| Tailwind sem libs | Máxima liberdade | Tudo do zero, a11y por nossa conta |
| Radix + custom CSS | Acessível, leve | Tailwind + radix = quase shadcn |

## Decision

**shadcn/ui + Tailwind CSS v4 + Framer Motion**, com `next-themes` para dark/light.

### Stack visual completa

| Camada | Escolha |
|---|---|
| Componentes base | shadcn/ui (Radix UI + Tailwind classes) |
| Utility CSS | Tailwind CSS v4 |
| Animações | Framer Motion |
| Theme | next-themes (default: dark) |
| Icons | lucide-react |
| Toasts | sonner |
| Command Palette | cmdk |
| Fonts | Geist Sans (UI) + JetBrains Mono (code/numbers) |
| State server | TanStack Query (React Query) |
| State client | Zustand (apenas se necessário; preferir React state) |
| Forms | React Hook Form + Zod |

## Rationale

### "You own the code" — vantagem decisiva

shadcn/ui não é uma dependência npm; é um **gerador** que copia componentes Radix+Tailwind para `src/components/ui/`. Vantagens:

- **Sem breaking changes silenciosos** — Atualizações são opt-in via comando
- **Customização sem fork** — É seu código
- **Tree-shaking perfeito** — Apenas o que você usa
- **A11y de Radix** — Foco visível, teclado, ARIA, tudo gratuito

### Tailwind v4

v4 é totalmente baseada em CSS (`@theme`, variáveis CSS nativas), com config simplificado e performance superior. Padrão 2025-2026.

### Framer Motion

Permite micro-animações que dão "alma" ao produto — layout transitions, stagger lists, gestures — sem reinventar.

## Consequences

### Positivas

- Componentes que **parecem caros** sem custo de manutenção de framework
- Acessibilidade por padrão (Radix)
- Dark mode primeira classe
- Setup conhecido por muitos devs contribuidores

### Negativas / Trade-offs

- **Mais código no repo** — componentes em vez de imports de lib
  - **Mitigação:** Aceito — preferimos isso a vendor lock-in
- **Curva inicial** — Devs precisam conhecer Tailwind
  - **Mitigação:** Documentação interna em `docs/CONTRIBUTING.md`
- **shadcn não tem todos componentes** (ex: DatePicker rico)
  - **Mitigação:** Usar Radix primitives + Tailwind quando necessário; ou react-day-picker

### Action Items

- `pnpm dlx shadcn@latest init` para setup inicial
- Configurar theme tokens em `app/globals.css` (Tailwind v4 syntax)
- Componentes base: Button, Card, Input, Select, Sheet, Dialog, Badge, Skeleton, Toast
- Componentes customizados em `components/` (não em `components/ui/`)
- Fonts via `next/font/local` ou Google
- Documentar pattern em `docs/CONTRIBUTING.md`
