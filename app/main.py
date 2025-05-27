from fastapi import FastAPI
from app.api.routes_whatsapp import router as whatsapp_router

app = FastAPI(title="Kavak Agent Bot")
app.include_router(whatsapp_router, prefix="/whatsapp", tags=["WhatsApp"])

@app.get("/health")
async def healt():
    return {"status": "ok"}