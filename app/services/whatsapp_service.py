# app/services/whatsapp_service.py

from typing import List, Dict
from rapidfuzz import process, fuzz

from app.services.recommendation_service import (
    recommend_cars,
    find_exact_model_year,
)
from app.services.financing_calculator import calculate_financing_plan
from app.dependencies.openai_client import OpenAIClient
from app.llm.prompt_templates import SYSTEM_PROMPT, USER_PROMPT_FIND_CAR


class WhatsAppService:
    """
    Servicio que procesa el texto entrante y decide:
    - Recomendación de autos
    - Cálculo de financiamiento
    - Fallback a LLM
    """
    # Umbral para considerar “match exacto”
    EXACT_MATCH_THRESHOLD = 80

    def __init__(self, ai_client: OpenAIClient):
        self.ai = ai_client

    def handle_message(self, text: str) -> str:
        text_lower = text.lower()

        if any(kw in text_lower for kw in ["recom", "busco", "quiero un"]):
            return self._handle_recommendation(text)

        if any(kw in text_lower for kw in ["enganche", "financ", "pago mensual"]):
            return self._handle_financing(text)

        return self._handle_fallback(text)

# app/services/whatsapp_service.py  (método _handle_recommendation)

    def _handle_recommendation(self, text: str) -> str:
        # 1) Intentamos encontrar exactamente ese modelo+año
        exact_list = find_exact_model_year(
            text, threshold=self.EXACT_MATCH_THRESHOLD)

        if exact_list:
            # Tomamos make/model del primer match para el encabezado
            first = exact_list[0]
            header = f"{first['make']} {first['model']}"
            lines = "\n".join(
                f"- {c['make']} {c['model']} {c['year']} (${c['price']:,.0f})"
                for c in exact_list
            )
            return f"Tenemos estos autos {header} que te podemos recomendar:\n{lines}"

        # 2) Si no hay coincidencia exacta, caemos en top 3
        top3 = recommend_cars(text, limit=3)
        if top3:
            lines = "\n".join(
                f"- {c['make']} {c['model']} {c['year']} (${c['price']:,.0f})"
                for c in top3
            )
            return (
                "De momento no tenemos el auto que estás buscando, "
                "pero te puedo recomendar estos:\n"
                + lines
            )

        # 3) Ni siquiera hay top3 (muy improbable)
        return "Lo siento, no encontré autos que coincidan con tu búsqueda."

    def _handle_financing(self, text: str) -> str:
        # Ejemplo sencillo de parseo de números
        try:
            # Extraemos solo números del texto
            tokens = [p.replace(",", "") for p in text.split()
                      if p.replace(",", "").isdigit()]
            price, down, years = float(tokens[0]), float(
                tokens[1]), int(tokens[2])
            plan = calculate_financing_plan(price, down, years)
            return (
                f"Pago mensual: ${plan['monthly_payment_amount']:,.2f}\n"
                f"Total a pagar: ${plan['total_amount_paid']:,.2f} "
                f"en {plan['loan_term_months']} meses"
            )
        except Exception:
            return (
                "No pude entender los números para el financiamiento. "
                "Usa: \"400000 con 80000 a 5 años\"."
            )

    def _handle_fallback(self, text: str) -> str:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": USER_PROMPT_FIND_CAR.format(
                user_input=text)}
        ]
        resp = self.ai.chat(messages, max_tokens=300, temperature=0.3)
        # Opción A: dict access para evitar warnings
        reply = resp.choices[0].message.content.strip()  # type: ignore
        return reply
