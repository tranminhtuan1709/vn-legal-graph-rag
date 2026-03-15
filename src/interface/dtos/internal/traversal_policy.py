from pydantic import BaseModel


class TraversalPolicy(BaseModel):
    n_hop: int
    n_node: int
    allowed_edge_types: list[str]
