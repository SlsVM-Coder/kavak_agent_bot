# app/services/recommendation_service.py

from typing import List, Dict
from rapidfuzz import process, fuzz
from app.utils.csv_loader import load_catalog


def recommend_cars(query: str, limit: int = 3) -> List[Dict]:
    """
    Top `limit` sugerencias más cercanas a `query`.
    """
    df = load_catalog()
    df["search_key"] = (
        df["make"].astype(str) + " "
        + df["model"].astype(str) + " "
        + df["year"].astype(str)
    )
    choices = process.extract(
        query,
        df["search_key"],
        scorer=fuzz.WRatio,
        limit=limit
    )
    results = []
    for match_text, score, idx in choices:
        row = df.iloc[idx]
        results.append({
            "stock_id": int(row["stock_id"]),
            "make":     row["make"],
            "model":    row["model"],
            "year":     int(row["year"]),
            "price":    float(row["price"]),
            "score":    score
        })
    return results


# app/services/recommendation_service.py


def find_exact_model_year(query: str, threshold: int = 80) -> List[Dict]:
    """
    Busca el mejor match global de make/model/year y, si supera el umbral,
    devuelve todas las filas del catálogo que tengan exactamente esos
    valores de make, model y year.
    """
    df = load_catalog()
    df["search_key"] = (
        df["make"].astype(str) + " "
        + df["model"].astype(str) + " "
        + df["year"].astype(str)
    )

    # 1) Extraemos el mejor match y su índice
    best_text, best_score, best_idx = process.extractOne(
        query,
        df["search_key"],
        scorer=fuzz.WRatio
    )

    # 2) Si no supera el umbral, devolvemos vacío
    if best_score < threshold:
        return []

    # 3) Tomamos la fila original para extraer make/model/year verdaderos
    best_row = df.iloc[best_idx]
    target_make = best_row["make"]
    target_model = best_row["model"]
    target_year = best_row["year"]

    # 4) Filtramos todas las filas que coincidan en esos tres campos
    mask = (
        (df["make"] == target_make) &
        (df["model"] == target_model) &
        (df["year"] == target_year)
    )
    matched_rows = df[mask]

    # 5) Convertimos a lista de dicts
    results: List[Dict] = []
    for _, row in matched_rows.iterrows():
        results.append({
            "stock_id": int(row["stock_id"]),
            "make":     row["make"],
            "model":    row["model"],
            "year":     int(row["year"]),
            "price":    float(row["price"]),
            "score":    best_score
        })
    return results
