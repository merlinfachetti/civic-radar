import Link from "next/link";
import { Radar } from "lucide-react";

export function SiteFooter(): JSX.Element {
  return (
    <footer className="mt-20 border-t border-[var(--color-border)]">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="flex flex-col gap-8 md:flex-row md:justify-between">
          <div className="space-y-2">
            <div className="flex items-center gap-2 font-mono text-sm font-semibold">
              <Radar className="size-4 text-[var(--color-primary)]" aria-hidden />
              CivicRadar
            </div>
            <p className="max-w-md text-sm text-[var(--color-muted-foreground)]">
              Radar open source para oportunidades de carreira pública no Brasil. Não substitui
              fonte oficial — sempre confirme nos canais originais.
            </p>
          </div>

          <div className="grid grid-cols-2 gap-6 text-sm sm:grid-cols-3">
            <div>
              <p className="mb-2 font-medium">Projeto</p>
              <ul className="space-y-1.5 text-[var(--color-muted-foreground)]">
                <li>
                  <Link href="/about" className="hover:text-[var(--color-foreground)]">
                    Sobre
                  </Link>
                </li>
                <li>
                  <Link href="/sources" className="hover:text-[var(--color-foreground)]">
                    Fontes
                  </Link>
                </li>
                <li>
                  <Link href="/contribute" className="hover:text-[var(--color-foreground)]">
                    Contribuir
                  </Link>
                </li>
              </ul>
            </div>
            <div>
              <p className="mb-2 font-medium">Desenvolvedores</p>
              <ul className="space-y-1.5 text-[var(--color-muted-foreground)]">
                <li>
                  <a
                    href="http://localhost:8000/docs"
                    className="font-mono hover:text-[var(--color-foreground)]"
                  >
                    API Docs
                  </a>
                </li>
                <li>
                  <a
                    href="https://github.com/merlinfachetti/civic-radar"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-[var(--color-foreground)]"
                  >
                    GitHub
                  </a>
                </li>
                <li>
                  <a
                    href="https://github.com/merlinfachetti/civic-radar/issues"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-[var(--color-foreground)]"
                  >
                    Issues
                  </a>
                </li>
              </ul>
            </div>
            <div>
              <p className="mb-2 font-medium">Legal</p>
              <ul className="space-y-1.5 text-[var(--color-muted-foreground)]">
                <li>
                  <a
                    href="https://github.com/merlinfachetti/civic-radar/blob/main/LICENSE"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-[var(--color-foreground)]"
                  >
                    AGPL-3.0
                  </a>
                </li>
                <li>
                  <a
                    href="https://github.com/merlinfachetti/civic-radar/blob/main/docs/SECURITY.md"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="hover:text-[var(--color-foreground)]"
                  >
                    Segurança
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>

        <p className="mt-8 border-t border-[var(--color-border)] pt-6 text-xs text-[var(--color-muted-foreground)]">
          Construído com ♥ como ferramenta de civic-tech. Open source AGPL-3.0.
        </p>
      </div>
    </footer>
  );
}
