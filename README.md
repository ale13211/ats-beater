# ATS Beater

[![Live demo](https://img.shields.io/badge/live%20demo-Vercel-black?logo=vercel)](https://ats-beater-ebon.vercel.app)
[![API](https://img.shields.io/badge/API-Render-46E3B7?logo=render&logoColor=white)](https://ats-beater-api.onrender.com/api/health/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**[Open the live demo →](https://ats-beater-ebon.vercel.app)**

## Why I built this

I built ATS Beater to explore a practical problem: when a resume is compared with a job description, it should be possible to understand *why* the result looks the way it does.

The application compares a resume with a job description and shows the recognized skills, potential gaps and the calculation behind the percentage. I intentionally kept the matching engine deterministic instead of presenting an opaque score as if it were a commercial ATS or a hiring prediction.

## What I worked on

- A React + TypeScript interface for entering resume and job-description content.
- PDF text extraction, with pasted text as a simpler fallback.
- A Django REST API with input validation and a health endpoint.
- A small, explicit skill taxonomy with aliases such as `Postgres` → `PostgreSQL` and `unit testing` → `testing`.
- A score based on recognized job skills found in the resume.
- Matched skills, missing skills and recommendations based on the result.
- A previous/current comparison in the same browser session.
- Dockerized local development and backend tests with pytest.
- A split deployment: Vercel for the frontend and Render for the API.

## Technical decisions

The core matching logic lives in `backend/analyzer/services.py`. It normalizes text, checks aliases with word boundaries and returns structured data for the frontend. Keeping this logic separate from the API view makes it easy to test and extend.

I chose a transparent rule-based approach for this version because it is easier to explain, test and debug than a black-box score. The trade-off is that the current taxonomy does not understand every possible synonym or the quality of a resume bullet. A future version could add weighted phrases or an optional NLP layer while keeping the current result explanation visible to the user.

## How it works

1. The user uploads a text-based PDF or pastes resume text.
2. The user adds a job description.
3. The API extracts recognized skills from both texts.
4. The frontend displays the score, matched skills, missing skills and recommendations.

The score is calculated as:

```text
matched recognized job skills / total recognized job skills × 100
```

It is a keyword-coverage indicator for this project, not a prediction of interview invitations or hiring outcomes.

## Live deployment

- Frontend: [ats-beater-ebon.vercel.app](https://ats-beater-ebon.vercel.app)
- API health check: [ats-beater-api.onrender.com/api/health/](https://ats-beater-api.onrender.com/api/health/)

The public demo runs the backend on Render's free web service with SQLite. Resumes are processed in memory, and the demo does not persist resumes or analysis results. For a production setup, I would add PostgreSQL, rate limiting, monitoring, stronger file validation and a privacy policy.

## Run locally

### Docker

```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- API health: http://localhost:8000/api/health/
- Analyze endpoint: `POST http://localhost:8000/api/analyze/`

Load the example data in the interface and click **Analyze match** to try the complete flow.

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
backend/     Django REST API, matching logic and tests
frontend/    React + TypeScript interface
render.yaml  Render deployment configuration
```

## Next improvements

- Add bilingual UI and skill-taxonomy administration.
- Support weighted phrases and seniority/context instead of only skill presence.
- Add browser end-to-end tests and accessibility checks.
- Add explicit-consent analysis history and production-grade file scanning.

## License

MIT
