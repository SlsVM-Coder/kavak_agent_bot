# app/services/handlers/fallback_handler.py
from app.llm.prompt_templates import SYSTEM_PROMPT


class FallbackHandler:
    def handle(self, user_id: str, text: str, sessions, llm) -> str:
        # Siempre limpia la sesión al fallback final
        sessions.clear(user_id)
        return llm.chat_user(text, max_tokens=150, temperature=0.3)
