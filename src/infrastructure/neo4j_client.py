import os
from neo4j import GraphDatabase, Session

from exceptions import InfrastructureError


class Neo4jClient:
    def __init__(self) -> None:
        """
        Connect to Neo4j and create a Driver.
        This function loads some necessary environment variables.

        Raises:
            InfrastructureError: If there are any errors occur.
        """

        self.host = os.getenv("NEO4J_HOST")
        self.port = os.getenv("NEO4J_PORT")
        self.username = os.getenv("NEO4J_USERNAME")
        self.password = os.getenv("NEO4J_PASSWORD")
        self.database = os.getenv("NEO4J_DATABASE")
        self.connection_timeout = os.getenv("NEO4J_CONNECTION_TIMEOUT")
        self.max_connection_pool_size = os.getenv("NEO4J_MAX_CONNECTION_POOL_SIZE")

        try:
            self.driver = GraphDatabase.driver(
                uri=f"bolt://{self.host}:{self.port}",
                auth=(self.username, self.password),
                connection_timeout=self.connection_timeout,
                max_connection_pool_size=self.max_connection_pool_size
            )

            self.driver.verify_connectivity()
        except Exception as e:
            raise InfrastructureError(
                message="Failed to connect to Neo4j",
                context={
                    "host": self.host,
                    "port": self.port,
                    "connection_time_out": self.connection_timeout,
                    "max_connection_pool_size": self.max_connection_pool_size
                }
            ) from e

    def get_session(self) -> Session:
        """
        Create and return a session from the connection pool.

        Raises:
            InfrastructureError: If there are any errors occur.

        Returns:
            Session: A session from connection pool.
        """
        
        try:
            session = self.driver.session(self.database)
            
            return session
        except Exception as e:
            raise InfrastructureError(f"Failed to create a Neo4j sessions to database {self.database}") from e
