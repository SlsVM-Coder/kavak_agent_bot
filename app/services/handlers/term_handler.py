from app.services.session_manager import State
from app.services.financing_calculator import calculate_financing_plan
from app.utils.constants import FAREWELL_MSG


class TermHandler:
    def handle(self, user_id: str, text: str, sessions, llm) -> str:
        data = sessions.get_data(user_id)
        try:
            yrs = int(text.strip())
            assert 3 <= yrs <= 6
            data["term_years"] = yrs
        except:
            prompt = "Por favor indícame un número de años **entre 3 y 6**."
            return llm.chat_user(prompt, max_tokens=30, temperature=0.7)

        car = data["selected_car"]
        plan = calculate_financing_plan(
            car["price"], data["down_payment"], yrs)

        sessions.clear(user_id)
        return (
            f"Tu plan de financiamiento para el {car['make']} {car['model']}:\n"
            f"- Pago mensual: ${plan['monthly_payment_amount']:,.2f}\n"
            f"- Total a pagar:  ${plan['total_amount_paid']:,.2f}\n"
            + FAREWELL_MSG
        )
