import React from "react";
import { useState } from "react";
import api from "../api/bidintelApi";

export default function UploadDocument() {
  const [file, setFile] = useState(null);
  const [steps, setSteps] = useState([]);

  async function ingest() {
    const fd = new FormData();
    fd.append("file", file);
    fd.append("title", file.name);
    fd.append("access_groups", JSON.stringify(["Proposal_Team", "Capture_Team"]));
    const res = await api.post("/upload", fd);   // -> upload_routes.py
    setSteps(res.data.pipeline);                  // drives the green checks
  }

  return (
    <div>
      <input type="file" accept="application/pdf" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={ingest} disabled={!file}>Ingest</button>
      <ul>{steps.map((s) => <li key={s}>✓ {s}</li>)}</ul>
    </div>
  );
}
