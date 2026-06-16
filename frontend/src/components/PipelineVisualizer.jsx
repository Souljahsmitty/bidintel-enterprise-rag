const STAGES = ["retrieve", "rerank", "context", "generate", "evaluate"];

export default function PipelineVisualizer({ trace = {} }) {
  return (
    <div className="pipeline">
      {STAGES.map((s) => (
        <div key={s} className={`stage ${trace.current === s ? "active" : ""}`}>
          <span>{s}</span><small>{trace[s] ?? "—"} ms</small>
        </div>
      ))}
    </div>
  );
}
