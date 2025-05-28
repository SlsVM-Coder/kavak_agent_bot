from fastapi import FastAPI
from app.api.routes_whatsapp import router as whatsapp_router

app = FastAPI(title="Kavak Agent Bot", version="1.0.0")
app.include_router(whatsapp_router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
