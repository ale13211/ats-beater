# ATS Beater — Resume Match Analyzer

A portfolio-ready full-stack MVP for comparing a resume with a job description.
Built with **Django REST Framework, PostgreSQL, React, TypeScript, Docker**.

> This is an educational keyword coverage tool, **not** a replica of proprietary ATS software.
> It does not predict interview invitations or hiring outcomes.

## Quick start

Requires Docker and Docker Compose.

```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- API health: http://localhost:8000/api/health/
- API endpoint: `POST http://localhost:8000/api/analyze/`

Click **Load example**, then **Analyze match**. Edit the CV and analyze again to compare scores.

## API example

```bash
curl -X POST http://localhost:8000/api/analyze/ \
  -F 'resume_text=Python Docker PostgreSQL' \
  -F 'job_description=Python Docker PostgreSQL Redis AWS'
```

You can send `resume_file=@resume.pdf` instead of `resume_text`.

## Testing

```bash
cd backend
pip install -r requirements.txt
pytest -q
```

## Public demo deployment

**Option:** Render Python web service + Vercel static frontend.
- The included `render.yaml` uses the app's SQLite fallback so the demo can run on
  Render's free web service without requiring billing details. The analyzer does not
  persist resumes or results. For a persistent production setup, add PostgreSQL and
  set `DATABASE_URL` to its connection string.
- Deploy backend with root directory `backend`, build `pip install -r requirements.txt`,
  start `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`.
- Set `SECRET_KEY` (long random string), `DEBUG=false`, `ALLOWED_HOSTS` to backend hostname,
  `DATABASE_URL` to hosted PostgreSQL, `CORS_ALLOWED_ORIGINS` to your frontend HTTPS URL.
- Deploy frontend with root directory `frontend`, build `npm run build`, output `dist`.
- Set `VITE_API_URL` to `https://YOUR-BACKEND/api/analyze/` at **build time**.
- Verify upload and sample analysis in the public URL. Free tiers and pricing change;
  review provider terms before deploying.

The backend does **not** persist resumes. Uploaded files are processed in memory.
For public use, add throttling, stronger file validation, monitoring, abuse prevention,
a privacy policy, and resource limits. Scanned PDFs without a text layer are unsupported.

## Current scope

- PDF or pasted resume text; job description text.
- Curated skill aliases and transparent percentage of job skills found in CV.
- Matched/missing skill lists, actionable conditional recommendations.
- Before/after comparison in current browser session (not persisted).
- English UI and sample data.

## Roadmap

- Bilingual UI (English/Spanish), i18n.
- spaCy-based phrase extraction and weighted skill scoring.
- Optional account-based analysis history with explicit consent.
- Accessibility audit and browser E2E tests.
- Rate limiting and production-grade file scanning.

## Portfolio pitch

**ATS Beater** — Full-stack resume-to-job matching application using DRF,
PostgreSQL, React and TypeScript. Built a transparent keyword matching engine,
PDF extraction, responsive dashboard, automated CI tests and Dockerized development.

## License

MIT

## Deployment configuration included

`render.yaml` defines a Render backend and PostgreSQL Blueprint; `frontend/vercel.json` configures Vercel frontend output. After deploying, set `ALLOWED_HOSTS` to the actual Render hostname, `CORS_ALLOWED_ORIGINS` to the actual Vercel origin and `VITE_API_URL` in Vercel to the complete Render API endpoint, then redeploy the frontend. Deployments are **not automatic** from this ZIP; they require connecting your GitHub account to the providers. See `PORTFOLIO_INTEGRATION.md` for a portfolio entry.
