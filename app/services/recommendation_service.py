# app/services/recommendation_service.py

import pandas as pd
from difflib import SequenceMatcher
from app.config import CATALOG_CSV_PATH

# Verificación temprana de existencia
if not CATALOG_CSV_PATH.is_file():
    raise FileNotFoundError(
        f"Catalog CSV no encontrado en: {CATALOG_CSV_PATH}")

df = pd.read_csv(CATALOG_CSV_PATH)


def normalize(text: str) -> str:
    return text.lower().strip()


def find_exact_model_year(query: str, threshold: float = 80) -> list[dict]:
    q = normalize(query)
    parts = q.replace(",", "").split()
    year = next((int(p) for p in parts if p.isdigit() and len(p) == 4), None)
    model = " ".join([p for p in parts if not (p.isdigit() and len(p) == 4)])
    results = []
    for _, row in df.iterrows():
        if year and row["year"] == year:
            score = SequenceMatcher(None, normalize(
                row["model"]), normalize(model)).ratio() * 100
            if score >= threshold:
                d = row.to_dict()
                d["score"] = score
                results.append(d)
    return results


def recommend_cars(query: str, limit: int = 3) -> list[dict]:
    q = normalize(query)
    scored = []
    for _, row in df.iterrows():
        m = normalize(row["model"])
        mk = normalize(row["make"])
        score = max(SequenceMatcher(None, m, q).ratio(),
                    SequenceMatcher(None, mk, q).ratio())
        scored.append((score, row))
    scored.sort(key=lambda x: x[0], reverse=True)
    result = []
    for score, row in scored[:limit]:
        d = row.to_dict()
        d["score"] = score * 100
        result.append(d)
    return result
