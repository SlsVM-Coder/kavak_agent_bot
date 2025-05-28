from app.api.models import OutgoingMessage
from app.services.session_manager import State
from app.utils.constants import FAREWELL_MSG


class FinanceConfirmHandler:
    def handle(self, user_id: str, text: str, sessions, llm) -> OutgoingMessage:
        opt = text.strip().upper()
        if opt == "A":
            sessions.set_state(user_id, State.AWAITING_DOWN_PAYMENT_CHOICE)
            return OutgoingMessage(text=(
                "¿Cuánto te gustaría dar de enganche?\n"
                "A) 10%\n"
                "B) 15%\n"
                "C) 20%\n"
                "D) Otro porcentaje\n"
                "E) Cantidad"
            ))
        if opt == "B":
            sessions.clear(user_id)
            return OutgoingMessage(text="¡Entendido! Si necesitas algo más, aquí estamos. 😊" + FAREWELL_MSG)

        prompt = (
            f"El cliente escribió «{text}», pero las opciones eran A) Sí o B) No. "
            "Reformula pidiéndole A o B."
        )
        return OutgoingMessage(text=llm.chat_user(prompt, max_tokens=40, temperature=0.7))
