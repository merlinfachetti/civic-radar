import { Card } from "@/components/ui/card";

export const metadata = {
  title: "Sobre",
};

export default function AboutPage(): JSX.Element {
  return (
    <div className="mx-auto max-w-3xl px-4 py-12 sm:px-6 lg:px-8">
      <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Sobre o CivicRadar</h1>
      <p className="mt-4 text-[var(--color-muted-foreground)]">
        CivicRadar é uma plataforma open source que monitora, normaliza e recomenda concursos
        públicos brasileiros com base no perfil de cada pessoa. O objetivo é facilitar acesso a
        informação pública sem substituir os canais oficiais.
      </p>

      <h2 className="mt-10 text-xl font-semibold">Princípios</h2>
      <ul className="mt-3 list-disc space-y-2 pl-5 text-sm text-[var(--color-muted-foreground)]">
        <li>Fontes oficiais sempre em primeiro lugar</li>
        <li>Rastreabilidade total — link, data de verificação, nível de confiança</li>
        <li>Open data mindset — metadados, nunca cópia integral</li>
        <li>Baixa dependência de infra — roda local em minutos</li>
        <li>Comunidade primeiro — contribuição é fácil, decisões são públicas</li>
      </ul>

      <h2 className="mt-10 text-xl font-semibold">O que NÃO é</h2>
      <Card className="mt-3 p-5">
        <ul className="space-y-1.5 text-sm text-[var(--color-muted-foreground)]">
          <li>❌ Fonte oficial — não substitui banca ou órgão</li>
          <li>❌ Garantia de inscrição ou aprovação</li>
          <li>❌ Serviço jurídico ou de consultoria</li>
          <li>❌ Agregador comercial fechado</li>
        </ul>
      </Card>

      <h2 className="mt-10 text-xl font-semibold">Licença e Disclaimer</h2>
      <p className="mt-3 text-sm text-[var(--color-muted-foreground)]">
        CivicRadar é distribuído sob <span className="font-mono">AGPL-3.0</span>. Modificações
        hospedadas como SaaS devem ser disponibilizadas em código aberto. Para detalhes legais, veja
        o arquivo <span className="font-mono">LICENSE</span> no repositório.
      </p>
    </div>
  );
}
