import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000",
});

// Attach auth token (from Cognito in prod) + tenant to every request.
api.interceptors.request.use((cfg) => {
  const token = localStorage.getItem("id_token");
  if (token) cfg.headers.Authorization = `Bearer ${token}`;
  cfg.headers["X-Tenant-Id"] = localStorage.getItem("tenant_id") || "demo";
  return cfg;
});

export default api;
