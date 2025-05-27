# app/services/whatsapp_service.py

from typing import List, Dict
from app.services.session_manager import SessionManager, State
from app.services.recommendation_service import find_exact_model_year, recommend_cars
from app.services.financing_calculator import calculate_financing_plan
from app.dependencies.openai_client import OpenAIClient
from app.llm.prompt_templates import SYSTEM_PROMPT


class WhatsAppService:
    FAREWELL_MSG = (
        "\n\nRecuerda que en Kavak queremos ayudarte a moverte libremente, "
        "a crear tus propios recuerdos: esas salidas nocturnas con amigos coreando "
        "tus canciones favoritas, quizá tu primer beso o simplemente disfrutar de la "
        "ciudad a tu ritmo. Cuando sientas que es tu momento, aquí te esperamos. 🚗✨"
    )
    EXACT_MATCH_THRESHOLD = 80

    def __init__(self, ai_client: OpenAIClient, sessions: SessionManager):
        self.ai = ai_client
        self.sessions = sessions

    def handle_message(self, user_id: str, text: str) -> str:
        state = self.sessions.get_state(user_id)
        if state is None:
            return self._greet(user_id)

        handlers = {
            State.AWAITING_OPTION:               self._handle_option,
            State.AWAITING_CAR_DETAILS:          self._handle_car_details,
            State.AWAITING_CAR_SELECTION:        self._handle_car_selection,
            State.AWAITING_FINANCE_CONFIRM:      self._handle_finance_confirm,
            State.AWAITING_DOWN_PAYMENT_CHOICE:  self._handle_down_payment_choice,
            State.AWAITING_DOWN_PAYMENT_VALUE:   self._handle_down_payment_value,
            State.AWAITING_TERM:                 self._handle_term,
        }
        return handlers.get(state, lambda uid, msg: self._fallback(msg))(user_id, text)

    def _greet(self, user_id: str) -> str:
        prompt = (
            "Eres un agente comercial de Kavak, amigable y cercano. "
            "Saluda al cliente y ofrécele:\n"
            "A) Ayuda a encontrar tu próximo auto\n"
            "B) Recomienda algunos modelos"
        )
        resp = self.ai.chat(
            [{"role": "system", "content": SYSTEM_PROMPT},
             {"role": "user",   "content": prompt}],
            max_tokens=80, temperature=0.7
        )
        greeting = resp.choices[0].message.content.strip()  # type: ignore

        self.sessions.start(user_id)
        self.sessions.set_state(user_id, State.AWAITING_OPTION)
        return greeting

    def _handle_option(self, user_id: str, text: str) -> str:
        opt = text.strip().upper()
        if opt == "A":
            self.sessions.set_state(user_id, State.AWAITING_CAR_DETAILS)
            return 'Para ayudarte, ¿me podrías proporcionar "Marca, Modelo, Año"?'
        if opt == "B":
            cars = recommend_cars("", limit=3)
            self.sessions.get_data(user_id)["recommendations"] = cars
            self.sessions.set_state(user_id, State.AWAITING_CAR_SELECTION)
            return self._format_options(cars)

        # invalid → LLM
        prompt = (
            f"El cliente respondió «{text}» cuando le ofrecí:\n"
            "A) Ayuda a encontrar tu próximo auto\n"
            "B) Recomienda algunos modelos\n\n"
            "Reformula esta invitación de forma amable y pídele que elija A o B."
        )
        resp = self.ai.chat(
            [{"role": "system", "content": SYSTEM_PROMPT},
             {"role": "user",   "content": prompt}],
            max_tokens=60, temperature=0.7
        )
        return resp.choices[0].message.content.strip()  # type: ignore

    def _handle_car_details(self, user_id: str, text: str) -> str:
        exact = find_exact_model_year(
            text, threshold=self.EXACT_MATCH_THRESHOLD)
        cars = exact if exact else recommend_cars(text, limit=3)
        data = self.sessions.get_data(user_id)

        # Si solo hay un auto, saltamos a confirmar financiamiento
        if len(cars) == 1:
            selected = cars[0]
            data["selected_car"] = selected
            self.sessions.set_state(user_id, State.AWAITING_FINANCE_CONFIRM)
            return (
                f"He encontrado este auto para ti:\n"
                f"- {selected['make']} {selected['model']} {selected['year']} "
                f"(${selected['price']:,.0f})\n\n"
                "¿Te gustaría un plan de financiamiento para este auto? Responde Sí o No."
            )

        # Múltiples opciones → selección
        data["recommendations"] = cars
        self.sessions.set_state(user_id, State.AWAITING_CAR_SELECTION)
        return self._format_options(cars)

    def _format_options(self, cars: List[Dict]) -> str:
        if not cars:
            return "Lo siento, no encontré autos que coincidan con tu búsqueda." + self.FAREWELL_MSG

        lines = []
        for idx, car in enumerate(cars, start=1):
            letter = chr(ord("A") + idx - 1)
            lines.append(
                f"{letter}) {car['make']} {car['model']} {car['year']} (${car['price']:,.0f})")

        options_text = "\n".join(lines)
        return (
            f"Elige la opción del auto que más te agrade:\n{options_text}\n\n"
            "Escribe la letra (A, B, C...) de tu elección."
        )

    def _handle_car_selection(self, user_id: str, text: str) -> str:
        data = self.sessions.get_data(user_id)
        cars = data.get("recommendations", [])
        idx = ord(text.strip().upper()) - ord("A")
        if 0 <= idx < len(cars):
            selected = cars[idx]
            data["selected_car"] = selected
            self.sessions.set_state(user_id, State.AWAITING_FINANCE_CONFIRM)
            return (
                "¿Te gustaría un plan de financiamiento para este auto? Responde Sí o No."
            )

        # invalid → LLM
        prompt = (
            f"El cliente escribió «{text}» pero las opciones eran A, B, C... "
            "Reformula de forma amable pidiéndole que elija una letra válida."
        )
        resp = self.ai.chat(
            [{"role": "system", "content": SYSTEM_PROMPT},
             {"role": "user",   "content": prompt}],
            max_tokens=40, temperature=0.7
        )
        return resp.choices[0].message.content.strip()  # type: ignore

    def _handle_finance_confirm(self, user_id: str, text: str) -> str:
        low = text.strip().lower()
        if low in ("sí", "si", "s", "yes", "y"):
            self.sessions.set_state(
                user_id, State.AWAITING_DOWN_PAYMENT_CHOICE)
            return (
                "Perfecto, dime cuánto te gustaría dar de enganche:\n"
                "A) 10%  B) 15%  C) 20%  D) Otro porcentaje  E) Cantidad"
            )
        if low in ("no", "n", "nop", "nope"):
            self.sessions.clear(user_id)
            return (
                "¡Entendido! Si necesitas algo más, aquí estamos. 😊"
                + self.FAREWELL_MSG
            )

        # invalid → LLM
        prompt = (
            f"El cliente respondió «{text}» cuando pregunté: "
            "¿Te gustaría un plan de financiamiento para este auto? Responde Sí o No.\n\n"
            "Reformula la pregunta de manera amable, pidiéndole que responda Sí o No."
        )
        resp = self.ai.chat(
            [{"role": "system", "content": SYSTEM_PROMPT},
             {"role": "user",   "content": prompt}],
            max_tokens=40, temperature=0.7
        )
        return resp.choices[0].message.content.strip()  # type: ignore

    def _handle_down_payment_choice(self, user_id: str, text: str) -> str:
        data = self.sessions.get_data(user_id)
        selected = data["selected_car"]
        price = selected["price"]
        opt = text.strip().upper()

        if opt in ("A", "B", "C"):
            pct = {"A": 0.10, "B": 0.15, "C": 0.20}[opt]
            data["down_payment"] = round(price * pct, 2)
            self.sessions.set_state(user_id, State.AWAITING_TERM)
            return "¿A cuántos años deseas financiar? (3–6 años)"

        if opt in ("D", "E"):
            data["down_choice"] = opt
            self.sessions.set_state(user_id, State.AWAITING_DOWN_PAYMENT_VALUE)
            return "Por favor indícame el porcentaje (ej. 12%) o la cantidad en pesos (ej. 50000)."

        # invalid → LLM
        prompt = (
            f"El cliente respondió «{text}» pero las opciones eran A–E. "
            "Reformula de forma amable pidiéndole que elija una opción válida."
        )
        resp = self.ai.chat(
            [{"role": "system", "content": SYSTEM_PROMPT},
             {"role": "user",   "content": prompt}],
            max_tokens=40, temperature=0.7
        )
        return resp.choices[0].message.content.strip()  # type: ignore

    def _handle_down_payment_value(self, user_id: str, text: str) -> str:
        data = self.sessions.get_data(user_id)
        sel = data.get("down_choice")
        val = text.strip().replace("%", "").replace(",", "")

        try:
            num = float(val)
            if sel == "D":
                pct = num / 100.0
                data["down_payment"] = round(
                    data["selected_car"]["price"] * pct, 2)
            else:
                data["down_payment"] = num
        except:
            prompt = (
                f"El cliente escribió «{text}» para enganche. "
                "Reformula pidiendo un porcentaje (ej. 12%) o una cantidad en pesos."
            )
            resp = self.ai.chat(
                [{"role": "system", "content": SYSTEM_PROMPT},
                 {"role": "user",   "content": prompt}],
                max_tokens=40, temperature=0.7
            )
            return resp.choices[0].message.content.strip()  # type: ignore

        self.sessions.set_state(user_id, State.AWAITING_TERM)
        return "¿A cuántos años deseas financiar? (3–6 años)"

    def _handle_term(self, user_id: str, text: str) -> str:
        data = self.sessions.get_data(user_id)
        try:
            years = int(text.strip())
            if years < 3 or years > 6:
                raise ValueError()
            data["term_years"] = years
        except:
            prompt = (
                f"El cliente respondió «{text}». "
                "Por favor reformula pidiendo un número de años entre 3 y 6."
            )
            resp = self.ai.chat(
                [{"role": "system", "content": SYSTEM_PROMPT},
                 {"role": "user",   "content": prompt}],
                max_tokens=30, temperature=0.7
            )
            return resp.choices[0].message.content.strip()  # type: ignore

        car = data["selected_car"]
        down = data["down_payment"]
        yrs = data["term_years"]
        plan = calculate_financing_plan(car["price"], down, yrs)

        financing_msg = (
            f"Tu plan de financiamiento para el {car['make']} {car['model']}:\n"
            f"- Pago mensual: ${plan['monthly_payment_amount']:,.2f}\n"
            f"- Total a pagar:  ${plan['total_amount_paid']:,.2f}\n"
        )
        self.sessions.clear(user_id)
        return financing_msg + self.FAREWELL_MSG

    def _fallback(self, text: str) -> str:
        resp = self.ai.chat(
            [{"role": "system", "content": SYSTEM_PROMPT},
             {"role": "user",   "content": text}],
            max_tokens=150, temperature=0.3
        )
        return resp.choices[0].message.content.strip()  # type: ignore
