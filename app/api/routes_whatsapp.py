from fastapi import APIRouter, Form, Depends, Response
from twilio.twiml.messaging_response import MessagingResponse

from app.dependencies.openai_client import get_openai_client
from app.services.session_manager import SessionManager
from app.services.whatsapp_service import WhatsAppService

router = APIRouter(prefix="/whatsapp")
sessions = SessionManager()


@router.post("/")
async def receive_message(
    From: str = Form(...),
    Body: str = Form(...),
    ai_client=Depends(get_openai_client),
):
    service = WhatsAppService(ai_client, sessions)
    out_msg = service.handle_message(From, Body)
    reply_text = out_msg.text

    twiml = MessagingResponse()
    twiml.message(reply_text)
    return Response(content=str(twiml), media_type="application/xml")
