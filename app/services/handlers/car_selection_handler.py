# app/services/handlers/car_selection_handler.py

from app.api.models import OutgoingMessage
from app.services.session_manager import State


class CarSelectionHandler:
    def handle(self, user_id: str, text: str, sessions, llm) -> OutgoingMessage:
        data = sessions.get_data(user_id)
        cars = data.get("recommendations", [])

        idx = ord(text.strip().upper()) - ord("A")
        if 0 <= idx < len(cars):
            selected = cars[idx]
            data["selected_car"] = selected

            # Ir directo a ENGANCHE, sin volver a confirmar financiamiento
            sessions.set_state(user_id, State.AWAITING_DOWN_PAYMENT_CHOICE)
            return OutgoingMessage(text=(
                f"Has elegido: {selected['make']} {selected['model']} {selected['year']} "
                f"(${selected['price']:,.0f}).\n\n"
                "¿Cuánto te gustaría dar de enganche? "
                "Puedes elegir por porcentaje o decirme la cantidad:\n"
                "A) 10%  B) 15%  C) 20%  D) Otro porcentaje  E) Cantidad"
            ))

        # Si la letra no es válida, reformulamos con el LLM
        prompt = (
            f"El cliente escribió «{text}», pero las opciones válidas eran "
            f"{', '.join([chr(ord('A')+i) for i in range(len(cars))])}. "
            "Por favor pídele amablemente que elija una de esas letras."
        )
        reply = llm.chat_user(prompt, max_tokens=40, temperature=0.7)
        return OutgoingMessage(text=reply)
