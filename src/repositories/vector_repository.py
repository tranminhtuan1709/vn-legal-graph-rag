import requests
import os


class VectorRepository:
    def __init__(self) -> None:
        pass
    
    def search_documents(self, text: str) -> list[int]:
        try:
            query = {
                "knn": {
                    "field": os.getenv("ELASTIC_DOCUMENT_EMBEDDING_FIELD"),
                    "query": ""
                }
            }
        except Exception:
            raise

    def search_articles(self):
        pass
