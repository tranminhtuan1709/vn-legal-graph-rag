from infrastructure.elasticsearch_client import ElasticsearchClient


class VectorRepository:
    def __init__(self, elasticsearch_client: ElasticsearchClient) -> None:
        self.elasticsearch_client = elasticsearch_client
    
    def search_documents(self):
        pass

    def search_articles(self):
        pass
