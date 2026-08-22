import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";

export default function Dashboard() {
  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api
      .getDashboard()
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <p>Loading your dashboard…</p>;
  }

  if (error) {
    return <div className="banner error">{error}</div>;
  }

  if (!data || !data.has_data) {
    return (
      <div className="empty-state">
        <h2>Your dashboard is ready for a first signal</h2>
        <div className="quote-card" style={{ maxWidth: 520, margin: "1.5rem auto" }}>
          Complete the career assessment and this page will become your personal decision
          dashboard.
        </div>
        <Link to="/assessment" className="btn btn-primary">
          🧭 Take the assessment
        </Link>
      </div>
    );
  }

  const { latest, total_assessments, chat_count, plan } = data;
  const maxScore = Math.max(latest.risk_score, latest.financial_score, latest.leadership_score, latest.readiness_score, 1);

  return (
    <div>
      <div className="eyebrow">Your direction at a glance</div>
      <h1>A home for your progress.</h1>
      <p className="lede">
        Review your latest career signal, revisit your action plan, and keep an eye on how your
        thinking evolves.
      </p>

      <h3>Welcome back, {latest.name}</h3>
      <div className="metric-row">
        <div className="metric">
          <div className="label">Assessments</div>
          <div className="value">{total_assessments}</div>
        </div>
        <div className="metric">
          <div className="label">Readiness</div>
          <div className="value">{latest.readiness_score}</div>
        </div>
        <div className="metric">
          <div className="label">Risk signal</div>
          <div className="value">{latest.risk_score}/50</div>
        </div>
        <div className="metric">
          <div className="label">Mentor chats</div>
          <div className="value">{chat_count}</div>
        </div>
      </div>

      <div className="two-col" style={{ alignItems: "start", marginTop: "1.5rem" }}>
        <div>
          <div className="result-card">
            <div className="result-label">Current direction</div>
            <div className="result-value">{latest.primary_recommendation}</div>
            <p>
              {latest.career_path} · alternative: {latest.secondary_recommendation}
            </p>
          </div>
          <h3 style={{ marginTop: "1.5rem" }}>30-day focus</h3>
          <div className="surface">
            {plan.map((item, i) => {
              const [label, copy] = item.includes(" - ") ? item.split(" - ") : [`Step ${i + 1}`, item];
              return (
                <div className="step" key={item}>
                  <div className="step-number">{i + 1}</div>
                  <div>
                    <strong>{label}</strong>
                    <span className="muted">{copy}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        <div>
          <h3>Your signal mix</h3>
          <div className="surface">
            {[
              ["Risk", latest.risk_score],
              ["Financial", latest.financial_score],
              ["Leadership", latest.leadership_score],
              ["Readiness", latest.readiness_score],
            ].map(([label, value]) => (
              <div key={label} style={{ marginBottom: "0.9rem" }}>
                <div style={{ display: "flex", justifyContent: "space-between", fontSize: "0.85rem", marginBottom: "0.3rem" }}>
                  <span>{label}</span>
                  <strong>{value}</strong>
                </div>
                <div style={{ background: "var(--sage)", borderRadius: 999, height: 10, overflow: "hidden" }}>
                  <div
                    style={{
                      width: `${(value / maxScore) * 100}%`,
                      background: "var(--green)",
                      height: "100%",
                      borderRadius: 999,
                    }}
                  />
                </div>
              </div>
            ))}
            <p style={{ color: "var(--muted)", fontSize: "0.85rem", marginTop: "0.5rem" }}>
              Last assessed · {String(latest.created_at).slice(0, 16)}
            </p>
          </div>
        </div>
      </div>

      <div className="hero-rule" />
      <h3>Continue the work</h3>
      <div style={{ display: "flex", gap: "0.9rem", flexWrap: "wrap" }}>
        <Link to="/mentor" className="btn btn-secondary">
          💬 Talk to your mentor
        </Link>
        <Link to="/assessment" className="btn btn-secondary">
          🧭 Retake assessment
        </Link>
        <Link to="/history" className="btn btn-secondary">
          🕘 View your history
        </Link>
      </div>
    </div>
  );
}
