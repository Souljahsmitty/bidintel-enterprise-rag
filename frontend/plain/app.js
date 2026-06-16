// app.js — wires every button to a backend route. The backend runs the RAG pipeline.
const API = "http://localhost:8000";          // FastAPI backend
const TENANT = "demo";

async function call(path, opts = {}) {
  opts.headers = Object.assign({ "X-Tenant-Id": TENANT }, opts.headers || {});
  const res = await fetch(API + path, opts);
  if (!res.ok) throw new Error(path + " -> " + res.status);
  return res.json();
}

// BUTTON 1: Ingest -> POST /upload -> pdf_loader -> chunker -> embedding -> store
document.getElementById("ingestBtn").addEventListener("click", async () => {
  const file = document.getElementById("fileInput").files[0];
  if (!file) return alert("Choose a PDF first");
  const fd = new FormData();
  fd.append("file", file);
  fd.append("title", file.name);
  fd.append("tenant_id", TENANT);
  fd.append("access_groups", JSON.stringify(["Proposal_Team"]));
  const data = await call("/upload", { method: "POST", body: fd });
  const ul = document.getElementById("pipeline");
  ul.innerHTML = "";
  (data.pipeline || []).forEach(step => {
    const li = document.createElement("li");
    li.textContent = "✓ " + step;           // green check per stage
    ul.appendChild(li);
  });
  ul.innerHTML += `<li>✓ ${data.chunks_inserted} chunks stored</li>`;
});

// BUTTON 2: Ask -> POST /ask -> cache/trusted KB/LLM fallback -> answer + citations
document.getElementById("askBtn").addEventListener("click", async () => {
  const q = document.getElementById("question").value.trim();
  if (!q) return;
  const data = await call("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: q, tenant_id: TENANT })
  });
  document.getElementById("answerPanel").classList.remove("hidden");
  document.getElementById("answerText").textContent = data.answer;
  // model-efficiency chips + citation chips
  const chips = document.getElementById("sources");
  chips.innerHTML = "";
  const source = data.answer_source || (data.eval || {}).answer_source || "unknown";
  const confidence = data.confidence?.score ?? data.confidence ?? (data.eval || {}).confidence_score;
  [`source: ${source}`, `model: ${data.model || "unknown"}`,
   confidence !== undefined ? `confidence: ${Number(confidence).toFixed(3)}` : null,
   data.cached_from ? `cached from: ${data.cached_from}` : null].filter(Boolean).forEach(label => {
    const s = document.createElement("span");
    s.className = "chip";
    s.textContent = label;
    chips.appendChild(s);
  });
  (data.citations || []).forEach(c => {
    const s = document.createElement("span");
    s.className = "chip";
    s.textContent = `[${c.marker}] doc ${c.document_id} p${c.page}`;
    chips.appendChild(s);
  });
  // quality scores
  const e = data.eval || {};
  document.getElementById("faith").textContent = (e.faithfulness ?? 0).toFixed(2);
  document.getElementById("arel").textContent  = (e.answer_relevance ?? 0).toFixed(2);
  document.getElementById("cprec").textContent = (e.context_precision ?? 0).toFixed(2);
  // retrieved evidence
  const ev = document.getElementById("evidence");
  ev.innerHTML = "";
  (data.evidence || []).forEach(x => {
    const d = document.createElement("div");
    d.className = "ev";
    const score = (x.rerank ?? x.rrf ?? 0).toFixed(2);
    d.innerHTML = `<span class="scoretag">${score}</span><b>chunk ${x.id}</b><br>${x.text.slice(0,140)}…`;
    ev.appendChild(d);
  });
  window._lastAnswerId = data.answer_id || "demo";
});

// BUTTON 3: Run scoring -> POST /score-proposal -> proposal_scoring_service
document.getElementById("scoreBtn").addEventListener("click", async () => {
  const data = await call("/score-proposal", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ opportunity_id: "dhs-cyber", tenant_id: TENANT })
  });
  document.getElementById("scoreOut").innerHTML =
    `<span class="score-big">${data.final_score}</span> / 100 — <b>${data.recommendation}</b>`;
});

// BUTTONS 4: Feedback -> POST /feedback (correct / wrong / needs_review)
document.querySelectorAll(".feedback .btn").forEach(btn => {
  btn.addEventListener("click", async () => {
    await call("/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ answer_id: window._lastAnswerId || "demo",
                             verdict: btn.dataset.verdict, tenant_id: TENANT })
    });
    btn.textContent = "Saved ✓";
  });
});
