export interface DoctorInfo {
  provider: string;
  provider_ok: boolean;
  providers_available: string[];
  max_iterations: number;
}

export interface Hypothesis {
  id: string;
  statement: string;
  score: number;
  status: string;
}

export interface ExperimentResult {
  id: string;
  design_id: string;
  conclusion: string;
  metrics: Record<string, number>;
}

export interface ResearchReport {
  question: string;
  iterations: number;
  converged: boolean;
  conclusion: string;
  hypotheses: Hypothesis[];
  experiments: ExperimentResult[];
}

const BASE = "/api";

export async function fetchDoctor(): Promise<DoctorInfo> {
  const r = await fetch(`${BASE}/doctor`);
  return r.json();
}

export async function runResearch(question: string): Promise<ResearchReport> {
  const r = await fetch(`${BASE}/research`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  });
  return r.json();
}
