from pydantic import BaseModel


class RetrievalRequest(BaseModel):
    request_id: str
    query: str
