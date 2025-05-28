from app.services.session_manager import State
from app.services.handlers.greeting_handler import GreetingHandler
from app.services.handlers.option_handler import OptionHandler
from app.services.handlers.car_details_handler import CarDetailsHandler
from app.services.handlers.selection_handler import SelectionHandler
from app.services.handlers.finance_confirm_handler import FinanceConfirmHandler
from app.services.handlers.down_payment_choice_handler import DownPaymentChoiceHandler
from app.services.handlers.down_payment_value_handler import DownPaymentValueHandler
from app.services.handlers.term_handler import TermHandler
from app.services.handlers.fallback_handler import FallbackHandler
from app.services.llm_service import LLMService


class WhatsAppService:
    def __init__(self, ai_client, sessions):
        self.sessions = sessions
        self.llm_service = LLMService(ai_client)
        self.handlers = {
            State.GREETING:                    GreetingHandler(),
            State.AWAITING_OPTION:             OptionHandler(),
            State.AWAITING_CAR_DETAILS:        CarDetailsHandler(),
            State.AWAITING_CAR_SELECTION:      SelectionHandler(),
            State.AWAITING_FINANCE_CONFIRM:    FinanceConfirmHandler(),
            State.AWAITING_DOWN_PAYMENT_CHOICE: DownPaymentChoiceHandler(),
            State.AWAITING_DOWN_PAYMENT_VALUE: DownPaymentValueHandler(),
            State.AWAITING_TERM:               TermHandler(),
        }
        self.fallback = FallbackHandler()

    def handle_message(self, user_id: str, text: str) -> str:
        state = self.sessions.get_state(user_id) or State.GREETING
        handler = self.handlers.get(state, self.fallback)
        return handler.handle(user_id, text, self.sessions, self.llm_service)
