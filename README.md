# ATS Beater — Resume Match Analyzer

[![Live demo](https://img.shields.io/badge/live%20demo-Vercel-black?logo=vercel)](https://ats-beater-ebon.vercel.app)
[![API](https://img.shields.io/badge/API-Render-46E3B7?logo=render&logoColor=white)](https://ats-beater-api.onrender.com/api/health/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

ATS Beater is a full-stack application that compares resume content with a job description and produces a transparent skill-coverage report.

**[Try the live demo →](https://ats-beater-ebon.vercel.app)**

## What it demonstrates

- React and TypeScript frontend with a responsive analysis dashboard.
- Django REST Framework API with validation and a health endpoint.
- PDF text extraction and pasted resume support.
- Curated skill aliases for clearer matching, including technologies such as Python, Django, Docker, AWS and PostgreSQL.
- Matched skills, missing skills, percentage score and actionable recommendations.
- Dockerized local development and automated backend tests with pytest.
- Separate production deployments: Vercel for the frontend and Render for the API.

## How it works

1. The user uploads a text-based PDF or pastes resume text.
2. The user adds a job description.
3. The API extracts and normalizes relevant skills.
4. The dashboard presents the score, matched skills, missing skills and recommendations.

The score is intentionally transparent: it represents the percentage of recognized job-description skills found in the resume. This is a portfolio project and keyword-coverage tool, not a replica of proprietary ATS software and not a predictor of hiring outcomes.

## Live deployment

- Frontend: [ats-beater-ebon.vercel.app](https://ats-beater-ebon.vercel.app)
- Backend health check: [ats-beater-api.onrender.com/api/health/](https://ats-beater-api.onrender.com/api/health/)

The public demo uses SQLite on Render's free web service and processes uploaded resumes in memory. It does not persist resumes or analysis results. A production setup can use PostgreSQL by providing `DATABASE_URL`, plus rate limiting, monitoring, stronger file validation and a privacy policy.

## Tech stack

**Frontend:** React, TypeScript, Vite, CSS  
**Backend:** Python, Django, Django REST Framework, pytest  
**Deployment:** Vercel, Render, Docker, Gunicorn  
**Optional production database:** PostgreSQL

## Run locally

### Docker

```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- API health: http://localhost:8000/api/health/
- Analyze endpoint: `POST http://localhost:8000/api/analyze/`

Load the example data in the UI and click **Analyze match** to see a complete result.

### Tests

```bash
cd backend
pip install -r requirements.txt
pytest -q
```

## API example

```bash
curl -X POST http://localhost:8000/api/analyze/ \
  -F 'resume_text=Python Docker PostgreSQL' \
  -F 'job_description=Python Docker PostgreSQL Redis AWS'
```

The API also accepts `resume_file=@resume.pdf` instead of `resume_text`.

## Project structure

```text
backend/     Django REST API, analysis engine and tests
frontend/    React + TypeScript interface
render.yaml  Render deployment configuration
```

## Scope and next steps

Current scope includes English UI, text-based PDF extraction, pasted resume text, skill aliases, transparent scoring and in-session comparison.

Potential next steps include bilingual support, weighted phrase extraction with spaCy, explicit-consent analysis history, browser E2E tests, rate limiting and production-grade file scanning.

## License

MIT
