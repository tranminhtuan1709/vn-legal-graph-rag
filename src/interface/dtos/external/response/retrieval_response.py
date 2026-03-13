from pydantic import BaseModel
from typing import Any


class RetrievalResponse(BaseModel):
    execution_time: int
    total_result: int
    total_token: int
    results: list[dict[str, Any]]
