from fastapi import Depends

from repositories.graph_repository import GraphRepository
from repositories.vector_repository import VectorRepository

from interface.dtos.external.response.retrieval_response import RetrievalResponse
from dependencies import get_graph_repository, get_vector_repository


class RetrievalService:
    def __init__(
        self,
        graph_repository: GraphRepository = Depends(get_graph_repository),
        vector_repository: VectorRepository = Depends(get_vector_repository)
    ) -> None:
        self.graph_repository = graph_repository
        self.vector_repository = vector_repository
    
    def retrieve(self, query: str) -> RetrievalResponse:
        pass
