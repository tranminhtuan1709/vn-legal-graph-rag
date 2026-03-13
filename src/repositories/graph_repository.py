from infrastructure.neo4j_client import Neo4jClient


class GraphRepository:
    def __init__(self, neo4j_client: Neo4jClient) -> None:
        self.neo4j_client = neo4j_client
    
    def traverse_graph(self, node_ids: list[str]):
        pass
