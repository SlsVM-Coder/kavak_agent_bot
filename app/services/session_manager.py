from enum import Enum
from typing import Dict, Any


class State(str, Enum):
    GREETING = "GREETING"
    AWAITING_OPTION = "AWAITING_OPTION"
    AWAITING_CAR_DETAILS = "AWAITING_CAR_DETAILS"
    AWAITING_CAR_SELECTION = "AWAITING_CAR_SELECTION"
    AWAITING_FINANCE_CONFIRM = "AWAITING_FINANCE_CONFIRM"      # Confirmación Sí/No
    AWAITING_DOWN_PAYMENT_CHOICE = "AWAITING_DOWN_PAYMENT_CHOICE"  # Elige A–E
    AWAITING_DOWN_PAYMENT_VALUE = "AWAITING_DOWN_PAYMENT_VALUE"   # Ingresa % o cantidad
    AWAITING_TERM = "AWAITING_TERM"                 # Plazo 3–6 años


class SessionManager:
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    def start(self, user_id: str):
        self._store[user_id] = {"state": State.GREETING, "data": {}}

    def get_state(self, user_id: str):
        return self._store.get(user_id, {}).get("state")

    def set_state(self, user_id: str, state: State):
        self._store.setdefault(user_id, {"data": {}})["state"] = state

    def get_data(self, user_id: str) -> Dict[str, Any]:
        return self._store.setdefault(user_id, {"state": State.GREETING, "data": {}})["data"]

    def clear(self, user_id: str):
        self._store.pop(user_id, None)
