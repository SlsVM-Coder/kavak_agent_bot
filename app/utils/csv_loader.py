import pandas as pd
from pathlib import Path

def load_catalog() -> pd.DataFrame:
    """
    lee el catalgo de autos desde data/catalog.csv
    y lo devuelve como DataFrame.
    """
    path = Path(__file__).parent.parent.parent / "data" / "catalog.csv"
    return pd.read_csv(path)