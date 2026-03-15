from fastapi import Depends

from infrastructure.neo4j_client import Neo4jClient
from infrastructure.voyage_client import VoyageClient

from repositories.graph_repository import GraphRepository
from repositories.vector_repository import VectorRepository

from services.retrieval_service import RetrievalService


def get_neo4j_client() -> Neo4jClient:
    return Neo4jClient()


def get_voyage_client() -> VoyageClient:
    return VoyageClient()


def get_graph_repository(neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    return GraphRepository(neo4j_client)


def get_vector_repository(voyage_client: VoyageClient = Depends(get_voyage_client)):
    return VectorRepository(voyage_client)


def get_retrieval_service(
    graph_repository: GraphRepository = Depends(get_graph_repository),
    vector_repository: VectorRepository = Depends(get_vector_repository)
):
    return RetrievalService(graph_repository, vector_repository)
