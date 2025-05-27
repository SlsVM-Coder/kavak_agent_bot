# app/api/routes_whatsapp.py

from fastapi import APIRouter, Form, Depends, Response
from twilio.twiml.messaging_response import MessagingResponse
from app.dependencies.openai_client import get_openai_client, OpenAIClient
from app.services.whatsapp_service import WhatsAppService

router = APIRouter()


@router.post("/")
async def receive_message(
    from_number: str = Form(..., alias="From"),
    body_text:   str = Form(..., alias="Body"),
    ai_client:   OpenAIClient = Depends(get_openai_client),
):
    service = WhatsAppService(ai_client)
    reply = service.handle_message(body_text)

    twiml = MessagingResponse()
    twiml.message(reply)
    return Response(content=str(twiml), media_type="application/xml")
