"use client";

import Link from "next/link";
import { ArrowUpRight, Building2, Calendar, MapPin, Users } from "lucide-react";
import { motion } from "framer-motion";

import type { Opportunity } from "@/lib/types";
import { daysUntil, formatDateBR, formatSalaryRange } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { SourceConfidenceBadge } from "@/components/source-confidence-badge";

interface OpportunityCardProps {
  opportunity: Opportunity;
  matchScore?: number;
}

export function OpportunityCard({ opportunity, matchScore }: OpportunityCardProps): JSX.Element {
  const days = daysUntil(opportunity.registration_end_date);
  const deadlineLabel = (() => {
    if (days == null) return null;
    if (days < 0) return { label: "Encerrado", tone: "destructive" as const };
    if (days === 0) return { label: "Encerra hoje", tone: "destructive" as const };
    if (days <= 3) return { label: `Encerra em ${days} dia(s)`, tone: "warning" as const };
    if (days <= 14) return { label: `Encerra em ${days} dias`, tone: "warning" as const };
    return { label: `${days} dias para inscrever`, tone: "secondary" as const };
  })();

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -2 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
    >
      <Card className="group relative flex flex-col gap-3 p-5 transition-shadow hover:shadow-[0_0_28px_-12px_var(--color-radar-glow)] sm:p-6">
        <div className="flex items-start justify-between gap-3">
          <div className="flex-1 space-y-1">
            <h3 className="text-base leading-snug font-semibold tracking-tight sm:text-lg">
              <Link
                href={`/opportunities/${opportunity.id}`}
                className="rounded hover:text-[var(--color-primary)] focus-visible:ring-2 focus-visible:ring-[var(--color-ring)] focus-visible:outline-none"
              >
                {opportunity.title}
                <ArrowUpRight className="ml-1 inline size-4 -translate-y-0.5 opacity-0 transition group-hover:opacity-100" />
              </Link>
            </h3>
            <p className="flex items-center gap-1.5 text-sm text-[var(--color-muted-foreground)]">
              <Building2 className="size-3.5" aria-hidden />
              {opportunity.organization}
            </p>
          </div>
          {matchScore != null && (
            <div className="shrink-0">
              <span className="font-mono text-2xl font-bold text-[var(--color-primary)] tabular-nums">
                {matchScore}
              </span>
              <span className="text-xs text-[var(--color-muted-foreground)]">%</span>
            </div>
          )}
        </div>

        <div className="grid grid-cols-1 gap-2 text-sm sm:grid-cols-2">
          {opportunity.salary_max != null && (
            <p className="font-mono tabular-nums">
              <span className="text-[var(--color-muted-foreground)]">Salário · </span>
              {formatSalaryRange(opportunity.salary_min, opportunity.salary_max)}
            </p>
          )}
          {(opportunity.city || opportunity.state) && (
            <p className="flex items-center gap-1.5 text-[var(--color-muted-foreground)]">
              <MapPin className="size-3.5" aria-hidden />
              {[opportunity.city, opportunity.state].filter(Boolean).join("/")}
            </p>
          )}
          {opportunity.vacancies != null && (
            <p className="flex items-center gap-1.5 text-[var(--color-muted-foreground)]">
              <Users className="size-3.5" aria-hidden />
              {opportunity.vacancies} vaga{opportunity.vacancies === 1 ? "" : "s"}
            </p>
          )}
          {opportunity.registration_end_date && (
            <p className="flex items-center gap-1.5 text-[var(--color-muted-foreground)]">
              <Calendar className="size-3.5" aria-hidden />
              Até {formatDateBR(opportunity.registration_end_date)}
            </p>
          )}
        </div>

        <div className="mt-1 flex flex-wrap items-center gap-2">
          {opportunity.area && <Badge variant="secondary">{opportunity.area}</Badge>}
          {opportunity.board && (
            <Badge variant="outline" className="font-mono text-xs">
              {opportunity.board}
            </Badge>
          )}
          {deadlineLabel && (
            <Badge
              variant={
                deadlineLabel.tone === "destructive"
                  ? "destructive"
                  : deadlineLabel.tone === "warning"
                    ? "warning"
                    : "secondary"
              }
            >
              {deadlineLabel.label}
            </Badge>
          )}
          <SourceConfidenceBadge level={opportunity.confidence_level} className="ml-auto" />
        </div>
      </Card>
    </motion.div>
  );
}
