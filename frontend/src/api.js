const API_BASE = import.meta.env.API_BASE || "http://localhost:8000";
const TOKEN_KEY = "brotherly_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

async function request(path, options = {}) {
  const token = getToken();
  const headers = { "Content-Type": "application/json", ...(options.headers || {}) };
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  let data = null;
  try {
    data = await res.json();
  } catch {
    // no JSON body
  }

  if (res.status === 401) {
    // Session expired or invalid — clear it and let the app know so it can
    // redirect to login, even if this call came from deep in a page.
    setToken(null);
    window.dispatchEvent(new Event("brotherly:unauthorized"));
  }

  if (!res.ok) {
    const message = (data && data.detail) || `Request failed (${res.status})`;
    throw new Error(message);
  }

  return data;
}

export const api = {
  register: (name, email, password) =>
    request("/api/auth/register", { method: "POST", body: JSON.stringify({ name, email, password }) }),
  login: (email, password) =>
    request("/api/auth/login", { method: "POST", body: JSON.stringify({ email, password }) }),
  me: () => request("/api/auth/me"),

  submitAssessment: (payload) =>
    request("/api/assessment", { method: "POST", body: JSON.stringify(payload) }),
  getDashboard: () => request("/api/dashboard"),
  getHistory: () => request("/api/history"),
  sendMentorMessage: (message, context) =>
    request("/api/mentor/chat", {
      method: "POST",
      body: JSON.stringify({ message, context }),
    }),
  getChats: () => request("/api/chats"),
};
