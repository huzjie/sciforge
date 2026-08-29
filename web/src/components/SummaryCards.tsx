import { ResearchReport } from "../api";

export default function SummaryCards({ report }: { report: ResearchReport }) {
  const cards = [
    { label: "迭代轮数", value: String(report.iterations) },
    { label: "假设数", value: String(report.hypotheses.length) },
    { label: "实验数", value: String(report.experiments.length) },
    { label: "是否收敛", value: report.converged ? "是" : "否" }
  ];
  return (
    <div className="cards">
      {cards.map((c) => (
        <div key={c.label} className="card">
          <div className="value">{c.value}</div>
          <div className="label">{c.label}</div>
        </div>
      ))}
    </div>
  );
}
