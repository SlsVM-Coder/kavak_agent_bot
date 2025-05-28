from app.services.session_manager import State
from app.llm.prompt_templates import SYSTEM_PROMPT


class GreetingHandler:
    def handle(self, user_id: str, text: str, sessions, llm) -> str:
        prompt = (
            "Eres un agente comercial de Kavak, amigable y cercano. "
            "Saluda al cliente y ofrécele:\n"
            "A) Ayuda a encontrar tu próximo auto\n"
            "B) Recomienda algunos modelos"
        )
        reply = llm.chat_user(prompt, max_tokens=80, temperature=0.7)
        sessions.start(user_id)
        sessions.set_state(user_id, State.AWAITING_OPTION)
        return reply
