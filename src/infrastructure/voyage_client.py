import os
from voyageai import client

from exceptions import InfrastructureError


class VoyageClient:
    def __init__(self) -> None:
        """
        Create a voyage client.

        Raises:
            InfrastructureError: If there are any errors occur.
        """

        self.api_key = os.getenv("VOYAGE_API_KEY")

        try:
            self.voyage_client = client.Client(self.api_key)
        except Exception as e:
            raise InfrastructureError("Failed to create Voyage client") from e
    
    def get_embedding(self, text: str, model: str, dimension: int) -> list[float]:
        """
        Embed a string `text` using embedding model `model` into a vector of dimension `dimension`.

        Args:
            text (str): Text to embed.
            model (str): VoyageAI model used to embed.
            dimension (int): Dimension of the vector embedding.

        Raises:
            InfrastructureError: If there are any errors occur.

        Returns:
            list[float]: Vector embedding.
        """
        
        if text == "" or dimension == 0:
            return []
        
        try:
            return self.voyage_client.embed(
                texts=[text],
                model=model,
                output_dimension=dimension
            ).embeddings[0]
        except Exception as e:
            raise InfrastructureError(
                message="Failed to get embedding",
                context={
                    "text": text,
                    "model": model,
                    "dimension": dimension
                }
            ) from e
