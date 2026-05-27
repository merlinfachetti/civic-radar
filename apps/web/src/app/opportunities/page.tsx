import Link from "next/link";
import { ArrowRight, SearchX } from "lucide-react";

import { OpportunityCard } from "@/components/opportunity-card";
import { Button } from "@/components/ui/button";
import { api } from "@/lib/api-client";
import type { OpportunityFilters } from "@/lib/types";

interface PageProps {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}

function pickArray(value: string | string[] | undefined): string[] | undefined {
  if (!value) return undefined;
  return Array.isArray(value) ? value : [value];
}

function pickString(value: string | string[] | undefined): string | undefined {
  if (!value) return undefined;
  return Array.isArray(value) ? value[0] : value;
}

export const dynamic = "force-dynamic";

export default async function OpportunitiesPage({ searchParams }: PageProps): Promise<JSX.Element> {
  const params = await searchParams;
  const filters: OpportunityFilters = {
    q: pickString(params.q),
    state: pickArray(params.state),
    area: pickArray(params.area),
    salary_min: params.salary_min ? Number(pickString(params.salary_min)) : undefined,
    sort: pickString(params.sort) ?? "-registration_end_date",
    limit: 30,
  };

  let data;
  try {
    data = await api.listOpportunities(filters);
  } catch {
    return <ApiUnreachable />;
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
      <div className="mb-8 flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Oportunidades</h1>
          <p className="mt-2 text-[var(--color-muted-foreground)]">
            {data.pagination.total_count} oportunidade{data.pagination.total_count === 1 ? "" : "s"}{" "}
            encontradas
          </p>
        </div>
        <Button asChild variant="outline">
          <Link href="/profile-match">
            Match com meu perfil <ArrowRight className="size-4" aria-hidden />
          </Link>
        </Button>
      </div>

      <ActiveFiltersChips filters={filters} />

      {data.items.length === 0 ? (
        <EmptyState />
      ) : (
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {data.items.map((opportunity) => (
            <OpportunityCard key={opportunity.id} opportunity={opportunity} />
          ))}
        </div>
      )}
    </div>
  );
}

function ActiveFiltersChips({ filters }: { filters: OpportunityFilters }): JSX.Element | null {
  const chips: { label: string; key: string }[] = [];
  filters.state?.forEach((s) => chips.push({ label: `UF: ${s}`, key: `state-${s}` }));
  filters.area?.forEach((a) => chips.push({ label: `Área: ${a}`, key: `area-${a}` }));
  if (filters.salary_min) chips.push({ label: `R$ ${filters.salary_min}+`, key: "salary" });
  if (filters.q) chips.push({ label: `"${filters.q}"`, key: "q" });

  if (chips.length === 0) return null;

  return (
    <div className="mb-6 flex flex-wrap items-center gap-2">
      {chips.map((chip) => (
        <span
          key={chip.key}
          className="inline-flex items-center rounded-full bg-[var(--color-accent)] px-3 py-1 text-xs"
        >
          {chip.label}
        </span>
      ))}
      <Link
        href="/opportunities"
        className="text-xs text-[var(--color-muted-foreground)] underline"
      >
        limpar
      </Link>
    </div>
  );
}

function EmptyState(): JSX.Element {
  return (
    <div className="mx-auto max-w-md py-20 text-center">
      <div className="mx-auto mb-4 inline-flex size-12 items-center justify-center rounded-full bg-[var(--color-muted)] text-[var(--color-muted-foreground)]">
        <SearchX className="size-5" aria-hidden />
      </div>
      <h2 className="text-lg font-semibold">Nada encontrado por aqui (ainda).</h2>
      <p className="mt-2 text-sm text-[var(--color-muted-foreground)]">
        Tente afrouxar os filtros, ou{" "}
        <a
          href="https://github.com/merlinfachetti/civic-radar/issues/new/choose"
          className="text-[var(--color-primary)] underline"
        >
          sugerir uma nova fonte
        </a>{" "}
        para que o radar capture mais.
      </p>
    </div>
  );
}

function ApiUnreachable(): JSX.Element {
  return (
    <div className="mx-auto max-w-md py-20 text-center">
      <h2 className="text-lg font-semibold">Não conseguimos falar com a API agora.</h2>
      <p className="mt-2 text-sm text-[var(--color-muted-foreground)]">
        Verifique se o backend está rodando em <span className="font-mono">localhost:8000</span> ou
        ajuste <span className="font-mono">NEXT_PUBLIC_API_URL</span>.
      </p>
    </div>
  );
}
