from enum import Enum


class State(str, Enum):
    GREETING = "GREETING"
    AWAITING_OPTION = "AWAITING_OPTION"
    AWAITING_CAR_DETAILS = "AWAITING_CAR_DETAILS"
    AWAITING_CAR_SELECTION = "AWAITING_CAR_SELECTION"
    AWAITING_FINANCE_CONFIRM = "AWAITING_FINANCE_CONFIRM"
    AWAITING_DOWN_PAYMENT_CHOICE = "AWAITING_DOWN_PAYMENT_CHOICE"
    AWAITING_DOWN_PAYMENT_VALUE = "AWAITING_DOWN_PAYMENT_VALUE"
    AWAITING_TERM = "AWAITING_TERM"


class SessionManager:
    def __init__(self):
        self.sessions: dict[str, dict] = {}

    def start(self, user_id: str):
        self.sessions[user_id] = {"state": State.GREETING, "data": {}}

    def get_state(self, user_id: str):
        return self.sessions.get(user_id, {}).get("state")

    def set_state(self, user_id: str, state: State):
        if user_id in self.sessions:
            self.sessions[user_id]["state"] = state

    def get_data(self, user_id: str) -> dict:
        return self.sessions.setdefault(user_id, {"state": None, "data": {}})["data"]

    def clear(self, user_id: str):
        self.sessions.pop(user_id, None)
