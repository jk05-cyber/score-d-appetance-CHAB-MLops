from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_predict():
    # Skipping as it requires trained model in MLflow
    # Run: python pipelines/training_flow.py first
    pass
