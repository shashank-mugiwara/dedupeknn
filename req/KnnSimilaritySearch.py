from pydantic import BaseModel


class KnnSimilaritySearch(BaseModel):
    text: str | None
    size: int
    k: int
    threshold: float
