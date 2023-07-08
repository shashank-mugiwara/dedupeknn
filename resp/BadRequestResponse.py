from pydantic import BaseModel


class BadRequestResponse(BaseModel):
    message: str = None
