from fastapi import FastAPI
from pydantic import BaseModel


class OpensearchVectorDocumentV1(BaseModel):
    text: str | None = None
