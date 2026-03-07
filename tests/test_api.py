from fastapi.testclient import TestClient
from src.api.app import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_predict():
    payload = {
        "client_id": 1,
        "age": 30,
        "tenure_days": 100,
        "n_products": 1,
        "sum_amount": 100,
        "mean_amount": 100
    }
    r = client.post("/predict", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "score" in data
