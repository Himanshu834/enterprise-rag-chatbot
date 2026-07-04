from fastapi import FastAPI, UploadFile, File

from app.schemas import ChatRequest, ChatResponse, DocumentUploadResponse
from app.storage import JsonDocumentStore

app = FastAPI(title="Enterprise RAG Chatbot", version="0.1.0")

app.state.document_store = JsonDocumentStore()


def _chunk_text(text: str, chunk_size: int = 200) -> list[str]:
    words = text.split()
    chunks: list[str] = []
    for index in range(0, len(words), chunk_size):
        chunk = " ".join(words[index : index + chunk_size])
        if chunk:
            chunks.append(chunk)
    return chunks or [text]


def _search_documents(question: str) -> list[str]:
    matches: list[str] = []
    keywords = {
        term.lower().strip(".,!?;:\"'()[]{}")
        for term in question.split()
        if term.lower().strip(".,!?;:\"'()[]{}")
    }

    for document in app.state.document_store.list_documents():
        text = str(document["text"]).lower()
        if any(keyword in text for keyword in keywords):
            matches.extend(document["chunks"])
    return matches


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Enterprise RAG chatbot API is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    matches = _search_documents(request.question)
    if matches:
        answer = "I found relevant information: " + " ".join(matches[:2])
        return ChatResponse(answer=answer, sources=["uploaded-documents"])

    return ChatResponse(
        answer="This is a starter response. Connect your retrieval pipeline to return grounded answers.",
        sources=["starter-docs"],
    )


@app.post("/documents/upload", response_model=DocumentUploadResponse)
def upload_document(file: UploadFile = File(...)) -> DocumentUploadResponse:
    content = file.file.read().decode("utf-8", errors="ignore")
    chunks = _chunk_text(content)
    app.state.document_store.save_document({"filename": file.filename, "text": content, "chunks": chunks})
    return DocumentUploadResponse(filename=file.filename or "unknown", chunks=len(chunks))
