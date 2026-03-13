from google import genai


class LLMClient:
    def __init__(self, api_key: str, project: str, location: str, model: str) -> None:
        self.gemini_client = genai.Client(
            api_key=api_key,
            project=project,
            location=location
        )
