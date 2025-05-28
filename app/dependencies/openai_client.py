from functools import lru_cache
from openai import OpenAI
from app.config import OPENAI_API_KEY, OPENAI_MODEL


class OpenAIClient:
    def __init__(self):
        self.model = OPENAI_MODEL
        self.client = OpenAI(api_key=OPENAI_API_KEY)

    def chat(self, messages: list[dict[str, str]], **kwargs) -> dict:
        payload = {"model": self.model, "messages": messages, **kwargs}
        return self.client.chat.completions.create(**payload)  # type: ignore


@lru_cache()
def get_openai_client() -> OpenAIClient:
    return OpenAIClient()
