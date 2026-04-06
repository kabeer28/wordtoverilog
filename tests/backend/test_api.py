from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_generate_endpoint_returns_contract() -> None:
    response = client.post("/api/v1/generate", json={"description": "2-input and gate"})
    assert response.status_code == 200
    data = response.json()
    assert "verilog_code" in data
    assert "metadata" in data
    assert "diagnostics" in data
