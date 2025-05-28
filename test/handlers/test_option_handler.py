from app.services.handlers.option_handler import OptionHandler
from app.services.session_manager import SessionManager, State


def test_option_a_leads_car_details():
    sessions = SessionManager()
    sessions.start("u")
    sessions.set_state("u", State.AWAITING_OPTION)
    h = OptionHandler()
    out = h.handle("u", "A", sessions, None)
    assert "Marca, Modelo, Año" in out.text
    assert sessions.get_state("u") == State.AWAITING_CAR_DETAILS
