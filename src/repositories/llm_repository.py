from infrastructure.llm_client import LLMClient


class LLMRepository:
    def __init__(self, llm_client: LLMClient) -> None:
        self.llm_client = llm_client

    def extract_er(self, text: str):
        pass
