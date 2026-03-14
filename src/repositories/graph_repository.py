from fastapi import Depends
from infrastructure.neo4j_client import Neo4jClient
from dependencies import get_neo4j_client
from interface.dtos.internal.traversal_policy import TraversalPolicy


class GraphRepository:
    def __init__(self, neo4j_client: Neo4jClient = Depends(get_neo4j_client)) -> None:
        self.neo4j_client = neo4j_client
    
    def traverse_graph(self, starting_node_ids: list[str], traversal_policy: TraversalPolicy):
        pass
