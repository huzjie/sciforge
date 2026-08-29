import { ResearchReport, DoctorInfo } from "./types";

export class SciforgeClient {
  constructor(private baseUrl = "http://localhost:8000") {}

  async doctor(): Promise<DoctorInfo> {
    const r = await fetch(`${this.baseUrl}/doctor`);
    return r.json();
  }

  async research(question: string): Promise<ResearchReport> {
    const r = await fetch(`${this.baseUrl}/research`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question })
    });
    return r.json();
  }
}
