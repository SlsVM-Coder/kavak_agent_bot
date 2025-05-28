# app/services/handlers/option_handler.py
from app.services.session_manager import State
from app.services.recommendation_service import recommend_cars
from app.utils.formatters import format_options


class OptionHandler:
    def handle(self, user_id: str, text: str, sessions, llm) -> str:
        opt = text.strip().upper()
        if opt == "A":
            sessions.set_state(user_id, State.AWAITING_CAR_DETAILS)
            return 'Para ayudarte, ¿me podrías proporcionar "Marca, Modelo, Año"?'
        if opt == "B":
            cars = recommend_cars("", limit=3)
            sessions.get_data(user_id)["recommendations"] = cars
            sessions.set_state(user_id, State.AWAITING_CAR_SELECTION)
            return format_options(cars)

        prompt = (
            f"El cliente respondió «{text}» cuando le ofrecí:\n"
            "A) Ayuda a encontrar tu próximo auto\n"
            "B) Recomienda algunos modelos\n\n"
            "Reformula esta invitación de forma amable y pídele que elija A o B."
        )
        return llm.chat_user(prompt, max_tokens=60, temperature=0.7)
