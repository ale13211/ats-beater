import re
import unicodedata

# Transparent, extensible skill taxonomy. No claim of reproducing commercial ATS scoring.
SKILLS = {
    "python": ["python"], "django": ["django"], "django rest framework": ["drf", "django rest framework"],
    "fastapi": ["fastapi"], "postgresql": ["postgres", "postgresql"],
    "sql": ["sql"], "docker": ["docker"], "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services"], "azure": ["azure"],
    "git": ["git"], "ci/cd": ["ci/cd", "continuous integration", "github actions"],
    "redis": ["redis"], "rest api": ["rest api", "restful", "rest apis"],
    "typescript": ["typescript"], "react": ["react", "reactjs"],
    "testing": ["pytest", "unit testing", "automated testing", "tests automatizados"],
    "linux": ["linux"], "mongodb": ["mongodb", "mongo db"],
    "celery": ["celery"], "microservices": ["microservices", "microservicios"],
    "agile": ["agile", "scrum"], "javascript": ["javascript"],
}

def normalize(value):
    value = unicodedata.normalize("NFKD", value.casefold())
    return "".join(c for c in value if not unicodedata.combining(c))

def extract_skills(text):
    text = normalize(text)
    found = set()
    for skill, aliases in SKILLS.items():
        if any(re.search(r"(?<!\w)" + re.escape(normalize(alias)) + r"(?!\w)", text) for alias in aliases):
            found.add(skill)
    return found

def analyze(resume, job):
    expected = extract_skills(job)
    actual = extract_skills(resume)
    matched = sorted(expected & actual)
    missing = sorted(expected - actual)
    score = round(100 * len(matched) / len(expected), 1) if expected else 0
    return {
        "score": score, "matched": matched, "missing": missing,
        "job_skills": sorted(expected),
        "recommendations": [
            f"If you have real experience with {skill}, document it with a concrete achievement."
            for skill in missing
        ],
        "disclaimer": "Keyword coverage is an indicative metric, not a prediction of hiring or ATS performance.",
    }
