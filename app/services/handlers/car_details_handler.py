# app/services/handlers/car_details_handler.py

from app.api.models import OutgoingMessage
from app.services.session_manager import State
from app.services.recommendation_service import find_exact_model_year, recommend_cars


class CarDetailsHandler:
    def handle(self, user_id: str, text: str, sessions, llm) -> OutgoingMessage:
        exact = find_exact_model_year(text, threshold=80)
        cars = exact if exact else recommend_cars(text, limit=3)
        data = sessions.get_data(user_id)

        # Caso 1: sólo hay un auto coincidente → saltamos directo a financiamiento
        if len(cars) == 1:
            sel = cars[0]
            data["selected_car"] = sel
            sessions.set_state(user_id, State.AWAITING_FINANCE_CONFIRM)
            msg = (
                f"He encontrado este auto para ti:\n"
                f"- {sel['make']} {sel['model']} {sel['year']} (${sel['price']:,.0f})\n\n"
                "¿Te gustaría un plan de financiamiento para este auto?\n"
                "A) Sí\n"
                "B) No"
            )
            return OutgoingMessage(text=msg)

        # Caso 2: varias coincidencias → listamos opciones y preguntamos financiamiento
        data["recommendations"] = cars
        sessions.set_state(user_id, State.AWAITING_CAR_SELECTION)

        # Construimos la lista A), B), C)…
        lines = [
            f"{chr(ord('A')+i)}) {c['make']} {c['model']} {c['year']} (${c['price']:,.0f})"
            for i, c in enumerate(cars)
        ]
        message = "Tenemos estos autos que coinciden:\n" + "\n".join(lines)

        # Nueva pregunta de financiamiento
        message += (
            "\n\n¿Te gustaría que te ayudara con un plan de financiamiento "
            "para alguna de estas opciones? Escribe la letra (A, B o C)."
        )

        return OutgoingMessage(text=message)
