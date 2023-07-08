from pydantic import BaseModel
from req import KnnSearchVectorFields


class KnnSearchIndex(BaseModel):
    dedupe_vector_nmslib: KnnSearchVectorFields

