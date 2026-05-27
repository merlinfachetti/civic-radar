"use client";

import { motion } from "framer-motion";
import { cn } from "@/lib/utils";

interface MatchScoreVisualProps {
  score: number;
  size?: number;
  className?: string;
}

/** Radial progress with a glow on high scores. */
export function MatchScoreVisual({
  score,
  size = 64,
  className,
}: MatchScoreVisualProps): JSX.Element {
  const clamped = Math.max(0, Math.min(100, score));
  const radius = (size - 8) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (clamped / 100) * circumference;

  const tone =
    clamped >= 75
      ? "var(--color-success)"
      : clamped >= 50
        ? "var(--color-primary)"
        : "var(--color-muted-foreground)";

  return (
    <div
      className={cn("relative inline-flex items-center justify-center", className)}
      style={{ width: size, height: size }}
      aria-label={`Match score: ${clamped} de 100`}
      role="img"
    >
      <svg width={size} height={size} className="-rotate-90" aria-hidden>
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke="var(--color-muted)"
          strokeWidth={4}
          fill="none"
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          stroke={tone}
          strokeWidth={4}
          strokeLinecap="round"
          fill="none"
          style={{
            filter: clamped >= 75 ? "drop-shadow(0 0 6px var(--color-radar-glow))" : "none",
          }}
          initial={{ strokeDasharray: circumference, strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        />
      </svg>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <span className="font-mono text-base font-semibold tabular-nums" style={{ color: tone }}>
          {clamped}
        </span>
        <span className="text-[10px] text-[var(--color-muted-foreground)]">/ 100</span>
      </div>
    </div>
  );
}
