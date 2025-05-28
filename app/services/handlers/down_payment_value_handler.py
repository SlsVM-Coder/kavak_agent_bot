from app.services.session_manager import State


class DownPaymentValueHandler:
    def handle(self, user_id: str, text: str, sessions, llm) -> str:
        data = sessions.get_data(user_id)
        sel = data.get("down_choice")
        val = text.strip().replace("%", "").replace(",", "")

        try:
            num = float(val)
            if sel == "D":  # libre %
                data["down_payment"] = round(
                    data["selected_car"]["price"] * (num/100), 2)
            else:           # cantidad
                data["down_payment"] = num
        except:
            prompt = (
                f"El cliente escribió «{text}» para enganche. "
                "Reformula pidiendo un porcentaje (ej. 12%) o una cantidad en pesos."
            )
            return llm.chat_user(prompt, max_tokens=40, temperature=0.7)

        sessions.set_state(user_id, State.AWAITING_TERM)
        return "¿A cuántos años deseas financiar? (3–6 años)"
