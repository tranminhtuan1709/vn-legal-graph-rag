from fastapi import Depends

from infrastructure.neo4j_client import Neo4jClient
from dependencies import get_neo4j_client
from interface.dtos.internal.traversal_policy import TraversalPolicy
from exceptions import GraphTraversalError


class GraphRepository:
    def __init__(self, neo4j_client: Neo4jClient = Depends(get_neo4j_client)) -> None:
        self.neo4j_client = neo4j_client
    
    def traverse_graph(self, starting_node_ids: list[str], traversal_policy: TraversalPolicy):
        if (
            len(starting_node_ids) == 0 or
            len(traversal_policy.allowed_edge_types) == 0 or
            traversal_policy.n_node == 0
        ):
            return []
        
        session = self.neo4j_client.get_session()
        transaction = None

        try:
            transaction = session.begin_transaction()
            
            hop_clause: str

            if traversal_policy.n_hop == -1:
                hop_clause = "*1.."
            else:
                hop_clause = "*1..$n_hop"
            
            edge_type_clause = "|".join(traversal_policy.allowed_edge_types)

            query = f"""
                MATCH (start:Article)
                WHERE start.node_id IN $starting_node_ids

                MATCH path = (start)-[r:{edge_type_clause}{hop_clause}]-(n:Article)

                WITH
                    collect(DISTINCT start) + collect(DISTINCT n) AS all_nodes,
                    collect(r) AS rels

                WITH
                    all_nodes[0..$n_node] AS limited_nodes,
                    rels

                RETURN
                [
                    node IN limited_nodes |
                    {
                        id: node.node_id,
                        labels: labels(node),
                        properties: properties(node)
                    }
                ] AS nodes,

                [
                    rel IN rels |
                    {
                        from: startNode(rel).node_id,
                        to: endNode(rel).node_id,
                        type: type(rel),
                        properties: properties(rel)
                    }
                ] AS edges
            """
        
            transaction.run()
            transaction.commit()
        except Exception as e:
            if transaction is not None:
                transaction.rollback()
                
            raise GraphTraversalError(
                message="Failed to perform graph traversal",
                context={
                    "num_starting_nodes": len(starting_node_ids),
                    "n_hops": traversal_policy.n_hop,
                    "n_nodes": traversal_policy.n_node,
                    "prioritized_relationships": traversal_policy.allowed_edge_types
                }
            ) from e
        finally:
            if transaction is not None:
                transaction.close()
            
            if session is not None:
                session.close()
