import json
from pathlib import Path
from typing import Any


class JsonDocumentStore:
    def __init__(self, store_path: str | None = None) -> None:
        self.store_path = Path(store_path or "data/documents.json")
        self.store_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.store_path.exists():
            self.store_path.write_text("[]", encoding="utf-8")

    def list_documents(self) -> list[dict[str, Any]]:
        return json.loads(self.store_path.read_text(encoding="utf-8"))

    def save_document(self, document: dict[str, Any]) -> None:
        documents = self.list_documents()
        documents.append(document)
        self.store_path.write_text(json.dumps(documents, indent=2), encoding="utf-8")

    def clear(self) -> None:
        self.store_path.write_text("[]", encoding="utf-8")
