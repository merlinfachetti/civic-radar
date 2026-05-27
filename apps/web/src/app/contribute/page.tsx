import { Github, FilePlus, Bug, BookOpen } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export const metadata = {
  title: "Contribuir",
};

export default function ContributePage(): JSX.Element {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8">
      <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Contribuir</h1>
      <p className="mt-4 text-[var(--color-muted-foreground)]">
        Toda contribuição é valiosa — desde correção de typo até adicionar uma nova banca. Veja{" "}
        <a
          href="https://github.com/merlinfachetti/civic-radar/blob/main/docs/CONTRIBUTING.md"
          target="_blank"
          rel="noopener noreferrer"
          className="text-[var(--color-primary)] hover:underline"
        >
          docs/CONTRIBUTING.md
        </a>{" "}
        para o guia completo.
      </p>

      <div className="mt-8 grid gap-4 sm:grid-cols-2">
        <ActionCard
          icon={<FilePlus className="size-5" aria-hidden />}
          title="Adicionar nova fonte"
          description="Banca, prefeitura, órgão público — cada fonte é um plugin independente."
          href="https://github.com/merlinfachetti/civic-radar/issues/new?template=new_source.yml"
        />
        <ActionCard
          icon={<Bug className="size-5" aria-hidden />}
          title="Reportar parser quebrado"
          description="Quando layout muda, parsers podem parar de extrair corretamente."
          href="https://github.com/merlinfachetti/civic-radar/issues/new?template=parser_broken.yml"
        />
        <ActionCard
          icon={<BookOpen className="size-5" aria-hidden />}
          title="Melhorar documentação"
          description="Typos, exemplos, traduções, screenshots — tudo conta."
          href="https://github.com/merlinfachetti/civic-radar/issues?q=is%3Aissue+is%3Aopen+label%3Adocumentation"
        />
        <ActionCard
          icon={<Github className="size-5" aria-hidden />}
          title="Ver good first issues"
          description="Issues delimitadas, ideais para primeira contribuição."
          href="https://github.com/merlinfachetti/civic-radar/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22"
        />
      </div>

      <Card className="mt-8 border-dashed p-6">
        <h2 className="font-semibold">Quero ajudar mas não programo</h2>
        <p className="mt-2 text-sm text-[var(--color-muted-foreground)]">
          Você pode (1) sugerir fontes via issue, (2) reportar oportunidades desatualizadas, (3)
          revisar acessibilidade do site, (4) sugerir melhorias de UX, (5) divulgar o projeto. Toda
          forma de contribuição é bem-vinda.
        </p>
        <div className="mt-4">
          <Button asChild>
            <a
              href="https://github.com/merlinfachetti/civic-radar/discussions/new?category=ideas"
              target="_blank"
              rel="noopener noreferrer"
            >
              Abrir uma discussão
            </a>
          </Button>
        </div>
      </Card>
    </div>
  );
}

function ActionCard({
  icon,
  title,
  description,
  href,
}: {
  icon: JSX.Element;
  title: string;
  description: string;
  href: string;
}): JSX.Element {
  return (
    <Card className="p-5 transition-shadow hover:shadow-[0_0_24px_-12px_var(--color-radar-glow)]">
      <a
        href={href}
        target="_blank"
        rel="noopener noreferrer"
        className="block focus-visible:outline-none"
      >
        <div className="mb-3 inline-flex size-9 items-center justify-center rounded-md bg-[var(--color-primary)]/10 text-[var(--color-primary)]">
          {icon}
        </div>
        <h3 className="font-semibold">{title}</h3>
        <p className="mt-1 text-sm text-[var(--color-muted-foreground)]">{description}</p>
      </a>
    </Card>
  );
}
