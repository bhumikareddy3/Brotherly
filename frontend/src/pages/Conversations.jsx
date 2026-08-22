import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { api } from "../api";

export default function Conversations() {
  const [chats, setChats] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api
      .getChats()
      .then((data) => setChats(data.chats))
      .catch((err) => setError(err.message));
  }, []);

  return (
    <div>
      <div className="eyebrow">Conversation archive</div>
      <h1>Advice worth returning to.</h1>
      <p className="lede">
        Revisit the questions you asked, the perspective you received, and the threads you may
        want to pick up again.
      </p>

      {error && <div className="banner error">{error}</div>}

      {chats && chats.length === 0 && (
        <div>
          <div className="banner info">No mentor conversations yet.</div>
          <Link to="/mentor" className="btn btn-primary">
            💬 Start a conversation
          </Link>
        </div>
      )}

      {chats && chats.length > 0 && (
        <>
          <p style={{ color: "var(--muted)" }}>
            {chats.length} saved conversation{chats.length !== 1 ? "s" : ""}
          </p>
          {chats.map((chat, i) => {
            const title =
              chat.user_message.length < 72
                ? chat.user_message
                : chat.user_message.slice(0, 69) + "…";
            return (
              <details className="expander" key={i}>
                <summary>
                  <span>
                    {String(chat.created_at).slice(0, 16)} · {title}
                  </span>
                  <span style={{ color: "var(--muted)" }}>▾</span>
                </summary>
                <div className="expander-body">
                  <p>
                    <strong>You asked</strong>
                  </p>
                  <p>{chat.user_message}</p>
                  <p>
                    <strong>Brotherly replied</strong>
                  </p>
                  <p style={{ whiteSpace: "pre-wrap" }}>{chat.ai_response}</p>
                </div>
              </details>
            );
          })}
        </>
      )}
    </div>
  );
}
