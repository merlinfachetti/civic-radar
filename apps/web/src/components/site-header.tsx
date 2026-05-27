"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Radar, Github } from "lucide-react";

import { Button } from "@/components/ui/button";
import { ThemeToggle } from "@/components/theme-toggle";
import { cn } from "@/lib/utils";

const NAV = [
  { href: "/opportunities", label: "Oportunidades" },
  { href: "/profile-match", label: "Match" },
  { href: "/sources", label: "Fontes" },
  { href: "/about", label: "Sobre" },
];

export function SiteHeader(): JSX.Element {
  const pathname = usePathname();

  return (
    <header className="glass sticky top-0 z-40 w-full border-b border-[var(--color-border)]">
      <div className="mx-auto flex h-14 max-w-7xl items-center gap-4 px-4 sm:px-6 lg:px-8">
        <Link
          href="/"
          className="flex items-center gap-2 font-mono text-sm font-semibold tracking-tight"
        >
          <Radar
            className="size-5 text-[var(--color-primary)]"
            style={{ filter: "drop-shadow(0 0 6px var(--color-radar-glow))" }}
            aria-hidden
          />
          <span>CivicRadar</span>
        </Link>

        <nav className="hidden items-center gap-1 text-sm md:flex">
          {NAV.map((item) => {
            const active = pathname === item.href || pathname.startsWith(item.href + "/");
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "rounded-md px-3 py-1.5 transition-colors",
                  active
                    ? "bg-[var(--color-accent)] text-[var(--color-foreground)]"
                    : "text-[var(--color-muted-foreground)] hover:bg-[var(--color-accent)]/60 hover:text-[var(--color-foreground)]",
                )}
              >
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="ml-auto flex items-center gap-1">
          <Button asChild variant="ghost" size="icon" aria-label="GitHub">
            <a
              href="https://github.com/merlinfachetti/civic-radar"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Github className="size-4" aria-hidden />
            </a>
          </Button>
          <ThemeToggle />
        </div>
      </div>

      <nav className="overflow-x-auto border-t border-[var(--color-border)]/60 px-2 py-1 md:hidden">
        <ul className="flex gap-1 text-xs">
          {NAV.map((item) => {
            const active = pathname === item.href || pathname.startsWith(item.href + "/");
            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={cn(
                    "block rounded-md px-3 py-1.5 whitespace-nowrap",
                    active
                      ? "bg-[var(--color-accent)] text-[var(--color-foreground)]"
                      : "text-[var(--color-muted-foreground)]",
                  )}
                >
                  {item.label}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
    </header>
  );
}
