import React from "react";

export default function EvidencePanel({ evidence = [] }) {
  return (
    <aside className="evidence-panel">
      <h3>Retrieved Context</h3>
      {evidence.map((e, i) => (
        <div key={e.id || i} className="evidence-card">
          <b>chunk {e.id}</b> <span>{(e.rerank ?? e.rrf)?.toFixed(2)}</span>
          <p>{e.text.slice(0, 140)}…</p>
        </div>
      ))}
    </aside>
  );
}
