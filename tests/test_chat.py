from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_chat_endpoint_returns_placeholder_response():
    response = client.post(
        "/chat",
        json={"question": "What is this project about?"},
    )
    assert response.status_code == 200
    assert "starter response" in response.json()["answer"].lower()
