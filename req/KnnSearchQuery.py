from pydantic import BaseModel
from req import KnnSearchIndex


class KnnSearchQuery(BaseModel):
    knn: KnnSearchIndex | None
