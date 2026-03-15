from typing import Any


class CustomError(Exception):
    def __init__(self, message: str, context: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.context = context


class InfrastructureError(CustomError):
    pass


class EmbedError(CustomError):
    pass


class SearchDocumentError(CustomError):
    pass


class SearchArticleError(CustomError):
    pass


class GraphTraversalError(CustomError):
    pass
