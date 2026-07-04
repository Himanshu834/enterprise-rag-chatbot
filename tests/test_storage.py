from app.storage import JsonDocumentStore


def test_json_document_store_persists_documents(tmp_path):
    store_path = tmp_path / "documents.json"
    store = JsonDocumentStore(str(store_path))

    store.save_document({"filename": "sample.txt", "text": "hello world", "chunks": ["hello world"]})

    reloaded = JsonDocumentStore(str(store_path))
    documents = reloaded.list_documents()

    assert len(documents) == 1
    assert documents[0]["filename"] == "sample.txt"
