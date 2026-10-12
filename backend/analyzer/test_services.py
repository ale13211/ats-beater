from analyzer.services import analyze, extract_skills

def test_synonyms():
    assert "postgresql" in extract_skills("Experience with Postgres.")

def test_score():
    result = analyze("Python, Docker", "Python, Docker, Redis")
    assert result["score"] == 66.7
    assert result["missing"] == ["redis"]

def test_empty_job_skills():
    assert analyze("Python", "Excellent communication")["score"] == 0
