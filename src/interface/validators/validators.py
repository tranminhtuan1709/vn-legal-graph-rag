from interface.dtos.external.request.retrieval_request import RetrievalRequest
from pydantic import ValidationError

def validate_retrival_request(request: RetrievalRequest) -> None:
    if request.request_id == "":
        raise ValidationError("request_id must not be empty")

    if request.query == "":
        raise ValidationError("query must not be empty")


def validate_query_params(
    n_doc: int,
    n_art: int,
    n_node: int,
    n_rr_node: int,
    n_rr_rel: int,
    rr_node_cutoff: int,
    rr_rel_cutoff: int,
    n_hop
) -> None:
    if not (
        n_doc >= 0 and
        n_art >= 0 and
        n_node >= -1 and
        n_rr_node > 0 and
        n_rr_rel >= -1 and
        0 <= rr_node_cutoff <= 1 and
        0 <= rr_rel_cutoff <= 1 and
        (n_hop == -1 or n_hop >= 1)
    ):
        raise ValidationError("Invalid parameters")
