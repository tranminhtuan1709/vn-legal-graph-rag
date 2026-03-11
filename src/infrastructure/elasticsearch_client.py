from elasticsearch import Elasticsearch


class ElasticsearchClient:
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        request_timeout: int
    ) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.request_timeout = request_timeout

        try:
            self.es = Elasticsearch(
                hosts=[f"http://{self.host}:{self.port}"],
                basic_auth=(self.username, self.password),
                request_timeout=self.request_timeout
            )
        except Exception:
            raise
