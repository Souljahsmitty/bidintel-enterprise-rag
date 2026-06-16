// Shared backend helpers used by every page.
const API = "http://localhost:8000";
window.API = API;
const TENANT = () => localStorage.getItem("tenant_id") || "demo";

function authHeaders(json) {
  const h = { "X-Tenant-Id": TENANT() };
  const t = localStorage.getItem("id_token");
  if (t) h["Authorization"] = "Bearer " + t;
  if (json) h["Content-Type"] = "application/json";
  return h;
}
async function apiGet(path) {
  const r = await fetch(API + path, { headers: authHeaders(false) });
  return r.json();
}
async function apiPostJson(path, body) {
  const r = await fetch(API + path, { method:"POST", headers: authHeaders(true), body: JSON.stringify(body) });
  return r.json();
}
async function apiPostForm(path, formData) {
  const r = await fetch(API + path, { method:"POST", headers: authHeaders(false), body: formData });
  return r.json();
}
// send the user to login if not signed in
function requireAuth() {
  if (!localStorage.getItem("id_token")) window.location = "login.html";
}
function logout() { localStorage.clear(); window.location = "login.html"; }
