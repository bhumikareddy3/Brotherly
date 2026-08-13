import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import logo from "../assets/logo.png";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");

    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }

    setSubmitting(true);
    try {
      await register(name, email, password);
      navigate("/", { replace: true });
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
        <h1 style={{ fontSize: "1.7rem" }}>Create your account</h1>
        <p className="lede" style={{ fontSize: "1rem" }}>
          A few seconds to set up — then straight into your assessment.
        </p>

        <form onSubmit={handleSubmit}>
          <div className="field">
            <label>Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              autoComplete="name"
              required
            />
          </div>
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
              autoComplete="new-password"
              required
            />
            <div className="field-hint">At least 8 characters.</div>
          </div>

          {error && <div className="banner error">{error}</div>}

          <button type="submit" className="btn btn-primary btn-block" disabled={submitting}>
            {submitting ? <span className="spinner" /> : "Create account"}
          </button>
        </form>

        <p style={{ marginTop: "1.25rem", textAlign: "center", color: "var(--muted)" }}>
          Already have an account? <Link to="/login" style={{ color: "var(--green)", fontWeight: 700 }}>Log in</Link>
        </p>
      </div>
    </div>
  );
}
