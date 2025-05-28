# app/services/handlers/term_handler.py

from app.api.models import OutgoingMessage
from app.services.financing_calculator import calculate_financing_plan
from app.services.session_manager import State
from app.utils.constants import FAREWELL_MSG
from app.llm.prompt_templates import SYSTEM_PROMPT


class TermHandler:
    def handle(self, user_id: str, text: str, sessions, llm) -> OutgoingMessage:
        data = sessions.get_data(user_id)

        # 1) Validar años
        try:
            years = int(text.strip())
            if years < 3 or years > 6:
                raise ValueError()
            data["term_years"] = years
        except:
            prompt = (
                f"El cliente respondió «{text}» para el plazo. "
                "Por favor indícalo como un número de años entre 3 y 6."
            )
            reply = llm.chat(
                [{"role": "system",  "content": SYSTEM_PROMPT},
                 {"role": "user",    "content": prompt}],
                max_tokens=30, temperature=0.7
            )
            # type: ignore
            return OutgoingMessage(text=reply.choices[0].message.content.strip())

        # 2) Cálculo de financiamiento
        car = data["selected_car"]
        down = data["down_payment"]
        plan = calculate_financing_plan(car["price"], down, years)

        # 3) Cantidad de pagos en meses
        months = years * 12

        # 4) Construir mensaje final
        financing_msg = (
            f"Tu plan de financiamiento para el {car['make']} {car['model']}:\n"
            f"- Pago mensual: ${plan['monthly_payment_amount']:,.2f}\n"
            f"- Total a pagar:  ${plan['total_amount_paid']:,.2f}\n"
            f"- Número de pagos (meses): {months}"
        )

        # 5) Limpiar sesión y despedirse
        sessions.clear(user_id)
        return OutgoingMessage(text=financing_msg + "\n\n" + FAREWELL_MSG)
