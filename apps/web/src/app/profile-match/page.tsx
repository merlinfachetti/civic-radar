"use client";

import { useMutation } from "@tanstack/react-query";
import { useState } from "react";
import { Sparkles } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { MatchScoreVisual } from "@/components/match-score-visual";
import { OpportunityCard } from "@/components/opportunity-card";
import { api } from "@/lib/api-client";
import type { MatchProfile } from "@/lib/types";

const EMPTY_PROFILE: MatchProfile = {
  areas: [],
  states: [],
  cities: [],
  education_level: null,
  minimum_salary: null,
  keywords: [],
  include_remote: false,
};

function parseCsv(input: string): string[] {
  return input
    .split(",")
    .map((s) => s.trim())
    .filter(Boolean);
}

export default function ProfileMatchPage(): JSX.Element {
  const [areas, setAreas] = useState("tecnologia");
  const [states, setStates] = useState("SP, RJ, DF");
  const [keywords, setKeywords] = useState("analista, sistemas");
  const [salary, setSalary] = useState("6000");
  const [education, setEducation] = useState("superior");

  const mutation = useMutation({
    mutationFn: async () => {
      const profile: MatchProfile = {
        ...EMPTY_PROFILE,
        areas: parseCsv(areas),
        states: parseCsv(states),
        keywords: parseCsv(keywords),
        minimum_salary: salary ? Number(salary) : null,
        education_level: education ? (education as MatchProfile["education_level"]) : null,
      };
      return api.match(profile, 30);
    },
  });

  return (
    <div className="mx-auto max-w-6xl px-4 py-10 sm:px-6 lg:px-8">
      <header className="mb-8">
        <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Match com seu perfil</h1>
        <p className="mt-2 max-w-2xl text-[var(--color-muted-foreground)]">
          Score determinístico com peso por critério. Seu perfil nunca é salvo — cada cálculo é
          stateless.
        </p>
      </header>

      <div className="grid gap-6 lg:grid-cols-[400px_1fr]">
        <Card className="lg:sticky lg:top-20 lg:self-start">
          <CardHeader>
            <CardTitle>Seu perfil</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Field
              label="Áreas (separadas por vírgula)"
              hint="ex: tecnologia, juridica"
              value={areas}
              onChange={setAreas}
            />
            <Field
              label="Estados (UF separados por vírgula)"
              hint="ex: SP, RJ, PR"
              value={states}
              onChange={setStates}
            />
            <Field
              label="Palavras-chave"
              hint="ex: analista, desenvolvedor"
              value={keywords}
              onChange={setKeywords}
            />
            <Field
              label="Salário mínimo (R$)"
              hint="número inteiro"
              type="number"
              value={salary}
              onChange={setSalary}
            />
            <div>
              <label className="mb-1.5 block text-sm font-medium">Escolaridade</label>
              <select
                className="flex h-10 w-full rounded-md border border-[var(--color-input)] bg-transparent px-3 text-sm"
                value={education}
                onChange={(e) => setEducation(e.target.value)}
              >
                <option value="">qualquer</option>
                <option value="fundamental">Fundamental</option>
                <option value="medio">Médio</option>
                <option value="tecnico">Técnico</option>
                <option value="superior">Superior</option>
                <option value="pos_graduacao">Pós-graduação</option>
              </select>
            </div>

            <Button
              className="w-full"
              onClick={() => mutation.mutate()}
              disabled={mutation.isPending}
            >
              <Sparkles className="size-4" aria-hidden />
              {mutation.isPending ? "Calculando..." : "Calcular match"}
            </Button>
          </CardContent>
        </Card>

        <div>
          {mutation.isPending && (
            <p className="text-sm text-[var(--color-muted-foreground)]">Calculando...</p>
          )}
          {mutation.isError && (
            <p className="text-sm text-[var(--color-destructive)]">
              Erro ao calcular match: {(mutation.error as Error).message}
            </p>
          )}
          {mutation.data && mutation.data.matches.length === 0 && (
            <p className="text-sm text-[var(--color-muted-foreground)]">
              Nenhuma oportunidade aberta no momento. Tente outros critérios.
            </p>
          )}
          {mutation.data && (
            <div className="space-y-4">
              <p className="text-sm text-[var(--color-muted-foreground)]">
                {mutation.data.total_returned} de {mutation.data.total_evaluated} oportunidades
                ordenadas por compatibilidade.
              </p>
              {mutation.data.matches.map((m) => (
                <Card key={m.opportunity_id} className="p-5 sm:p-6">
                  <div className="flex items-start gap-4">
                    <MatchScoreVisual score={m.score} size={72} />
                    <div className="min-w-0 flex-1">
                      <OpportunityCard opportunity={m.opportunity} matchScore={m.score} />
                    </div>
                  </div>
                  <details className="mt-3 text-sm">
                    <summary className="cursor-pointer text-[var(--color-muted-foreground)] hover:text-[var(--color-foreground)]">
                      Por que esse score?
                    </summary>
                    <ul className="mt-2 space-y-1">
                      {m.reasons.map((r) => (
                        <li
                          key={r.criterion}
                          className="flex items-center justify-between gap-2 font-mono text-xs"
                        >
                          <span className="text-[var(--color-muted-foreground)]">
                            {r.explanation}
                          </span>
                          <span className="shrink-0 tabular-nums">
                            {r.points}/{r.weight}
                          </span>
                        </li>
                      ))}
                    </ul>
                  </details>
                </Card>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

function Field({
  label,
  hint,
  value,
  onChange,
  type = "text",
}: {
  label: string;
  hint?: string;
  value: string;
  onChange: (v: string) => void;
  type?: string;
}): JSX.Element {
  return (
    <div>
      <label className="mb-1.5 block text-sm font-medium">{label}</label>
      <Input type={type} value={value} onChange={(e) => onChange(e.target.value)} />
      {hint && <p className="mt-1 text-xs text-[var(--color-muted-foreground)]">{hint}</p>}
    </div>
  );
}
