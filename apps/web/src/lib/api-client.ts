import type {
  MatchProfile,
  MatchResponse,
  OpportunityDetail,
  OpportunityFilters,
  OpportunityListResponse,
  SourceListResponse,
  StatsResponse,
} from "@/lib/types";

const BROWSER_API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

const SERVER_API_URL =
  process.env.INTERNAL_API_URL ?? process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

function baseUrl(): string {
  return typeof window === "undefined" ? SERVER_API_URL : BROWSER_API_URL;
}

class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly url: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${baseUrl()}${path}`;
  const response = await fetch(url, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json",
      ...(init?.headers ?? {}),
    },
    cache: init?.cache ?? "no-store",
  });

  if (!response.ok) {
    const detail = await response.text().catch(() => "");
    throw new ApiError(
      `${response.status} ${response.statusText} — ${detail.slice(0, 200)}`,
      response.status,
      url,
    );
  }

  return (await response.json()) as T;
}

function queryString(filters: OpportunityFilters): string {
  const params = new URLSearchParams();
  if (filters.q) params.set("q", filters.q);
  filters.state?.forEach((s) => params.append("state", s));
  filters.area?.forEach((a) => params.append("area", a));
  if (filters.city) params.set("city", filters.city);
  if (filters.education_level) params.set("education_level", filters.education_level);
  if (filters.salary_min != null) params.set("salary_min", filters.salary_min.toString());
  if (filters.status) params.set("status", filters.status);
  if (filters.board) params.set("board", filters.board);
  if (filters.organization) params.set("organization", filters.organization);
  if (filters.cursor) params.set("cursor", filters.cursor);
  if (filters.limit) params.set("limit", filters.limit.toString());
  if (filters.sort) params.set("sort", filters.sort);
  const qs = params.toString();
  return qs ? `?${qs}` : "";
}

export const api = {
  listOpportunities: (filters: OpportunityFilters = {}) =>
    request<OpportunityListResponse>(`/v1/opportunities${queryString(filters)}`),

  getOpportunity: (id: string) => request<OpportunityDetail>(`/v1/opportunities/${id}`),

  listSources: () => request<SourceListResponse>("/v1/sources"),

  getStats: () => request<StatsResponse>("/v1/stats"),

  match: (profile: MatchProfile, limit = 50) =>
    request<MatchResponse>(`/v1/match?limit=${limit}`, {
      method: "POST",
      body: JSON.stringify(profile),
    }),
};

export { ApiError };
