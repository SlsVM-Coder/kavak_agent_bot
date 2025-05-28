from app.api.models import OutgoingMessage
from app.services.session_manager import State


class DownPaymentValueHandler:
    def handle(self, user_id: str, text: str, sessions, llm) -> OutgoingMessage:
        data = sessions.get_data(user_id)
        sel = data.get("down_choice")
        val = text.strip().rstrip("%").replace(",", "")
        try:
            num = float(val)
            if sel == "D":
                data["down_payment"] = round(
                    data["selected_car"]["price"] * (num/100), 2)
            else:
                data["down_payment"] = num
        except:
            prompt = (
                f"El cliente escribió «{text}». Por favor pide porcentaje (ej. 12%) o cantidad."
            )
            return OutgoingMessage(text=llm.chat_user(prompt, max_tokens=40, temperature=0.7))

        sessions.set_state(user_id, State.AWAITING_TERM)
        return OutgoingMessage(text=(
            "¿A cuántos años deseas financiar?\n"
            "3) 3 años\n"
            "4) 4 años\n"
            "5) 5 años\n"
            "6) 6 años"
        ))
