import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { GoogleLogin } from "@react-oauth/google";
import { useAuth } from "../context/AuthContext";
import logo from "../assets/logo.png";

// Premium SVG Icons for the Password Toggle
const EyeOpen = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLineJoin="round">
    <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
    <circle cx="12" cy="12" r="3"></circle>
  </svg>
);

const EyeClosed = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLineJoin="round">
    <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
    <line x1="1" y1="1" x2="23" y2="23"></line>
  </svg>
);

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from || "/";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await login(email, password);
      navigate(from, { replace: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  async function handleGoogleSuccess(credentialResponse) {
    setError("");
    setSubmitting(true);
    try {
      const apiBase = import.meta.env.API_BASE || "http://localhost:8000";
      const res = await fetch(`${apiBase}/api/auth/google`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ credential: credentialResponse.credential }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.detail || "Google authentication failed.");
      }

      // Store auth session
      localStorage.setItem("brotherly_token", data.token);
      localStorage.setItem("brotherly_user", JSON.stringify(data.user));

      // Refresh to load authenticated state
      window.location.href = from;
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  // Uniform premium input styling to fix the squished password box issue
  const inputStyle = {
    width: "100%",
    padding: "0.75rem 1rem",
    fontSize: "1rem",
    borderRadius: "8px",
    border: "1px solid #d1d5db",
    boxSizing: "border-box",
    fontFamily: "inherit",
    outline: "none"
  };

  return (
    <div className="auth-shell">
      <div className="auth-card surface">
        <img src={logo} alt="Brotherly" className="auth-logo" />
        <h1 style={{ fontSize: "1.7rem" }}>Welcome back</h1>
        <p className="lede" style={{ fontSize: "1rem" }}>
          Log in to pick up where you left off.
        </p>

        {/* Google Sign-In Button */}
        <div style={{ display: "flex", justifyContent: "center", marginBottom: "1.25rem" }}>
          <GoogleLogin
            onSuccess={handleGoogleSuccess}
            onError={() => setError("Google login failed. Please try again.")}
            theme="outline"
            size="large"
            width="100%"
          />
        </div>

        <div style={{ display: "flex", alignItems: "center", margin: "1.25rem 0", color: "var(--muted)" }}>
          <hr style={{ flex: 1, borderColor: "rgba(255, 255, 255, 0.1)" }} />
          <span style={{ padding: "0 0.75rem", fontSize: "0.85rem" }}>or with email</span>
          <hr style={{ flex: 1, borderColor: "rgba(255, 255, 255, 0.1)" }} />
        </div>

        <form onSubmit={handleSubmit}>
          <div className="field" style={{ marginBottom: "1rem", textAlign: "left" }}>
            <label style={{ display: "block", marginBottom: "0.4rem", fontWeight: "600", fontSize: "0.9rem" }}>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
              style={inputStyle}
              required
            />
          </div>
          <div className="field" style={{ marginBottom: "1.5rem", textAlign: "left" }}>
            <label style={{ display: "block", marginBottom: "0.4rem", fontWeight: "600", fontSize: "0.9rem" }}>Password</label>
            <div style={{ position: "relative", display: "flex", alignItems: "center" }}>
              <input
                type={showPassword ? "text" : "password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                autoComplete="current-password"
                style={{ ...inputStyle, paddingRight: "3rem" }}
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{
                  position: "absolute",
                  right: "0.5rem",
                  background: "transparent",
                  border: "none",
                  cursor: "pointer",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: "#6b7280",
                  padding: "0.25rem"
                }}
              >
                {showPassword ? <EyeClosed /> : <EyeOpen />}
              </button>
            </div>
          </div>

          {error && <div className="banner error" style={{ marginBottom: "1rem" }}>{error}</div>}

          <button type="submit" className="btn btn-primary btn-block" disabled={submitting}>
            {submitting ? <span className="spinner" /> : "Log in"}
          </button>
        </form>

        <p style={{ marginTop: "1.25rem", textAlign: "center", color: "var(--muted)" }}>
          New here? <Link to="/register" style={{ color: "var(--green)", fontWeight: 700 }}>Create an account</Link>
        </p>
      </div>
    </div>
  );
}