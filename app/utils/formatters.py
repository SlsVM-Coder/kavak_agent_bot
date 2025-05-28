from typing import List, Dict
from app.utils.constants import FAREWELL_MSG


def plain_recommendation(cars: List[Dict]) -> str:
    if not cars:
        return "Lo siento, no encontré autos que coincidan con tu búsqueda." + FAREWELL_MSG
    lines = [
        f"- {c['make']} {c['model']} {c['year']} (${c['price']:,.0f})" for c in cars]
    return "Te recomiendo estos autos:\n" + "\n".join(lines)
