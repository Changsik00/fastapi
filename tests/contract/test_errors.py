from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)

def test_404_handler():
    response = client.get("/non-existent-route")
    assert response.status_code == 404
    data = response.json()
    assert data["code"] == "NOT_FOUND"
    assert data["message"] == "The requested resource was not found"
    assert data["path"] == "/non-existent-route"
