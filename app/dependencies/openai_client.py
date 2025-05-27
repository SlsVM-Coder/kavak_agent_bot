# app/dependencies/openai_client.py

import os
from functools import lru_cache
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class OpenAIClient:
    def __init__(self):
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        print(self.client)

    def chat(self,
             messages: list[dict[str, str]],
             **kwargs
             ) -> dict:
        # Construimos el payload
        payload = {
            "model":    self.model,
            "messages": messages,
            **kwargs,    # p.ej. max_tokens, temperature…
        }
        # Llamada real al cliente tipado de OpenAI.
        # En tiempo de ejecución funciona; Pylance marcará warning,
        # así que lo silenciamos con type: ignore.
        return self.client.chat.completions.create(**payload)  # type: ignore


@lru_cache()
def get_openai_client() -> OpenAIClient:
    return OpenAIClient()
