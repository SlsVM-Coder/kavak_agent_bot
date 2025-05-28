from functools import lru_cache
from app.dependencies.openai_client import OpenAIClient
from app.llm.prompt_templates import SYSTEM_PROMPT


class LLMService:
    def __init__(self, client: OpenAIClient):
        self.client = client

    @lru_cache(maxsize=10)
    def _static(self, prompt: str) -> str:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt},
        ]
        resp = self.client.chat(messages, max_tokens=80, temperature=0.7)
        return resp.choices[0].message.content.strip()  # type: ignore

    def chat_user(self, prompt: str, max_tokens: int, temperature: float) -> str:
        # Si el prompt coincide con alguno muy usado (saludo, FAQs), cae en la cache
        if prompt.startswith("Eres un agente comercial de Kavak"):
            return self._static(prompt)
        # En cualquier otro caso, invoca normal
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt},
        ]
        resp = self.client.chat(
            messages, max_tokens=max_tokens, temperature=temperature)
        return resp.choices[0].message.content.strip()  # type: ignore
