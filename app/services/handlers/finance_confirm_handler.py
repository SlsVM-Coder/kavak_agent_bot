from app.services.session_manager import State


class FinanceConfirmHandler:
    def handle(self, user_id: str, text: str, sessions, llm) -> str:
        low = text.strip().lower()
        if low in ("sí", "si", "s", "yes", "y"):
            sessions.set_state(user_id, State.AWAITING_DOWN_PAYMENT_CHOICE)
            return (
                "Perfecto, dime cuánto te gustaría dar de enganche:\n"
                "A) 10%  B) 15%  C) 20%  D) Otro porcentaje  E) Cantidad"
            )
        if low in ("no", "n", "nop", "nope"):
            sessions.clear(user_id)
            # farewell se añade en _fallback
            return "¡Entendido! Si necesitas algo más, aquí estamos. 😊" + sessions.clear and ""

        prompt = (
            f"El cliente respondió «{text}» cuando pregunté: "
            "¿Te gustaría un plan de financiamiento para este auto? Responde Sí o No."
        )
        return llm.chat_user(prompt, max_tokens=40, temperature=0.7)
