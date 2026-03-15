import requests
import os

from exceptions import SearchDocumentError, SearchArticleError

class VectorRepository:
    def __init__(self) -> None:
        """
        Init an instance of this class and get necessary environment variables.
        """

        self.elastic_host = os.getenv("ELASTIC_HOST")
        self.elastic_port = int(os.getenv("ELASTIC_PORT"))
        self.elastic_username = os.getenv("ELASTIC_USERNAME")
        self.elastic_password = os.getenv("ELASTIC_PASSWORD")

        self.elastic_document_index_name = os.getenv("ELASTIC_DOCUMENT_INDEX_NAME")
        self.elastic_document_embedding_field = os.getenv("ELASTIC_DOCUMENT_EMBEDDING_FIELD")
        self.elastic_search_document_timeout = os.getenv("ELASTIC_SEARCH_DOCUMENT_TIMEOUT")

        self.elastic_article_index_name = os.getenv("ELASTIC_ARTICLE_INDEX_NAME")
        self.elastic_article_embedding_field = os.getenv("ELASTIC_ARTICLE_EMBEDDING_FIELD")
        self.elastic_search_article_timeout = os.getenv("ELASTIC_SEARCH_ARTICLE_TIMEOUT")
    
    def search_documents(self, embedding: list[float], n_doc: int) -> list[int]:
        """
        Search documents in ElasticSearch using ANN.

        Args:
            embedding (list[float]): Vector embedding used for semantic search.
            n_doc (int): Number of documents to search (top_k).

        Raises:
            SearchDocumentError: If there are any errors occur.

        Returns:
            list[int]: List of document IDs.
        """
        
        if n_doc == 0:
            return []
        
        response = None

        try:
            query = {
                "knn": {
                    "field": self.elastic_document_embedding_field,
                    "query": embedding,
                    "k": n_doc,
                    "num_candidates": 10000
                },
                "_source": ["id"]
            }

            response = requests.post(
                url=f"http://{self.elastic_host}:{self.elastic_port}/{self.elastic_document_index_name}/_search",
                auth=(self.elastic_username, self.elastic_password),
                headers={"Content-Type": "application/json"},
                timeout=self.elastic_search_document_timeout,
                json=query
            )

            if response.status_code != 200:
                raise Exception("Unexpected response status")
            
            response_json = response.json()
            document_ids = []
            
            for item in response_json.get("hits", {}).get("hits", []):
                document_id = item.get("_source", {}).get("id")

                if document_id is not None and isinstance(document_id, int):
                    document_ids.append(document_id)
            
            return document_ids
        except Exception as e:
            raise SearchDocumentError(
                message="Failed to search document from ElasticSearch",
                context={
                    "status_code": response.status_code if response is not None else None,
                    "response": response.text if response is not None else None,
                    "index": self.elastic_document_index_name,
                    "embedding_field": self.elastic_document_embedding_field,
                    "embedding_dimension": len(embedding),
                    "k": n_doc
                }
            ) from e

    def search_articles(self, embedding: list[float], n_art: int, document_ids: list[int]) -> list[int]:
        """
        Search articles from ElasticSearch using ANN with prefiltering by a list of document IDs.

        Args:
            embedding (list[float]): Vector embedding used for semantic search.
            n_art (int): Number of articles to search (top_k).
            document_ids (list[int]): List of document IDs used for prefiltering before ANN.

        Raises:
            SearchArticleError: If there are any problems occur.

        Returns:
            list[int]: List of found article IDs.
        """

        if n_art == 0 or len(document_ids) == 0:
            return []
        
        query = None
        response = None

        try:
            query = {
                "knn": {
                    "field": self.elastic_article_embedding_field,
                    "query": embedding,
                    "k": n_art,
                    "num_candidates": 10000,
                    "filter": {
                        "terms": {
                            "law_ids": document_ids
                        }
                    }
                },
                "_source": ["article_pk"]
            }

            response = requests.post(
                url=f"http://{self.elastic_host}:{self.elastic_port}/{self.elastic_article_index_name}/_search",
                auth=(self.elastic_username, self.elastic_password),
                headers={"Content-Type": "application/json"},
                timeout=self.elastic_search_article_timeout,
                json=query
            )

            if response.status_code != 200:
                raise Exception("Unexpected response status")

            response_json = response.json()
            article_ids = []

            for item in response_json.get("hits", {}).get("hits", []):
                article_id = item.get("_source", {}).get("article_pk")

                if article_id is not None and isinstance(article_id, int):
                    article_ids.append(article_id)
            
            return article_ids
        except Exception as e:
            raise SearchArticleError(
                message="Failed to search article from ElasticSearch",
                context={
                    "status_code": response.status_code if response is not None else None,
                    "response": response.text if response is not None else None,
                    "index": self.elastic_article_index_name,
                    "embedding_dimension": len(embedding),
                    "k": n_art,
                    "num_document_ids": len(document_ids)
                }
            ) from e
