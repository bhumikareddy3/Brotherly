import { useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";
import { useApp } from "../context/AppContext";

const TABS = ["01 · Background", "02 · Finances", "03 · Risk", "04 · Work style", "05 · Motivation"];

const DEFAULTS = {
  name: "",
  education: "Bachelor's",
  experience: 1,
  age: 22,
  current_status: "Student",
  current_role: "",
  savings: "3-6 Months",
  dependents: "No",
  income_stability: 5,
  income_reduction: 5,
  financial_pressure: 5,
  risk_uncertainty: 5,
  risk_opportunity: 5,
  risk_failure: 5,
  risk_relocation: 5,
  risk_decision: 5,
  environment: "Balanced",
  leadership: "Sometimes",
  work_type: "Technical Work",
  self_discipline: 5,
  initiative: 5,
  interest: "Technology",
  priority: "Growth",
  long_term_goal: "Career Growth",
  built_project: "No",
  sold_service: "No",
};

const EXPLANATIONS = {
  "Job First": "Build stability, skills, and professional leverage before taking a larger bet.",
  "Business First": "Your readiness, initiative, and appetite for uncertainty support independent value creation.",
  "Hybrid Later": "Keep a stable base while testing opportunities through deliberate, low-risk experiments.",
};

function Field({ label, children, hint }) {
  return (
    <div className="field">
      <label>{label}</label>
      {children}
      {hint && <div className="field-hint">{hint}</div>}
    </div>
  );
}

function Slider({ value, onChange, min = 1, max = 10, help }) {
  return (
    <>
      <div className="slider-row">
        <input
          type="range"
          min={min}
          max={max}
          value={value}
          onChange={(e) => onChange(Number(e.target.value))}
        />
        <span className="slider-value">{value}</span>
      </div>
      {help && <div className="field-hint">{help}</div>}
    </>
  );
}

function PillRadio({ options, value, onChange }) {
  return (
    <div className="pill-group">
      {options.map((opt) => (
        <button
          type="button"
          key={opt}
          className={`pill${value === opt ? " selected" : ""}`}
          onClick={() => onChange(opt)}
        >
          {opt}
        </button>
      ))}
    </div>
  );
}

export default function Assessment() {
  const { assessment, setAssessment } = useApp();
  const [form, setForm] = useState(DEFAULTS);
  const [tab, setTab] = useState(0);
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState(assessment);

  const set = (key) => (value) => setForm((f) => ({ ...f, [key]: value }));
  const onInput = (key) => (e) => set(key)(e.target.value);
  const onNumber = (key) => (e) => set(key)(Number(e.target.value));

  async function handleSubmit(e) {
    e.preventDefault();
    if (!form.name.trim()) {
      setError("Please enter your name before generating your direction.");
      setTab(0);
      return;
    }
    setError("");
    setSubmitting(true);
    try {
      const data = await api.submitAssessment(form);
      setResult(data);
      setAssessment(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div>
      <div className="eyebrow">Career compass</div>
      <h1>Let's understand where you are.</h1>
      <p className="lede">
        Answer honestly — not aspirationally. There are no right answers here, only useful
        signals for your next move.
      </p>
      <div className="hero-rule" />

      <form onSubmit={handleSubmit} className="surface">
        <div className="tabs">
          {TABS.map((label, i) => (
            <button
              type="button"
              key={label}
              className={`tab-btn${tab === i ? " active" : ""}`}
              onClick={() => setTab(i)}
            >
              {label}
            </button>
          ))}
        </div>

        {tab === 0 && (
          <div>
            <h3>Start with your current reality</h3>
            <div className="two-col">
              <div>
                <Field label="Your name">
                  <input
                    type="text"
                    placeholder="What should we call you?"
                    value={form.name}
                    onChange={onInput("name")}
                  />
                </Field>
                <Field label="Highest education">
                  <select value={form.education} onChange={onInput("education")}>
                    {["High School", "Diploma", "Bachelor's", "Master's", "PhD"].map((o) => (
                      <option key={o}>{o}</option>
                    ))}
                  </select>
                </Field>
                <Field label={`Years of experience — ${form.experience}`}>
                  <input
                    type="range"
                    min={0}
                    max={20}
                    value={form.experience}
                    onChange={onNumber("experience")}
                    style={{ accentColor: "var(--green)" }}
                  />
                </Field>
              </div>
              <div>
                <Field label="Age">
                  <input
                    type="number"
                    min={16}
                    max={80}
                    value={form.age}
                    onChange={onNumber("age")}
                  />
                </Field>
                <Field label="Current status">
                  <select value={form.current_status} onChange={onInput("current_status")}>
                    {["Student", "Working Professional", "Freelancer", "Business Owner", "Unemployed"].map(
                      (o) => (
                        <option key={o}>{o}</option>
                      )
                    )}
                  </select>
                </Field>
                <Field label="Current role or field">
                  <input
                    type="text"
                    placeholder="e.g. Computer science student"
                    value={form.current_role}
                    onChange={onInput("current_role")}
                  />
                </Field>
              </div>
            </div>
          </div>
        )}

        {tab === 1 && (
          <div>
            <h3>How much room do you have to experiment?</h3>
            <div className="two-col">
              <div>
                <Field label="Savings runway">
                  <select value={form.savings} onChange={onInput("savings")}>
                    {["0-3 Months", "3-6 Months", "6-12 Months", "12+ Months"].map((o) => (
                      <option key={o}>{o}</option>
                    ))}
                  </select>
                </Field>
                <Field label="Do people financially depend on you?">
                  <PillRadio options={["Yes", "No"]} value={form.dependents} onChange={set("dependents")} />
                </Field>
                <div className="field">
                  <label>Income stability</label>
                  <Slider
                    value={form.income_stability}
                    onChange={set("income_stability")}
                    help="1 = very unstable, 10 = highly stable"
                  />
                </div>
              </div>
              <div>
                <div className="field">
                  <label>Comfort with temporary income reduction</label>
                  <Slider value={form.income_reduction} onChange={set("income_reduction")} />
                </div>
                <div className="field">
                  <label>Current financial pressure</label>
                  <Slider value={form.financial_pressure} onChange={set("financial_pressure")} />
                </div>
                <div className="banner info">
                  Financial constraints are context, not a judgment. They help us recommend the
                  right timing.
                </div>
              </div>
            </div>
          </div>
        )}

        {tab === 2 && (
          <div>
            <h3>Your relationship with uncertainty</h3>
            <div className="two-col">
              <div>
                <Field label="Comfort with uncertain outcomes">
                  <Slider value={form.risk_uncertainty} onChange={set("risk_uncertainty")} />
                </Field>
                <Field label="Leaving stability for a promising opportunity">
                  <Slider value={form.risk_opportunity} onChange={set("risk_opportunity")} />
                </Field>
                <Field label="Ability to recover from failure">
                  <Slider value={form.risk_failure} onChange={set("risk_failure")} />
                </Field>
              </div>
              <div>
                <Field label="Willingness to relocate">
                  <Slider value={form.risk_relocation} onChange={set("risk_relocation")} />
                </Field>
                <Field label="Deciding without complete certainty">
                  <Slider value={form.risk_decision} onChange={set("risk_decision")} />
                </Field>
              </div>
            </div>
          </div>
        )}

        {tab === 3 && (
          <div>
            <h3>The conditions where you do your best work</h3>
            <div className="two-col">
              <div>
                <Field label="Preferred environment">
                  <select value={form.environment} onChange={onInput("environment")}>
                    {["Structured", "Flexible", "Balanced"].map((o) => (
                      <option key={o}>{o}</option>
                    ))}
                  </select>
                </Field>
                <Field label="Do you enjoy leading people?">
                  <PillRadio
                    options={["Yes", "Sometimes", "No"]}
                    value={form.leadership}
                    onChange={set("leadership")}
                  />
                </Field>
                <Field label="Work that energizes you">
                  <select value={form.work_type} onChange={onInput("work_type")}>
                    {["Technical Work", "People Interaction", "Problem Solving", "Business Activities"].map(
                      (o) => (
                        <option key={o}>{o}</option>
                      )
                    )}
                  </select>
                </Field>
              </div>
              <div>
                <Field label="Self-discipline">
                  <Slider value={form.self_discipline} onChange={set("self_discipline")} />
                </Field>
                <Field label="Enjoyment of taking initiative">
                  <Slider value={form.initiative} onChange={set("initiative")} />
                </Field>
              </div>
            </div>
          </div>
        )}

        {tab === 4 && (
          <div>
            <h3>What pulls you forward?</h3>
            <div className="two-col">
              <div>
                <Field label="Primary interest">
                  <select value={form.interest} onChange={onInput("interest")}>
                    {["Technology", "Business", "Sales", "Design", "Operations"].map((o) => (
                      <option key={o}>{o}</option>
                    ))}
                  </select>
                </Field>
                <Field label="What matters most right now?">
                  <select value={form.priority} onChange={onInput("priority")}>
                    {["Stability", "Growth", "Freedom", "Wealth", "Impact"].map((o) => (
                      <option key={o}>{o}</option>
                    ))}
                  </select>
                </Field>
                <Field label="Biggest five-year goal">
                  <select value={form.long_term_goal} onChange={onInput("long_term_goal")}>
                    {["Career Growth", "Leadership", "Own Business", "Financial Freedom", "Work-Life Balance"].map(
                      (o) => (
                        <option key={o}>{o}</option>
                      )
                    )}
                  </select>
                </Field>
              </div>
              <div>
                <Field label="Built a project or side business?">
                  <PillRadio
                    options={["Yes", "No"]}
                    value={form.built_project}
                    onChange={set("built_project")}
                  />
                </Field>
                <Field label="Sold a product or service?">
                  <PillRadio
                    options={["Yes", "No"]}
                    value={form.sold_service}
                    onChange={set("sold_service")}
                  />
                </Field>
                <div className="banner info">
                  Your actions are often a stronger signal than your ambitions. Small experiments
                  count.
                </div>
              </div>
            </div>
          </div>
        )}

        {error && <div className="banner error">{error}</div>}

        <button type="submit" className="btn btn-primary btn-block" disabled={submitting} style={{ marginTop: "1rem" }}>
          {submitting ? <span className="spinner" /> : "Reveal my direction  →"}
        </button>
      </form>

      {result && (
        <div style={{ marginTop: "2.5rem" }}>
          <div className="hero-rule" />
          <h2>Your direction, {result.name}</h2>
          {result.warning && <div className="banner error">{result.warning}</div>}
          <div className="two-col" style={{ alignItems: "start" }}>
            <div>
              <div className="result-card">
                <div className="result-label">Primary recommendation</div>
                <div className="result-value">{result.primary}</div>
                <p>{EXPLANATIONS[result.primary] || "A personalized recommendation based on your assessment."}</p>
              </div>
              <p style={{ marginTop: "1rem" }}>
                <strong>Strong alternative:</strong> {result.secondary}
              </p>
              <p>
                <strong>Best-fit direction:</strong> {result.career_path}
              </p>
            </div>
            <div className="metric-row">
              <div className="metric">
                <div className="label">Risk</div>
                <div className="value">{result.scores.risk}/50</div>
              </div>
              <div className="metric">
                <div className="label">Financial</div>
                <div className="value">{result.scores.financial}/25</div>
              </div>
              <div className="metric">
                <div className="label">Leadership</div>
                <div className="value">{result.scores.leadership}/10</div>
              </div>
              <div className="metric">
                <div className="label">Readiness</div>
                <div className="value">{result.scores.readiness}</div>
              </div>
            </div>
          </div>

          <h3 style={{ marginTop: "1.75rem" }}>What your answers say</h3>
          {result.profile.map((item) => (
            <p key={item}>✓ &nbsp; {item}</p>
          ))}

          <h3 style={{ marginTop: "1.5rem" }}>Your next 30 days</h3>
          <div className="surface">
            {result.plan.map((item, i) => {
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

          <div style={{ display: "flex", gap: "0.9rem", marginTop: "1.5rem", flexWrap: "wrap" }}>
            <Link to="/mentor" className="btn btn-secondary">
              💬 Discuss with mentor
            </Link>
            <Link to="/dashboard" className="btn btn-secondary">
              📊 Open dashboard
            </Link>
          </div>
        </div>
      )}
    </div>
  );
}
