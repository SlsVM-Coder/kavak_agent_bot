from typing import List, Dict
from app.dependencies.openai_client import OpenAIClient
from app.llm.prompt_templates import SYSTEM_PROMPT


class LLMService:
    def __init__(self, client: OpenAIClient):
        self.client = client

    def chat_user(self, user_prompt: str, max_tokens: int, temperature: float) -> str:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": user_prompt}
        ]
        resp = self.client.chat(
            messages, max_tokens=max_tokens, temperature=temperature)
        return resp.choices[0].message.content.strip()  # type: ignore
