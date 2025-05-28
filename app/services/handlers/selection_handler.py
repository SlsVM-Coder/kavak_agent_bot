from app.services.session_manager import State


class SelectionHandler:
    def handle(self, user_id: str, text: str, sessions, llm) -> str:
        data = sessions.get_data(user_id)
        cars = data.get("recommendations", [])
        idx = ord(text.strip().upper()) - ord("A")
        if 0 <= idx < len(cars):
            data["selected_car"] = cars[idx]
            sessions.set_state(user_id, State.AWAITING_FINANCE_CONFIRM)
            return "¿Te gustaría un plan de financiamiento para este auto? Responde Sí o No."

        prompt = (
            f"El cliente escribió «{text}» pero las opciones eran A, B, C... "
            "Reformula de forma amable pidiéndole que elija una letra válida."
        )
        return llm.chat_user(prompt, max_tokens=40, temperature=0.7)
