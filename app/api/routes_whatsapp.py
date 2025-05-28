from fastapi import APIRouter, Form, Depends, Response
from twilio.twiml.messaging_response import MessagingResponse
from app.dependencies.openai_client import get_openai_client
from app.services.session_manager import SessionManager
from app.services.whatsapp_service import WhatsAppService

router = APIRouter()
sessions = SessionManager()


@router.post("/")
async def receive_message(
    From: str = Form(...),
    Body: str = Form(...),
    ai_client=Depends(get_openai_client),
):
    service = WhatsAppService(ai_client, sessions)
    reply = service.handle_message(From, Body)
    twiml = MessagingResponse()
    twiml.message(reply)
    return Response(str(twiml), media_type="application/xml")
