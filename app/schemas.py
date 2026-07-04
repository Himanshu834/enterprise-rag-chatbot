from pydantic import BaseModel


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: list[str] = []


class DocumentUploadResponse(BaseModel):
    filename: str
    chunks: int
