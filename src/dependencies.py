import os
from fastapi import Depends

from infrastructure.neo4j_client import Neo4jClient
from infrastructure.elasticsearch_client import ElasticsearchClient
from infrastructure.llm_client import LLMClient

from repositories.graph_repository import GraphRepository
from repositories.vector_repository import VectorRepository
from repositories.llm_repository import LLMRepository

from services.retrieval_service import RetrievalService


def get_neo4j_client() -> Neo4jClient:
    return Neo4jClient(
        host=os.getenv("NEO4J_HOST"),
        port=int(os.getenv("NEO4J_PORT")),
        username=os.getenv("NEO4J_USERNAME"),
        password=os.getenv("NEO4J_PASSWORD"),
        database=os.getenv("NEO4J_DATABASE"),
        connection_timeout=int(os.getenv("NEO4J_CONNECTION_TIMEOUT")),
        max_connection_pool_size=int(os.getenv("NEO4J_MAX_CONNECTION_POOL_SIZE"))
    )


def get_elasticsearch_client() -> ElasticsearchClient:
    return ElasticsearchClient(
        host=os.getenv("ELASTICSEARCH_HOST"),
        port=int(os.getenv("ELASTICSEARCH_PORT")),
        username=os.getenv("ELASTICSEARCH_USERNAME"),
        password=os.getenv("ELASTICSEARCH_PASSWORD"),
        request_timeout=int(os.getenv("ELASTICSEARCH_REQUEST_TIMEOUT"))
    )


def get_llm_client() -> LLMClient:
    return LLMClient()


def get_graph_repository(neo4j_client: Neo4jClient = Depends(get_neo4j_client)):
    return GraphRepository(neo4j_client)


def get_vector_repository(elasticsearch_client: ElasticsearchClient = Depends(get_elasticsearch_client)):
    return VectorRepository(elasticsearch_client)


def get_llm_repository(llm_client: LLMClient = Depends(get_llm_client)):
    return LLMRepository(llm_client)


def get_retrieval_service(
    graph_repository: GraphRepository = Depends(get_graph_repository),
    vector_repository: VectorRepository = Depends(get_vector_repository),
    llm_repository: LLMRepository = Depends(get_llm_repository)
):
    return RetrievalService(graph_repository, vector_repository, llm_repository)
