import { useState } from "react";
import api from "../api/bidintelApi";
import AnswerPanel from "./AnswerPanel";
import EvidencePanel from "./EvidencePanel";

export default function AskQuestion({ opportunityId }) {
  const [q, setQ] = useState("");
  const [data, setData] = useState(null);

  async function ask() {
    const res = await api.post("/ask", { question: q, opportunity_id: opportunityId });
    setData(res.data);
  }

  return (
    <div className="ask">
      <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Ask your knowledge base..." />
      <button onClick={ask}>Ask</button>
      {data && (
        <div className="results">
          <AnswerPanel answer={data.answer} citations={data.citations} evalScores={data.eval} />
          <EvidencePanel evidence={data.evidence} />
        </div>
      )}
    </div>
  );
}
