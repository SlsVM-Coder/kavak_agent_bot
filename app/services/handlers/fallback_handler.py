from app.api.models import OutgoingMessage


class FallbackHandler:
    def handle(self, user_id: str, text: str, sessions, llm) -> OutgoingMessage:
        # No limpiamos sesión: mantiene el estado
        answer = llm.chat_user(text, max_tokens=150, temperature=0.3)
        return OutgoingMessage(text=answer)
