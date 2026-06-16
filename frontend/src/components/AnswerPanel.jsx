import React from "react";

function Bar({ label, value }) {
  return (
    <div className="bar">
      <span>{label}</span>
      <div className="track"><div className="fill" style={{ width: `${value * 100}%` }} /></div>
      <b>{value?.toFixed(2)}</b>
    </div>
  );
}

export default function AnswerPanel({ answer, citations = [], evalScores = {}, meta = {} }) {
  const source = meta.answer_source || evalScores.answer_source || "unknown";
  const confidence = meta.confidence?.score ?? meta.confidence ?? evalScores.confidence_score;
  const chipRow = { display: "flex", flexWrap: "wrap", gap: "6px", margin: "8px 0" };
  const chip = { border: "1px solid #cfe3ff", borderRadius: "999px", padding: "3px 10px", color: "#2563eb", background: "#eef6ff", fontSize: "12px", fontWeight: 600 };
  return (
    <div className="answer-panel">
      <div className="sources" style={chipRow}>
        <span className="chip" style={chip}>source: {source}</span>
        <span className="chip" style={chip}>model: {meta.model || "unknown"}</span>
        {confidence !== undefined && <span className="chip" style={chip}>confidence: {Number(confidence).toFixed(3)}</span>}
        {meta.cached_from && <span className="chip" style={chip}>cached from: {meta.cached_from}</span>}
      </div>
      <p>{answer}</p>
      <div className="sources" style={chipRow}>
        {citations.map((c) => (
          <span key={c.marker} className="chip" style={chip}>[{c.marker}] doc {c.document_id} p{c.page}</span>
        ))}
      </div>
      <Bar label="Faithfulness" value={evalScores.faithfulness} />
      <Bar label="Answer rel." value={evalScores.answer_relevance} />
      <Bar label="Context prec." value={evalScores.context_precision} />
    </div>
  );
}
