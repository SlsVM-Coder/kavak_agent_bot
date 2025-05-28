# Kavak Agent Bot

Un chatbot de WhatsApp para Kavak que simula el comportamiento de un agente comercial, construido con FastAPI, Twilio Sandbox, y OpenAI GPT-4.  

---

## 📖 Documentación Online

Toda la arquitectura, prompts, guía de instalación y roadmap están disponibles aquí:

**▶️ [Ver documentación completa](https://kavak-docs-lr08mk5tn-slsvmcoders-projects.vercel.app/)**  

---

## 🎥 Videos de prueba

Los clips de la interacción real en tu Sandbox de Twilio de prueba se enviaran por correo debido al peso:

---

## 🚀 Cómo arrancar el proyecto

```bash
git clone https://github.com/SlsVM-Coder/kavak_agent_bot.git
cd kavak_agent_bot

# 1) Instala dependencias
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2) Variables de entorno
cp .env.example .env
# Edita .env con tus claves de OpenAI y Twilio

# 3) Levanta la API
uvicorn app.main:app --reload

# 4) Expón con ngrok (opcional)
ngrok http 8000

# 5) Configura tu webhook en Twilio Sandbox apuntando a:
#    https://<tu-subdominio-ngrok>.ngrok-free.app/whatsapp/

# 6) ¡Prueba enviando “Hola” por WhatsApp!
