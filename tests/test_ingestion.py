from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_upload_and_query_document():
    app.state.document_store.clear()

    response = client.post(
        "/documents/upload",
        files={"file": ("sample.txt", b"The quick brown fox jumps over the lazy dog.", "text/plain")},
    )

    assert response.status_code == 200
    assert response.json()["filename"] == "sample.txt"
    assert response.json()["chunks"] >= 1

    chat_response = client.post(
        "/chat",
        json={"question": "What animal jumps over the lazy dog?"},
    )

    assert chat_response.status_code == 200
    answer = chat_response.json()["answer"].lower()
    assert "fox" in answer
