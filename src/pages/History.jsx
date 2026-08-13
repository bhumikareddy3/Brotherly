import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";

export default function History() {
  const [assessments, setAssessments] = useState(null);
  const [error, setError] = useState("");
  const [showTable, setShowTable] = useState(false);

  useEffect(() => {
    api
      .getHistory()
      .then((data) => setAssessments(data.assessments))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div>
      <div className="eyebrow">Your decision journal</div>
      <h1>See how your direction evolves.</h1>
      <p className="lede">
        Past answers are not a verdict. They are snapshots of who you were, what you needed, and
        what changed.
      </p>

      {error && <div className="banner error">{error}</div>}

      {assessments && assessments.length === 0 && (
        <div>
          <div className="banner info">No assessments yet. Your first result will appear here.</div>
          <Link to="/assessment" className="btn btn-primary">
            🧭 Take the assessment
          </Link>
        </div>
      )}

      {assessments && assessments.length > 0 && (
        <>
          <div className="metric-row">
            <div className="metric">
              <div className="label">Total check-ins</div>
              <div className="value">{assessments.length}</div>
            </div>
            <div className="metric">
              <div className="label">Latest direction</div>
              <div className="value" style={{ fontSize: "1.1rem" }}>
                {assessments[0].primary_recommendation}
              </div>
            </div>
            <div className="metric">
              <div className="label">Latest readiness</div>
              <div className="value">{assessments[0].readiness_score}</div>
            </div>
          </div>

          <h3>Assessment timeline</h3>
          {assessments.map((row) => (
            <details className="expander" key={row.id}>
              <summary>
                <span>
                  {String(row.created_at).slice(0, 16)} · {row.primary_recommendation} ·{" "}
                  {row.career_path}
                </span>
                <span style={{ color: "var(--muted)" }}>▾</span>
              </summary>
              <div className="expander-body">
                <div className="metric-row">
                  <div className="metric">
                    <div className="label">Risk</div>
                    <div className="value">{row.risk_score}</div>
                  </div>
                  <div className="metric">
                    <div className="label">Financial</div>
                    <div className="value">{row.financial_score}</div>
                  </div>
                  <div className="metric">
                    <div className="label">Leadership</div>
                    <div className="value">{row.leadership_score}</div>
                  </div>
                  <div className="metric">
                    <div className="label">Readiness</div>
                    <div className="value">{row.readiness_score}</div>
                  </div>
                </div>
                <p>
                  <strong>Context:</strong> {row.education} · {row.current_status} ·{" "}
                  {row.experience} years experience
                </p>
                <p style={{ color: "var(--muted)", fontSize: "0.88rem" }}>
                  Secondary direction: {row.secondary_recommendation}
                </p>
              </div>
            </details>
          ))}

          <details className="expander" open={showTable} onToggle={(e) => setShowTable(e.target.open)}>
            <summary>
              <span>View as table</span>
              <span style={{ color: "var(--muted)" }}>▾</span>
            </summary>
            <div className="expander-body table-wrap">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Name</th>
                    <th>Primary</th>
                    <th>Alternative</th>
                    <th>Career path</th>
                    <th>Readiness</th>
                  </tr>
                </thead>
                <tbody>
                  {assessments.map((row) => (
                    <tr key={row.id}>
                      <td>{String(row.created_at).slice(0, 16)}</td>
                      <td>{row.name}</td>
                      <td>{row.primary_recommendation}</td>
                      <td>{row.secondary_recommendation}</td>
                      <td>{row.career_path}</td>
                      <td>{row.readiness_score}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </details>
        </>
      )}
    </div>
  );
}
