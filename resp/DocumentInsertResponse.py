from pydantic import BaseModel


class DocumentInsertResponse(BaseModel):
    success: bool = False
    seq_no: int = None
