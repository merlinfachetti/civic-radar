import { describe, expect, it } from "vitest";

import { cn, daysUntil, formatBRL, formatDateBR, formatSalaryRange } from "./utils";

describe("cn", () => {
  it("merges classes deduping tailwind conflicts", () => {
    expect(cn("px-2", "px-4")).toBe("px-4");
  });

  it("filters out falsy values", () => {
    expect(cn("a", false, undefined, "b")).toBe("a b");
  });
});

describe("formatBRL", () => {
  it("formats a number as BRL", () => {
    expect(formatBRL(5000)).toContain("R$");
    expect(formatBRL(5000)).toContain("5.000");
  });

  it("returns em-dash for null", () => {
    expect(formatBRL(null)).toBe("—");
  });
});

describe("formatSalaryRange", () => {
  it("returns a range when both bounds differ", () => {
    const text = formatSalaryRange(5000, 8000);
    expect(text).toMatch(/–/);
  });

  it("returns single value when min === max", () => {
    const text = formatSalaryRange(5000, 5000);
    expect(text).not.toMatch(/–/);
  });

  it("returns placeholder when both are null", () => {
    expect(formatSalaryRange(null, null)).toBe("Salário a definir");
  });
});

describe("daysUntil", () => {
  it("returns null for null input", () => {
    expect(daysUntil(null)).toBeNull();
  });

  it("returns a non-negative number for a future date", () => {
    const future = new Date(Date.now() + 5 * 86_400_000).toISOString().slice(0, 10);
    expect(daysUntil(future)).toBeGreaterThanOrEqual(4);
  });

  it("returns a negative number for past dates", () => {
    const past = new Date(Date.now() - 5 * 86_400_000).toISOString().slice(0, 10);
    expect(daysUntil(past)).toBeLessThanOrEqual(-4);
  });
});

describe("formatDateBR", () => {
  it("formats ISO to pt-BR locale", () => {
    expect(formatDateBR("2026-05-27")).toMatch(/27\/05\/2026/);
  });

  it("returns em-dash for null", () => {
    expect(formatDateBR(null)).toBe("—");
  });
});
