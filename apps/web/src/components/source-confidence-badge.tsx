import { Badge } from "@/components/ui/badge";
import type { ConfidenceLevel } from "@/lib/types";
import { ShieldCheck, ShieldQuestion, ShieldAlert } from "lucide-react";
import { cn } from "@/lib/utils";

const CONFIG: Record<
  ConfidenceLevel,
  { label: string; variant: "success" | "warning" | "secondary"; icon: typeof ShieldCheck }
> = {
  high: { label: "Alta confiança", variant: "success", icon: ShieldCheck },
  medium: { label: "Confiança média", variant: "warning", icon: ShieldQuestion },
  low: { label: "Baixa confiança", variant: "secondary", icon: ShieldAlert },
};

export function SourceConfidenceBadge({
  level,
  className,
}: {
  level: ConfidenceLevel;
  className?: string;
}): JSX.Element {
  const { label, variant, icon: Icon } = CONFIG[level];
  return (
    <Badge variant={variant} className={cn("gap-1", className)}>
      <Icon className="size-3" aria-hidden />
      {label}
    </Badge>
  );
}
