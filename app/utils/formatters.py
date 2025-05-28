from typing import List, Dict
from app.utils.constants import FAREWELL_MSG


def format_options(cars: List[Dict]) -> str:
    if not cars:
        return "Lo siento, no encontré autos que coincidan con tu búsqueda." + FAREWELL_MSG
    lines = []
    for idx, car in enumerate(cars, start=1):
        letter = chr(ord("A") + idx - 1)
        lines.append(
            f"{letter}) {car['make']} {car['model']} {car['year']} (${car['price']:,.0f})")

    return (
        "Elige la opción del auto que más te agrade:\n"
        + "\n".join(lines)
        + "\n\nEscribe la letra (A, B, C...) de tu elección."
    )
