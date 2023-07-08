from pydantic import BaseModel
from req import KnnSearchQuery


class KnnSearchV1(BaseModel):
    size: int
    query: KnnSearchQuery

