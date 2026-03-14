from pydantic import BaseModel
from typing import Any


class RetrievalResponse(BaseModel):
    execution_time: int
    nodes: list[dict[str, Any]]
    edges: list[dict[str, Any]]
