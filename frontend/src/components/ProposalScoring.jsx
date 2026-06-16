import React from "react";
import { useState } from "react";
import api from "../api/bidintelApi";

export default function ProposalScoring({ opportunityId }) {
  const [r, setR] = useState(null);
  async function score() {
    const res = await api.post("/score-proposal", { opportunity_id: opportunityId });
    setR(res.data);
  }
  return (
    <div>
      <button onClick={score}>Run Bid / No-Bid</button>
      {r && (
        <div>
          <h2>{r.final_score} / 100 — {r.recommendation}</h2>
          <ul>{Object.entries(r.factors).map(([k, v]) => <li key={k}>{k}: {v}</li>)}</ul>
        </div>
      )}
    </div>
  );
}
