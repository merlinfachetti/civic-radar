import Link from "next/link";
import { notFound } from "next/navigation";
import { Building2, Calendar, ExternalLink, GraduationCap, MapPin, Users } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { SourceConfidenceBadge } from "@/components/source-confidence-badge";
import { ApiError, api } from "@/lib/api-client";
import { daysUntil, formatDateBR, formatSalaryRange } from "@/lib/utils";

interface PageProps {
  params: Promise<{ id: string }>;
}

export const dynamic = "force-dynamic";

export default async function OpportunityDetailPage({ params }: PageProps): Promise<JSX.Element> {
  const { id } = await params;

  let opportunity;
  try {
    opportunity = await api.getOpportunity(id);
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) notFound();
    throw error;
  }

  const days = daysUntil(opportunity.registration_end_date);
  const deadlineLabel = (() => {
    if (days == null) return null;
    if (days < 0) return { label: "Inscrições encerradas", tone: "destructive" as const };
    if (days === 0) return { label: "Encerra hoje", tone: "destructive" as const };
    if (days <= 7) return { label: `Encerra em ${days} dias`, tone: "warning" as const };
    return { label: `${days} dias restantes`, tone: "secondary" as const };
  })();

  return (
    <div className="mx-auto max-w-4xl px-4 py-10 sm:px-6 lg:px-8">
      <Link
        href="/opportunities"
        className="mb-6 inline-block text-sm text-[var(--color-muted-foreground)] hover:text-[var(--color-foreground)]"
      >
        ← voltar
      </Link>

      <header className="space-y-3">
        <div className="flex flex-wrap items-center gap-2">
          {opportunity.area && <Badge variant="secondary">{opportunity.area}</Badge>}
          {opportunity.board && (
            <Badge variant="outline" className="font-mono">
              {opportunity.board}
            </Badge>
          )}
          {deadlineLabel && (
            <Badge variant={deadlineLabel.tone === "destructive" ? "destructive" : "warning"}>
              {deadlineLabel.label}
            </Badge>
          )}
          <SourceConfidenceBadge level={opportunity.confidence_level} />
        </div>
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">{opportunity.title}</h1>
        <p className="text-[var(--color-muted-foreground)]">{opportunity.organization}</p>
      </header>

      <div className="my-8 grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <Stat icon={<MapPin className="size-4" aria-hidden />} label="Localização">
          {[opportunity.city, opportunity.state].filter(Boolean).join("/") || "—"}
        </Stat>
        <Stat icon={<GraduationCap className="size-4" aria-hidden />} label="Escolaridade">
          {opportunity.education_level ?? "—"}
        </Stat>
        <Stat icon={<Users className="size-4" aria-hidden />} label="Vagas">
          {opportunity.vacancies ?? "—"}
        </Stat>
        <Stat icon={<Calendar className="size-4" aria-hidden />} label="Encerra">
          {formatDateBR(opportunity.registration_end_date)}
        </Stat>
      </div>

      <Card className="p-6">
        <h2 className="mb-2 text-sm font-medium text-[var(--color-muted-foreground)]">
          Remuneração
        </h2>
        <p className="font-mono text-xl tabular-nums">
          {formatSalaryRange(opportunity.salary_min, opportunity.salary_max)}
        </p>
      </Card>

      {opportunity.description && (
        <Card className="mt-6 p-6">
          <h2 className="mb-3 text-sm font-medium text-[var(--color-muted-foreground)]">Resumo</h2>
          <p className="text-sm leading-relaxed whitespace-pre-line">{opportunity.description}</p>
        </Card>
      )}

      {opportunity.keywords && opportunity.keywords.length > 0 && (
        <div className="mt-6">
          <h2 className="mb-2 text-sm font-medium text-[var(--color-muted-foreground)]">
            Palavras-chave
          </h2>
          <div className="flex flex-wrap gap-2">
            {opportunity.keywords.map((kw) => (
              <Badge key={kw} variant="outline" className="font-mono text-xs">
                {kw}
              </Badge>
            ))}
          </div>
        </div>
      )}

      <Card className="mt-6 p-6">
        <h2 className="mb-2 text-sm font-medium text-[var(--color-muted-foreground)]">
          Fonte original
        </h2>
        <p className="mb-4 text-sm text-[var(--color-muted-foreground)]">
          CivicRadar não substitui fonte oficial. Confirme inscrição, prazos e requisitos
          diretamente no link abaixo.
        </p>
        <div className="flex flex-col gap-2 sm:flex-row">
          <Button asChild>
            <a href={opportunity.source_url} target="_blank" rel="noopener noreferrer">
              <Building2 className="size-4" aria-hidden />
              Fonte ({opportunity.board ?? "banca"}) <ExternalLink className="size-4" aria-hidden />
            </a>
          </Button>
          {opportunity.original_url && (
            <Button asChild variant="outline">
              <a href={opportunity.original_url} target="_blank" rel="noopener noreferrer">
                Página do órgão <ExternalLink className="size-4" aria-hidden />
              </a>
            </Button>
          )}
        </div>
        <p className="mt-4 font-mono text-xs text-[var(--color-muted-foreground)]">
          Última verificação: {new Date(opportunity.last_checked_at).toLocaleString("pt-BR")}
        </p>
      </Card>
    </div>
  );
}

function Stat({
  icon,
  label,
  children,
}: {
  icon: JSX.Element;
  label: string;
  children: React.ReactNode;
}): JSX.Element {
  return (
    <div className="rounded-md border border-[var(--color-border)] bg-[var(--color-card)] p-4">
      <div className="flex items-center gap-2 text-xs text-[var(--color-muted-foreground)]">
        {icon}
        {label}
      </div>
      <div className="mt-1 font-medium">{children}</div>
    </div>
  );
}
