export interface ResearchReport {
  question: string;
  iterations: number;
  converged: boolean;
  conclusion: string;
  hypotheses: { id: string; statement: string; score: number; status: string }[];
  experiments: { id: string; design_id: string; conclusion: string; metrics: Record<string, number> }[];
}

export interface DoctorInfo {
  provider: string;
  provider_ok: boolean;
  providers_available: string[];
  max_iterations: number;
}
