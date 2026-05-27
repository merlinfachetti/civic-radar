import { Database, ExternalLink } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { SourceConfidenceBadge } from "@/components/source-confidence-badge";
import { api } from "@/lib/api-client";
import type { SourceItem } from "@/lib/types";

const TYPE_LABEL: Record<string, string> = {
  organizing_board: "Banca organizadora",
  agency: "Órgão público",
  portal: "Portal institucional",
  aggregator: "Agregador",
};

export const dynamic = "force-dynamic";

export default async function SourcesPage(): Promise<JSX.Element> {
  let sources: SourceItem[] = [];
  try {
    sources = (await api.listSources()).items;
  } catch {
    sources = [];
  }

  return (
    <div className="mx-auto max-w-5xl px-4 py-10 sm:px-6 lg:px-8">
      <header className="mb-8">
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Fontes monitoradas</h1>
        <p className="mt-2 max-w-2xl text-[var(--color-muted-foreground)]">
          Cada oportunidade no CivicRadar vem com link para a fonte original. Esta página lista
          quais sites são monitorados ativamente, com nível de confiança e estado de saúde.
        </p>
      </header>

      {sources.length === 0 ? (
        <p className="text-[var(--color-muted-foreground)]">
          Não foi possível carregar as fontes agora.
        </p>
      ) : (
        <div className="grid gap-4 md:grid-cols-2">
          {sources.map((source) => (
            <Card key={source.source_id} className="p-6">
              <div className="flex items-start justify-between gap-3">
                <div>
                  <h2 className="text-lg font-semibold tracking-tight">{source.name}</h2>
                  <p className="font-mono text-xs text-[var(--color-muted-foreground)]">
                    {source.source_id}
                  </p>
                </div>
                <SourceConfidenceBadge level={source.quality_level} />
              </div>

              <p className="mt-3 text-sm text-[var(--color-muted-foreground)]">
                {TYPE_LABEL[source.type] ?? source.type}
              </p>

              <div className="mt-4 flex flex-wrap items-center gap-3 text-sm">
                <Badge variant="secondary">
                  <Database className="mr-1 size-3" aria-hidden />
                  {source.items_count} item{source.items_count === 1 ? "" : "s"}
                </Badge>
                {source.enabled ? (
                  <Badge variant="success">ativa</Badge>
                ) : (
                  <Badge variant="destructive">desativada</Badge>
                )}
                {source.last_successful_check_at && (
                  <span className="font-mono text-xs text-[var(--color-muted-foreground)]">
                    Última checagem:{" "}
                    {new Date(source.last_successful_check_at).toLocaleString("pt-BR")}
                  </span>
                )}
              </div>

              <a
                href={source.base_url}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-4 inline-flex items-center gap-1 text-sm text-[var(--color-primary)] hover:underline"
              >
                {new URL(source.base_url).hostname}
                <ExternalLink className="size-3" aria-hidden />
              </a>
            </Card>
          ))}
        </div>
      )}

      <Card className="mt-8 border-dashed p-6">
        <h2 className="text-lg font-semibold">Falta uma fonte importante?</h2>
        <p className="mt-2 text-sm text-[var(--color-muted-foreground)]">
          Abra uma issue com o template <span className="font-mono">📡 Add new source</span> no
          GitHub. Adicionar uma fonte nova é frequentemente uma{" "}
          <span className="font-mono">good first issue</span>.
        </p>
      </Card>
    </div>
  );
}
