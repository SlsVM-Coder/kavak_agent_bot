# app/services/handlers/down_payment_choice_handler.py

from app.api.models import OutgoingMessage
from app.services.session_manager import State


class DownPaymentChoiceHandler:
    def handle(self, user_id: str, text: str, sessions, llm) -> OutgoingMessage:
        data = sessions.get_data(user_id)
        price = data["selected_car"]["price"]
        opt = text.strip().upper()

        # Opciones fijas 10%, 15%, 20%
        if opt in ("A", "B", "C"):
            pct_map = {"A": 0.10, "B": 0.15, "C": 0.20}
            data["down_payment"] = round(price * pct_map[opt], 2)
            sessions.set_state(user_id, State.AWAITING_TERM)
            return OutgoingMessage(text=(
                "¿A cuántos años deseas financiar?\n"
                "3) 3 años\n"
                "4) 4 años\n"
                "5) 5 años\n"
                "6) 6 años"
            ))

        # Porcentaje libre
        if opt == "D":
            data["down_choice"] = opt
            sessions.set_state(user_id, State.AWAITING_DOWN_PAYMENT_VALUE)
            return OutgoingMessage(text=(
                "Por favor, indícame el porcentaje de enganche que deseas (ej. 12%)."
            ))

        # Cantidad en pesos
        if opt == "E":
            data["down_choice"] = opt
            sessions.set_state(user_id, State.AWAITING_DOWN_PAYMENT_VALUE)
            return OutgoingMessage(text=(
                "Por favor, indícame la cantidad de enganche en pesos (ej. 50000)."
            ))

        # Opción inválida → reformulación con LLM
        prompt = (
            f"El cliente escribió «{text}», pero las opciones eran:\n"
            "A) 10%  B) 15%  C) 20%  D) Otro porcentaje  E) Cantidad.\n"
            "Reformula de forma amable pidiéndole que elija una de esas letras."
        )
        reply = llm.chat_user(prompt, max_tokens=40, temperature=0.7)
        return OutgoingMessage(text=reply)
