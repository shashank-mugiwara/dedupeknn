from fastapi import FastAPI
from pydantic import BaseModel


class OpensearchVectorDocumentV1(BaseModel):
    index: str | None = None
    document_id: int
    text: str | None = None
