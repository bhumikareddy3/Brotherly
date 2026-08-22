# Deploying Brotherly (Render + Vercel)

This deploys the FastAPI backend to **Render** and the React frontend to **Vercel**.
Total time: ~15-20 minutes, most of it waiting for the backend build (it installs
`torch` and `sentence-transformers`, which are large).

## Before you start — a real constraint to know about

This backend isn't a typical lightweight API:
- It loads an embedding model (`sentence-transformers`) and a Chroma vector database
  for the RAG mentor pipeline
- It persists user accounts, assessments, and chats to a SQLite file

That means:
- **Render's free tier (512MB RAM) will likely crash or fail to build.** Use at least
  the **Starter** plan ($7/mo). `render.yaml` below is already set to `starter`.
- SQLite needs a **persistent disk**, or your users/assessments vanish every time
  Render redeploys or restarts the service. `render.yaml` mounts one automatically.

If you want a truly free option instead, see "Alternative: keep it free" at the bottom.

---

## Part 1 — Push to GitHub

Commit and push the whole `brotherly-app` folder (both `backend/` and `frontend/`) to
your existing repo, if you haven't already:

```bash
git add .
git commit -m "Add auth, logo, and deploy configs"
git push
```

---

## Part 2 — Deploy the backend to Render

### Option A — Blueprint (recommended, uses the included `render.yaml`)

1. Go to [dashboard.render.com](https://dashboard.render.com) → **New +** → **Blueprint**
2. Connect your GitHub repo and select it
3. Render will detect `backend/render.yaml` and show you the `brotherly-api` service
   it's about to create — click **Apply**
4. Before the first deploy finishes, open the service → **Environment** and set:
   - `NVIDIA_API_KEY` — your key (required for the mentor chat to work)
   - `CORS_ORIGINS` — leave as-is for now; you'll update it after deploying the
     frontend in Part 3 (it needs your real Vercel URL)
   - `JWT_SECRET` — Render auto-generates this; leave it
5. Click **Manual Deploy → Deploy latest commit** if it didn't start automatically

### Option B — Manual setup (no Blueprint)

1. **New +** → **Web Service** → connect your repo
2. **Root Directory:** `backend`
3. **Runtime:** Python 3
4. **Build Command:**
   ```
   pip install --index-url https://download.pytorch.org/whl/cpu torch && pip install -r requirements.txt
   ```
5. **Start Command:**
   ```
   uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
6. **Instance Type:** Starter (or higher) — not Free
7. Add environment variables: `NVIDIA_API_KEY`, `JWT_SECRET` (any long random string),
   `CORS_ORIGINS` (fill in after Part 3), `PYTHON_VERSION=3.12.3`
8. Add a **Disk**: mount path `/opt/render/project/src/backend/database`, size 1GB
9. Click **Create Web Service**

### After it deploys

Render gives you a URL like `https://brotherly-api.onrender.com`. Test it:
```bash
curl https://brotherly-api.onrender.com/api/health
# should return {"status":"ok"}
```

Note: Starter-tier services on Render spin down after inactivity is *not* the case for
paid plans (only Free tier sleeps) — Starter stays warm.

---

## Part 3 — Deploy the frontend to Vercel

1. Go to [vercel.com/new](https://vercel.com/new) and import the same GitHub repo
2. **Root Directory:** `frontend`
3. Vercel auto-detects Vite — leave build command (`npm run build`) and output
   directory (`dist`) as default
4. Add an environment variable:
   - `VITE_API_BASE` = `https://brotherly-api.onrender.com` (your Render URL from
     Part 2, no trailing slash)
5. Click **Deploy**

Vercel gives you a URL like `https://brotherly-app.vercel.app`.

---

## Part 4 — Connect them (CORS)

Go back to Render → your `brotherly-api` service → **Environment** → set:
```
CORS_ORIGINS=https://brotherly-app.vercel.app
```
(use your actual Vercel URL). Save — Render will redeploy automatically.

If you later add a custom domain on Vercel, add it to `CORS_ORIGINS` too
(comma-separated, no spaces): `CORS_ORIGINS=https://brotherly.com,https://brotherly-app.vercel.app`

---

## Part 5 — Verify

1. Open your Vercel URL
2. Register a new account
3. Complete an assessment
4. Try the mentor chat (needs `NVIDIA_API_KEY` to be set correctly on Render)

If registration/login fails silently, open the browser console — a CORS error there
almost always means `CORS_ORIGINS` on Render doesn't exactly match your Vercel URL
(check for trailing slashes or `www.` mismatches).

---

## Alternative: keep it free

If cost is the priority over reliability:
- Deploy the backend on **Render's free tier** anyway, but disable the RAG/mentor
  pipeline (skip installing `chromadb`/`sentence-transformers`/`torch`, and make the
  `Retriever` import fail gracefully — it already does this). You'll lose grounded
  mentor answers but keep the assessment/dashboard/history features working within
  512MB RAM.
- Use **Render's free PostgreSQL** or accept that free-tier disks aren't persistent
  (your SQLite data resets on every redeploy/restart).
- The frontend on Vercel is free either way — that part doesn't change.
