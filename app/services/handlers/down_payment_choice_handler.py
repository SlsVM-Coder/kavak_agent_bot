from app.services.session_manager import State


class DownPaymentChoiceHandler:
    def handle(self, user_id: str, text: str, sessions, llm) -> str:
        data = sessions.get_data(user_id)
        selected = data["selected_car"]
        price = selected["price"]
        opt = text.strip().upper()

        if opt in ("A", "B", "C"):
            pct_map = {"A": 0.10, "B": 0.15, "C": 0.20}
            data["down_payment"] = round(price * pct_map[opt], 2)
            sessions.set_state(user_id, State.AWAITING_TERM)
            return "¿A cuántos años deseas financiar? (3–6 años)"

        if opt in ("D", "E"):
            data["down_choice"] = opt
            sessions.set_state(user_id, State.AWAITING_DOWN_PAYMENT_VALUE)
            return "Por favor indícame el porcentaje (ej. 12%) o la cantidad en pesos (ej. 50000)."

        prompt = (
            f"El cliente respondió «{text}» pero las opciones eran A–E. "
            "Reformula de forma amable pidiéndole que elija una opción válida."
        )
        return llm.chat_user(prompt, max_tokens=40, temperature=0.7)
