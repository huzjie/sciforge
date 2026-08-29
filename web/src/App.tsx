import { useCallback, useEffect, useState } from "react";
import { fetchDoctor, runResearch, ResearchReport, DoctorInfo } from "./api";
import SummaryCards from "./components/SummaryCards";
import HypothesisList from "./components/HypothesisList";
import ExperimentTable from "./components/ExperimentTable";

export default function App() {
  const [doctor, setDoctor] = useState<DoctorInfo | null>(null);
  const [question, setQuestion] = useState("睡眠不足是否影响记忆巩固？");
  const [report, setReport] = useState<ResearchReport | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDoctor().then(setDoctor).catch(console.error);
  }, []);

  const onRun = useCallback(async () => {
    setLoading(true);
    try {
      const r = await runResearch(question);
      setReport(r);
    } finally {
      setLoading(false);
    }
  }, [question]);

  return (
    <div className="app">
      <header className="header">
        <h1>sciforge</h1>
        <span className="subtitle">AI 科研智能体与自动化科学发现平台</span>
        {doctor && (
          <span className="badge">
            provider: {doctor.provider} · iterations ≤ {doctor.max_iterations}
          </span>
        )}
      </header>

      <section className="controls">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="输入研究问题…"
        />
        <button onClick={onRun} disabled={loading}>
          {loading ? "研究中…" : "运行研究闭环"}
        </button>
      </section>

      {report && (
        <div className="report">
          <SummaryCards report={report} />
          <div className="grid">
            <HypothesisList hypotheses={report.hypotheses} />
            <ExperimentTable experiments={report.experiments} />
          </div>
          <p className="conclusion">{report.conclusion}</p>
        </div>
      )}
    </div>
  );
}
