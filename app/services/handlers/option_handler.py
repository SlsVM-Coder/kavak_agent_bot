from app.api.models import OutgoingMessage
from app.services.session_manager import State
from app.services.recommendation_service import recommend_cars


class OptionHandler:
    def handle(self, user_id: str, text: str, sessions, llm) -> OutgoingMessage:
        opt = text.strip().upper()
        if opt == "A":
            sessions.set_state(user_id, State.AWAITING_CAR_DETAILS)
            return OutgoingMessage(text='Para ayudarte, ¿me podrías proporcionar "Marca, Modelo, Año"?')

        if opt == "B":
            cars = recommend_cars("", limit=3)
            sessions.get_data(user_id)["recommendations"] = cars
            sessions.set_state(user_id, State.AWAITING_CAR_SELECTION)
            lines = [
                f"{chr(ord('A')+i)}) {c['make']} {c['model']} {c['year']} (${c['price']:,.0f})"
                for i, c in enumerate(cars)
            ]
            return OutgoingMessage(text="Elige el auto que más te guste:\n" + "\n".join(lines))

        prompt = (
            f"El cliente respondió «{text}» cuando le ofrecí A) Buscar auto o B) Recomendar modelos. "
            "Reformula de forma amable pidiéndole que elija A o B."
        )
        return OutgoingMessage(text=llm.chat_user(prompt, max_tokens=60, temperature=0.7))
