import type { Metadata, Viewport } from "next";
import { GeistSans } from "geist/font/sans";
import { GeistMono } from "geist/font/mono";
import { Analytics } from "@vercel/analytics/next";
import { SpeedInsights } from "@vercel/speed-insights/next";

import "./globals.css";

import { Providers } from "@/components/providers";
import { SiteHeader } from "@/components/site-header";
import { SiteFooter } from "@/components/site-footer";

export const metadata: Metadata = {
  metadataBase: new URL(process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000"),
  title: {
    default: "CivicRadar — Concursos públicos compatíveis com o seu perfil",
    template: "%s · CivicRadar",
  },
  description:
    "Open source radar para oportunidades de carreira pública no Brasil. Encontre, filtre e acompanhe concursos compatíveis com seu perfil.",
  keywords: [
    "concursos públicos",
    "civic tech",
    "open source",
    "carreira pública",
    "Brasil",
    "Cebraspe",
    "FGV",
  ],
  authors: [{ name: "CivicRadar contributors" }],
  openGraph: {
    type: "website",
    locale: "pt_BR",
    url: "/",
    title: "CivicRadar",
    description: "Open source radar para oportunidades de carreira pública no Brasil.",
    siteName: "CivicRadar",
  },
  twitter: {
    card: "summary_large_image",
    title: "CivicRadar",
    description: "Open source radar para oportunidades de carreira pública no Brasil.",
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#ffffff" },
    { media: "(prefers-color-scheme: dark)", color: "#252525" },
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }): JSX.Element {
  return (
    <html
      lang="pt-BR"
      suppressHydrationWarning
      className={`${GeistSans.variable} ${GeistMono.variable}`}
    >
      <body className="min-h-screen font-sans antialiased">
        <Providers>
          <div className="flex min-h-screen flex-col">
            <SiteHeader />
            <main className="flex-1">{children}</main>
            <SiteFooter />
          </div>
        </Providers>
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
