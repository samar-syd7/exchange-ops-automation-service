from datetime import datetime, timedelta
from fastapi.testclient import TestClient
from app.main import app

def test_missed_daily_job_detected():
    client = TestClient(app)

    response = client.get("/api/health/")
    data = response.json()

    # If no job ran today, system should detect it
    assert "missed_daily_reconciliation" in data