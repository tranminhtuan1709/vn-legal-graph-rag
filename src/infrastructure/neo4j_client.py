from neo4j import GraphDatabase, Session


class Neo4jClient:
    def __init__(
        self,
        host: str,
        port: int,
        username: str,
        password: str,
        database: str,
        connection_timeout: int,
        max_connection_pool_size: int
    ) -> None:

        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database
        self.connection_timeout = connection_timeout
        self.max_connection_pool_size = max_connection_pool_size

        try:
            self.driver = GraphDatabase.driver(
                uri=f"bolt://{self.host}:{self.port}",
                auth=(self.username, self.password),
                connection_timeout=self.connection_timeout,
                max_connection_pool_size=self.max_connection_pool_size
            )

            self.driver.verify_connectivity()
        except Exception:
            raise

    def get_session(self) -> Session:
        try:
            session = self.driver.session(database=self.database)
            
            return session
        except Exception:
            raise
