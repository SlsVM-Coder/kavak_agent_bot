from app.services.handlers.greeting_handler import GreetingHandler
from app.services.session_manager import SessionManager, State


class DummyLLM:
    # El handler de saludo usa chat_user y espera un string
    def chat_user(self, *args, **kwargs):
        return "Hola test"
    # Fallback handlers pueden usar chat(...) si los pruebas, pero no es obligatorio aquí

    def chat(self, *args, **kwargs):
        return None


def test_greeting_starts_session():
    sessions = SessionManager()
    h = GreetingHandler()
    out = h.handle("user1", "", sessions, DummyLLM())
    assert "Hola" in out.text
    assert sessions.get_state("user1") == State.AWAITING_OPTION
