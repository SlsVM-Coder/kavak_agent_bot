from typing import Optional, Dict


class OutgoingMessage:
    def __init__(self, text: str, interactive: Optional[Dict] = None):
        # interactive queda siempre None en esta versión
        self.text = text
        self.interactive = interactive
