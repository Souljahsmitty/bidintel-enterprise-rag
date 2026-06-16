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

export default function AnswerPanel({ answer, citations = [], evalScores = {} }) {
  return (
    <div className="answer-panel">
      <p>{answer}</p>
      <div className="sources">
        {citations.map((c) => (
          <span key={c.marker} className="chip">[{c.marker}] doc {c.document_id} p{c.page}</span>
        ))}
      </div>
      <Bar label="Faithfulness" value={evalScores.faithfulness} />
      <Bar label="Answer rel." value={evalScores.answer_relevance} />
      <Bar label="Context prec." value={evalScores.context_precision} />
    </div>
  );
}
