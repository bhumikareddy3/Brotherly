import { createContext, useContext, useState } from "react";

const AppContext = createContext(null);

export function AppProvider({ children }) {
  // Mirrors what Streamlit kept in st.session_state: the latest
  // assessment result (used to give the mentor context) and the
  // in-progress chat thread.
  const [assessment, setAssessment] = useState(null); // { primary, secondary, career_path, scores, profile, plan, name }
  const [messages, setMessages] = useState([]); // [{ role, content }]

  const assessmentContext = assessment
    ? {
        primary: assessment.primary,
        secondary: assessment.secondary,
        career_path: assessment.career_path,
        scores: assessment.scores,
        profile: assessment.profile,
      }
    : null;

  return (
    <AppContext.Provider
      value={{ assessment, setAssessment, messages, setMessages, assessmentContext }}
    >
      {children}
    </AppContext.Provider>
  );
}

export function useApp() {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useApp must be used within AppProvider");
  return ctx;
}
