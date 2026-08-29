import { Hypothesis } from "../api";

export default function HypothesisList({ hypotheses }: { hypotheses: Hypothesis[] }) {
  return (
    <div className="panel">
      <h2>假设</h2>
      {hypotheses.length === 0 && <p className="empty">暂无</p>}
      <ul>
        {hypotheses.map((h) => (
          <li key={h.id}>
            <span className="score">{h.score.toFixed(3)}</span>
            <span>{h.statement}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
