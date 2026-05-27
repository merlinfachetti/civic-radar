"use client";

import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";
import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";

export function ThemeToggle(): JSX.Element {
  const { theme, resolvedTheme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  const active = mounted ? (theme ?? resolvedTheme) : "dark";
  const isLight = active === "light";

  return (
    <Button
      variant="ghost"
      size="icon"
      aria-label={isLight ? "Mudar para tema escuro" : "Mudar para tema claro"}
      onClick={() => setTheme(isLight ? "dark" : "light")}
    >
      {mounted && isLight ? (
        <Moon className="size-4" aria-hidden />
      ) : (
        <Sun className="size-4" aria-hidden />
      )}
    </Button>
  );
}
