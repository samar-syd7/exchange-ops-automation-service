from fastapi.testclient import TestClient
from app.main import app

def test_health_endpoint_returns_ok():
    client = TestClient(app)

    response = client.get("/api/health/")
    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert "database" in data
    assert "last_successful_job_run" in data
    assert "missed_daily_reconciliation" in data