from fastapi import Depends
from infrastructure.elasticsearch_client import ElasticsearchClient
from dependencies import get_elasticsearch_client


class VectorRepository:
    def __init__(self, elasticsearch_client: ElasticsearchClient = Depends(get_elasticsearch_client)) -> None:
        self.elasticsearch_client = elasticsearch_client
    
    def search_documents(self):
        pass

    def search_articles(self):
        pass
