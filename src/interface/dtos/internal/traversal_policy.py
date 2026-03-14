from pydantic import BaseModel


class TraversalPolicy(BaseModel):
    n_hops: int
    n_nodes: int
    edge_types: list[str]
