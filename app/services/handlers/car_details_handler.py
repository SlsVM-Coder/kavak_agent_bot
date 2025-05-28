# app/services/handlers/car_details_handler.py
from app.services.session_manager import State
from app.services.recommendation_service import find_exact_model_year, recommend_cars
from app.utils.formatters import format_options


class CarDetailsHandler:
    def handle(self, user_id: str, text: str, sessions, llm) -> str:
        exact = find_exact_model_year(text, threshold=80)
        cars = exact if exact else recommend_cars(text, limit=3)
        data = sessions.get_data(user_id)

        if len(cars) == 1:
            selected = cars[0]
            data["selected_car"] = selected
            sessions.set_state(user_id, State.AWAITING_FINANCE_CONFIRM)
            return (
                f"He encontrado este auto para ti:\n"
                f"- {selected['make']} {selected['model']} {selected['year']} "
                f"(${selected['price']:,.0f})\n\n"
                "¿Te gustaría un plan de financiamiento para este auto? Responde Sí o No."
            )

        data["recommendations"] = cars
        sessions.set_state(user_id, State.AWAITING_CAR_SELECTION)
        return format_options(cars)
