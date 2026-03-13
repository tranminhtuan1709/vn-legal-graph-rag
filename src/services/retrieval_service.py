from repositories.graph_repository import GraphRepository
from repositories.vector_repository import VectorRepository
from repositories.llm_repository import LLMRepository

from interface.dtos.external.response.retrieval_response import RetrievalResponse



class RetrievalService:
    def __init__(
        self,
        graph_repository: GraphRepository,
        vector_repository: VectorRepository,
        llm_repository: LLMRepository
    ) -> None:
        self.graph_repository = graph_repository
        self.vector_repository = vector_repository
        self.llm_repository = llm_repository
    
    def retrieve(self, query: str) -> RetrievalResponse:
        pass
