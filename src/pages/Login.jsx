import { useState } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import logo from "../assets/logo.png";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from || "/";

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
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

  return (
    <div className="auth-shell">
      <div className="auth-card surface">
        <img src={logo} alt="Brotherly" className="auth-logo" />
        <h1 style={{ fontSize: "1.7rem" }}>Welcome back</h1>
        <p className="lede" style={{ fontSize: "1rem" }}>
          Log in to pick up where you left off.
        </p>

        <form onSubmit={handleSubmit}>
          <div className="field">
            <label>Email</label>
            <input
              type="text"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
              required
            />
          </div>
          <div className="field">
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="current-password"
              required
            />
          </div>

          {error && <div className="banner error">{error}</div>}

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
