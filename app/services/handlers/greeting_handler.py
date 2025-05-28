from app.api.models import OutgoingMessage
from app.services.session_manager import State


class GreetingHandler:
    def handle(self, user_id: str, text: str, sessions, llm) -> OutgoingMessage:
        prompt = (
            "Eres un agente comercial de Kavak, muy amable y cercano. "
            "Saluda al cliente, preséntate brevemente y diles que estás aquí para ayudar."
        )
        greeting = llm.chat_user(prompt, max_tokens=80, temperature=0.7)

        body = (
            f"{greeting}\n\n"
            "A) Buscar auto\n"
            "B) Recomendar modelos"
        )

        sessions.start(user_id)
        sessions.set_state(user_id, State.AWAITING_OPTION)
        return OutgoingMessage(text=body)
