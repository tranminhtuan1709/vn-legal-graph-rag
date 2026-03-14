from interface.dtos.external.request.retrieval_request import RetrievalRequest
from pydantic import ValidationError

def validate_retrival_request(request: RetrievalRequest) -> None:
    if request.request_id == "":
        raise ValidationError("request_id must not be empty")

    if request.query == "":
        raise ValidationError("query must not be empty")
