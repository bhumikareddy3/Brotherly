import { Link } from "react-router-dom";
import logo from "../assets/logo.png";

const CARDS = [
  {
    icon: "◎",
    title: "Understand your signal",
    copy: "Turn your experience, finances, risk appetite, and work style into a clear profile.",
  },
  {
    icon: "↗",
    title: "Choose a realistic path",
    copy: "Compare job, business, and hybrid directions through the lens of your actual circumstances.",
  },
  {
    icon: "✓",
    title: "Leave with a plan",
    copy: "Get a focused 30-day roadmap and keep refining it with your AI mentor.",
  },
];

export default function Home() {
  return (
    <div>
      <div className="two-col" style={{ alignItems: "center", marginBottom: "1rem" }}>
        <div>
          <img src={logo} alt="Brotherly" style={{ width: 56, height: 56, marginBottom: "1rem" }} />
          <div className="eyebrow">Career clarity, without the noise</div>
          <h1>A clearer next move starts with an honest conversation.</h1>
          <p className="lede">
            Brotherly combines a structured career assessment with grounded AI mentorship —
            so you can choose between a job, business, or a hybrid path with confidence.
          </p>
          <div style={{ display: "flex", gap: "0.9rem", marginTop: "1.5rem", flexWrap: "wrap" }}>
            <Link to="/assessment" className="btn btn-primary">
              🧭 Start assessment
            </Link>
            <Link to="/mentor" className="btn btn-secondary">
              💬 Talk to your mentor
            </Link>
          </div>
        </div>
        <div className="surface" style={{ transform: "rotate(1.5deg)" }}>
          <div className="eyebrow">A note from Brotherly</div>
          <h3 style={{ fontSize: "1.35rem" }}>You don't need your whole life figured out.</h3>
          <p>You only need enough clarity for the next honest step. We'll find that step together.</p>
          <div style={{ marginTop: "1.2rem", color: "var(--green)", fontWeight: 700 }}>
            No hype. No generic advice. →
          </div>
        </div>
      </div>

      <div className="hero-rule" />
      <h2>Built for decisions that feel personal</h2>
      <p style={{ color: "var(--muted)" }}>A thoughtful process from uncertainty to a practical plan.</p>

      <div className="card-grid">
        {CARDS.map((card) => (
          <div className="surface" key={card.title}>
            <div className="icon">{card.icon}</div>
            <h3>{card.title}</h3>
            <p>{card.copy}</p>
          </div>
        ))}
      </div>

      <div className="quote-card">
        <strong>Brotherly won't predict your future.</strong> It helps you make a better decision
        with the information you have today.
      </div>
    </div>
  );
}
