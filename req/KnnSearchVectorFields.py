from pydantic import BaseModel


class KnnSearchVectorFields(BaseModel):
    vector: list
    k: int
