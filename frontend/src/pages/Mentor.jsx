import { useRef, useState } from "react";
import { api } from "../api";
import { useApp } from "../context/AppContext";

const STARTERS = [
  "Help me choose between two career paths",
  "Turn my recommendation into a weekly plan",
  "What am I overlooking in my current situation?",
];

export default function Mentor() {
  const { assessment, assessmentContext, messages, setMessages } = useApp();
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const inputRef = useRef(null);

  async function send(text) {
    const prompt = text.trim();
    if (!prompt || sending) return;

    setError("");
    setMessages((m) => [...m, { role: "user", content: prompt }]);
    setInput("");
    setSending(true);

    try {
      const data = await api.sendMentorMessage(prompt, assessmentContext);
      setMessages((m) => [...m, { role: "assistant", content: data.reply }]);
    } catch (err) {
      setError(
        "I couldn't reach the mentor service just now. Check the API key and connection, then try again."
      );
    } finally {
      setSending(false);
      inputRef.current?.focus();
    }
  }

  function handleSubmit(e) {
    e.preventDefault();
    send(input);
  }

  return (
    <div>
      <div className="eyebrow">Your private sounding board</div>
      <h1>Talk it through.</h1>
      <p className="lede">
        Ask about a decision, pressure-test an idea, or turn your recommendation into a
        practical next step.
      </p>

      {assessment ? (
        <div className="banner success">
          ✅ Assessment connected · {assessment.primary} · {assessment.career_path}
        </div>
      ) : (
        <div className="banner info">
          🧭 For more personal guidance, complete the assessment first. You can still start a
          conversation now.
        </div>
      )}

      {messages.length === 0 && (
        <div>
          <h3>A few good places to begin</h3>
          <div className="suggestion-row">
            {STARTERS.map((s) => (
              <button key={s} className="suggestion-btn" onClick={() => send(s)}>
                {s}
              </button>
            ))}
          </div>
        </div>
      )}

      <div className="chat-window">
        {messages.map((m, i) => (
          <div key={i} className={`chat-bubble ${m.role}`}>
            {m.content}
          </div>
        ))}
        {sending && (
          <div className="chat-bubble assistant">
            <span className="spinner" style={{ borderTopColor: "var(--green)", borderColor: "rgba(35,79,62,0.25)" }} />{" "}
            Thinking it through…
          </div>
        )}
      </div>

      {error && <div className="banner error">{error}</div>}

      <form onSubmit={handleSubmit} className="chat-input-row">
        <input
          ref={inputRef}
          type="text"
          placeholder="What's on your mind?"
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button type="submit" className="btn btn-primary" disabled={sending || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}
