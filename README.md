# 🤖 Brotherly AI Mentor

Brotherly is an AI-powered career mentor combining a structured **career assessment**,
**Retrieval-Augmented Generation (RAG)**, and an **LLM** to give personalized, grounded
career guidance.

This version has been rebuilt as a **FastAPI backend + React (Vite) frontend**,
replacing the original Streamlit app. All the assessment scoring, recommendation logic,
and RAG/mentor pipeline are unchanged — only the presentation layer moved from
Streamlit to a REST API + SPA.

---

## Project structure

```
brotherly-app/
├── backend/            FastAPI app
│   ├── main.py          REST endpoints (assessment, dashboard, history, mentor chat)
│   ├── ai/               Mentor orchestration + LLM client (NVIDIA API)
│   ├── database/         SQLite persistence (assessments, chats)
│   ├── recommendation/   Scoring, rules, career paths, action plans (pure functions)
│   ├── rag/               Ingestion pipeline + retrieval (ChromaDB, sentence-transformers)
│   └── knowledge_base/    Source PDFs/markdown for the RAG knowledge base
└── frontend/            Vite + React app
    ├── src/pages/          Home, Assessment, Mentor, Dashboard, History, Conversations
    ├── src/context/        Shared assessment/chat state (replaces st.session_state)
    └── src/api.js           Fetch client for the backend
```

---

## Running the backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # then add your NVIDIA_API_KEY
uvicorn main:app --reload --port 8000
```

The API boots and serves the assessment/dashboard/history endpoints even without an
API key configured — only the `/api/mentor/chat` endpoint needs `NVIDIA_API_KEY` (and a
built knowledge base) to work.

### Building the knowledge base (optional, for RAG)

The `rag/data/` directory ships with a pre-built Chroma index. If you update the PDFs in
`knowledge_base/`, rebuild it with:

```bash
python rag/ingestion/pipeline.py
```

---

## Running the frontend

```bash
cd frontend
npm install
cp .env.example .env    # defaults to http://localhost:8000, change if needed
npm run dev
```

Open the printed local URL (typically `http://localhost:5173`). The frontend talks to
the backend over `VITE_API_BASE` (CORS is already enabled on the backend for local dev).

---

## API endpoints

| Method | Path                | Description                                      |
|--------|---------------------|---------------------------------------------------|
| POST   | `/api/assessment`   | Submit assessment answers, get scores + plan       |
| GET    | `/api/dashboard`    | Latest assessment + aggregate stats                |
| GET    | `/api/history`      | All past assessments                               |
| POST   | `/api/mentor/chat`  | Send a message to the AI mentor, get a reply        |
| GET    | `/api/chats`        | All saved mentor conversations                      |
| GET    | `/api/health`       | Health check                                       |

---

## What changed from the Streamlit version

- Streamlit's `pages/*.py` (rendered server-side) are replaced by React pages that call
  the FastAPI endpoints above.
- `st.session_state` (assessment result + chat thread) is replaced by a small React
  context (`src/context/AppContext.jsx`).
- `ai/config.py` no longer depends on `st.secrets` — it just reads `.env`/environment
  variables.
- The OpenAI client and the Chroma retriever used to be created at import time, which
  meant the whole app would crash on startup without an `NVIDIA_API_KEY` or without
  `chromadb`/`sentence-transformers` installed. Both are now created lazily, so the API
  boots and the assessment/dashboard/history features work regardless — only the mentor
  chat feature needs them.
- Dashboard/history data access now goes through small JSON-friendly helpers in
  `database/db.py` instead of `pandas.read_sql_query` (pandas is no longer a dependency).

## Authentication

Accounts and login are now built in — every user only sees their own assessments and
mentor conversations.

**Backend (new files/changes):**
- `backend/auth.py` — password hashing (bcrypt) and JWT creation/verification
- `backend/database/db.py` — added a `users` table; `assessments` and `chats` now carry
  a `user_id` and every query is scoped to the logged-in user
- `backend/main.py` — added `POST /api/auth/register`, `POST /api/auth/login`,
  `GET /api/auth/me`, and a `get_current_user` dependency that protects
  `/api/assessment`, `/api/dashboard`, `/api/history`, `/api/mentor/chat`, `/api/chats`
- `backend/requirements.txt` — added `pyjwt`, `bcrypt`, `pydantic[email]`
- `backend/.env.example` — added `JWT_SECRET` (generate a real one for production with
  `python -c "import secrets; print(secrets.token_hex(32))"`)

**Frontend (new files/changes):**
- `src/pages/Login.jsx`, `src/pages/Register.jsx` — new auth pages
- `src/context/AuthContext.jsx` — holds the logged-in user, wraps login/register/logout,
  and auto-restores a session from a saved token on page load
- `src/components/ProtectedRoute.jsx` — redirects to `/login` when logged out
- `src/api.js` — attaches `Authorization: Bearer <token>` to every request; clears the
  session and notifies the app if a request comes back `401`
- `src/App.jsx` — added `/login` and `/register` routes; every other route is now
  wrapped in `ProtectedRoute`
- `src/components/Layout.jsx` — sidebar now shows the logged-in user's name and a
  log-out button

A JWT is issued on register/login, stored in the browser's `localStorage`, and sent on
every API call. There's no email verification or password reset flow — add one before
using this in production.

## Branding

The sidebar, login/register pages, and homepage now use the Brotherly logo
(`frontend/src/assets/logo.png`), and the browser tab icon is set from
`frontend/public/favicon.png`. Swap either file to change the branding.

## Tech stack

- **Backend:** FastAPI, Pydantic, SQLite, ChromaDB, sentence-transformers, OpenAI SDK
  (pointed at NVIDIA's API), PyJWT, bcrypt
- **Frontend:** React 19, Vite, React Router

## Deploying

See [`DEPLOY.md`](./DEPLOY.md) for a full walkthrough of deploying the backend to
Render and the frontend to Vercel, including CORS setup and a note on Render's
resource requirements for this app.
