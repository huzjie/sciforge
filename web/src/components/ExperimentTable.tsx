import { ExperimentResult } from "../api";

export default function ExperimentTable({ experiments }: { experiments: ExperimentResult[] }) {
  return (
    <div className="panel">
      <h2>实验</h2>
      {experiments.length === 0 && <p className="empty">暂无</p>}
      <table>
        <thead>
          <tr><th>#</th><th>效应量</th><th>结论</th></tr>
        </thead>
        <tbody>
          {experiments.map((e, i) => (
            <tr key={e.id}>
              <td>{i + 1}</td>
              <td>{(e.metrics.effect_size ?? 0).toFixed(3)}</td>
              <td>{e.conclusion}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
