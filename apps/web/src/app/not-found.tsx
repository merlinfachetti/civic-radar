import Link from "next/link";

import { Button } from "@/components/ui/button";

export default function NotFound(): JSX.Element {
  return (
    <div className="mx-auto flex min-h-[60vh] max-w-md flex-col items-center justify-center px-4 text-center">
      <p className="font-mono text-xs text-[var(--color-muted-foreground)]">404</p>
      <h1 className="mt-2 text-3xl font-semibold tracking-tight">Página fora do radar</h1>
      <p className="mt-3 text-sm text-[var(--color-muted-foreground)]">
        Esta rota não está mapeada. Talvez a oportunidade tenha sido encerrada ou o link tenha sido
        renomeado.
      </p>
      <Button asChild className="mt-6">
        <Link href="/">Voltar à página inicial</Link>
      </Button>
    </div>
  );
}
