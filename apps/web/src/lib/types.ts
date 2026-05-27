/** TypeScript types mirroring the CivicRadar API.
 *
 * In the future, these can be auto-generated from `/openapi.json` via
 * openapi-typescript. For now they are hand-curated to match the Python
 * Pydantic schemas in apps/api/src/civic_radar/schemas/.
 */

export type OpportunityStatus = "draft" | "open" | "closed" | "cancelled";
export type ConfidenceLevel = "high" | "medium" | "low";
export type EducationLevel = "fundamental" | "medio" | "tecnico" | "superior" | "pos_graduacao";

export interface Opportunity {
  id: string;
  title: string;
  organization: string;
  board: string | null;
  area: string | null;
  position_name: string | null;
  education_level: EducationLevel | null;
  salary_min: number | null;
  salary_max: number | null;
  vacancies: number | null;
  state: string | null;
  city: string | null;
  status: OpportunityStatus;
  registration_start_date: string | null;
  registration_end_date: string | null;
  exam_date: string | null;
  source_url: string;
  confidence_level: ConfidenceLevel;
  last_checked_at: string;
}

export interface OpportunityDetail extends Opportunity {
  description: string | null;
  original_url: string | null;
  keywords: string[] | null;
  created_at: string;
  updated_at: string;
}

export interface PaginationMeta {
  next_cursor: string | null;
  has_more: boolean;
  total_count: number;
}

export interface OpportunityListResponse {
  items: Opportunity[];
  pagination: PaginationMeta;
}

export interface SourceItem {
  source_id: string;
  name: string;
  type: "agency" | "organizing_board" | "portal" | "aggregator";
  base_url: string;
  quality_level: ConfidenceLevel;
  enabled: boolean;
  last_successful_check_at: string | null;
  items_count: number;
}

export interface SourceListResponse {
  items: SourceItem[];
}

export interface StatsResponse {
  total_opportunities: number;
  open_opportunities: number;
  closed_opportunities: number;
  by_state: Record<string, number>;
  by_area: Record<string, number>;
  by_education_level: Record<string, number>;
  last_7_days: { new_opportunities: number; closed_opportunities: number };
  sources: { total: number; healthy: number };
}

export interface MatchProfile {
  areas: string[];
  states: string[];
  cities: string[];
  education_level: EducationLevel | null;
  minimum_salary: number | null;
  keywords: string[];
  include_remote: boolean;
}

export interface MatchReason {
  criterion: string;
  points: number;
  weight: number;
  explanation: string;
}

export interface MatchResult {
  opportunity_id: string;
  opportunity: Opportunity;
  score: number;
  max_score: number;
  reasons: MatchReason[];
}

export interface MatchResponse {
  matches: MatchResult[];
  total_evaluated: number;
  total_returned: number;
}

export interface OpportunityFilters {
  q?: string;
  state?: string[];
  area?: string[];
  city?: string;
  education_level?: EducationLevel;
  salary_min?: number;
  status?: OpportunityStatus;
  board?: string;
  organization?: string;
  cursor?: string;
  limit?: number;
  sort?: string;
}
