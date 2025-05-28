from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent

TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

CATALOG_CSV_PATH = (BASE_DIR / "data" / "catalog.csv").resolve()
if not CATALOG_CSV_PATH.is_file():
    raise FileNotFoundError(f"catalog.csv no encontrado en {CATALOG_CSV_PATH}")
