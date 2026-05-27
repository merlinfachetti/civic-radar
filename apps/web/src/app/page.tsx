import Link from "next/link";
import { ArrowRight, Filter, Github, Radar, ShieldCheck, Sparkles, Target } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { api } from "@/lib/api-client";
import type { StatsResponse } from "@/lib/types";

export const revalidate = 60;

async function loadStats(): Promise<StatsResponse | null> {
  try {
    return await api.getStats();
  } catch {
    return null;
  }
}

export default async function HomePage(): Promise<JSX.Element> {
  const stats = await loadStats();

  return (
    <>
      <section className="radar-grid relative isolate overflow-hidden">
        <div className="mx-auto max-w-7xl px-4 py-20 sm:px-6 sm:py-28 lg:px-8 lg:py-32">
          <div className="mx-auto max-w-3xl text-center">
            <div className="mx-auto mb-6 inline-flex items-center gap-2 rounded-full border border-[var(--color-border)] bg-[var(--color-card)]/60 px-3 py-1 font-mono text-xs text-[var(--color-muted-foreground)] backdrop-blur">
              <Radar
                className="size-3 text-[var(--color-primary)]"
                style={{ filter: "drop-shadow(0 0 4px var(--color-radar-glow))" }}
                aria-hidden
              />
              v0.1 · open source civic-tech
            </div>
            <h1 className="text-4xl font-bold tracking-tight text-balance sm:text-5xl lg:text-6xl">
              Radar open source para{" "}
              <span className="bg-gradient-to-r from-[var(--color-primary)] to-[var(--color-foreground)] bg-clip-text text-transparent">
                concursos públicos
              </span>{" "}
              que combinam com você.
            </h1>
            <p className="mt-6 text-base text-pretty text-[var(--color-muted-foreground)] sm:text-lg">
              CivicRadar monitora bancas, órgãos e portais públicos, normaliza as oportunidades e
              calcula um score determinístico — sem caixa preta. Para qualquer pessoa que busca uma
              carreira pública no Brasil.
            </p>
            <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
              <Button asChild size="lg">
                <Link href="/opportunities">
                  Ver oportunidades <ArrowRight className="size-4" aria-hidden />
                </Link>
              </Button>
              <Button asChild variant="outline" size="lg">
                <Link href="/profile-match">
                  <Target className="size-4" aria-hidden />
                  Calcular meu match
                </Link>
              </Button>
            </div>

            {stats && (
              <div className="mx-auto mt-12 grid max-w-2xl grid-cols-2 gap-4 sm:grid-cols-4">
                <Stat label="Oportunidades" value={stats.total_opportunities} />
                <Stat label="Abertas agora" value={stats.open_opportunities} tone="success" />
                <Stat label="Fontes" value={stats.sources.total} />
                <Stat
                  label="Últimos 7 dias"
                  value={stats.last_7_days.new_opportunities}
                  suffix="+"
                />
              </div>
            )}
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">Por que CivicRadar?</h2>
          <p className="mt-4 text-[var(--color-muted-foreground)]">
            Informação pública não deveria ser caça-fragmentada. Construímos um radar que respeita
            fontes oficiais, prioriza rastreabilidade e cabe num{" "}
            <span className="font-mono">docker compose up</span>.
          </p>
        </div>
        <div className="mt-12 grid gap-4 md:grid-cols-3">
          <Feature
            icon={<Filter className="size-5" aria-hidden />}
            title="Filtros poderosos"
            description="Estado, área, escolaridade, faixa salarial, banca, palavra-chave. Combinados em tempo real."
          />
          <Feature
            icon={<Target className="size-5" aria-hidden />}
            title="Match explicável"
            description="Algoritmo determinístico — sem IA opaca. Cada score vem com o motivo do match em texto humano."
          />
          <Feature
            icon={<ShieldCheck className="size-5" aria-hidden />}
            title="Rastreabilidade total"
            description="Cada oportunidade exibe a fonte original, data da última verificação e nível de confiança."
          />
        </div>
      </section>

      <section className="border-t border-[var(--color-border)] bg-[var(--color-card)]/30">
        <div className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8 lg:py-20">
          <div className="mx-auto max-w-3xl text-center">
            <h2 className="text-3xl font-semibold tracking-tight sm:text-4xl">
              Construído como projeto open source.
            </h2>
            <p className="mt-4 text-[var(--color-muted-foreground)]">
              Licença AGPL-3.0. Crawlers em Python (uv + FastAPI), web em Next.js 15 + shadcn/ui.
              Contribua, abra uma issue, ou adicione sua banca/órgão favorito.
            </p>
            <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
              <Button asChild size="lg" variant="default">
                <a
                  href="https://github.com/merlinfachetti/civic-radar"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <Github className="size-4" aria-hidden />
                  GitHub
                </a>
              </Button>
              <Button asChild size="lg" variant="outline">
                <Link href="/contribute">
                  <Sparkles className="size-4" aria-hidden />
                  Como contribuir
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </>
  );
}

function Stat({
  label,
  value,
  suffix,
  tone,
}: {
  label: string;
  value: number;
  suffix?: string;
  tone?: "success";
}): JSX.Element {
  return (
    <div className="rounded-lg border border-[var(--color-border)] bg-[var(--color-card)]/40 px-4 py-3 backdrop-blur">
      <div
        className="font-mono text-2xl font-semibold tabular-nums"
        style={{ color: tone === "success" ? "var(--color-success)" : undefined }}
      >
        {value.toLocaleString("pt-BR")}
        {suffix ?? ""}
      </div>
      <div className="text-xs text-[var(--color-muted-foreground)]">{label}</div>
    </div>
  );
}

function Feature({
  icon,
  title,
  description,
}: {
  icon: JSX.Element;
  title: string;
  description: string;
}): JSX.Element {
  return (
    <Card className="p-6 transition-shadow hover:shadow-[0_0_28px_-12px_var(--color-radar-glow)]">
      <div className="mb-4 inline-flex size-10 items-center justify-center rounded-lg bg-[var(--color-primary)]/10 text-[var(--color-primary)]">
        {icon}
      </div>
      <h3 className="mb-2 text-lg font-semibold tracking-tight">{title}</h3>
      <p className="text-sm text-[var(--color-muted-foreground)]">{description}</p>
    </Card>
  );
}
