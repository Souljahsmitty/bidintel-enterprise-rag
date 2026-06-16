import React from "react";
import api from "../api/bidintelApi";

export default function FeedbackButtons({ answerId }) {
  const send = (verdict) => api.post("/feedback", { answer_id: answerId, verdict });
  return (
    <div className="feedback">
      <button onClick={() => send("correct")}>Correct</button>
      <button onClick={() => send("wrong")}>Wrong</button>
      <button onClick={() => send("needs_review")}>Needs Review</button>
    </div>
  );
}
