from pydantic import BaseModel

class WhatsAppMessage(BaseModel):
    From: str
    Body: str