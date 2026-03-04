from fastapi import FastAPI, HTTPException, Form
from email_service import EmailService
from datetime import datetime

app = FastAPI()
email_service = EmailService()

@app.get("/")
def read_root():
    return {"Hello": "World from pythonapp"}

@app.post("/send-email")
async def send_email(text: str = Form(...)):
    """
    Envoie un texte par email à l'adresse par défaut (efatim443@gmail.com).
    """
    print(f"DEBUG: Tentative d'envoi d'email avec le texte : {text[:20]}...")
    success = email_service.send_text_email(text)
    
    if success:
        return {"status": "success", "message": "Email envoyé avec succès"}
    else:
        raise HTTPException(status_code=500, detail="Erreur lors de l'envoi de l'email")

if __name__ == "__main__":
    import uvicorn
    import os
    host = os.getenv("APP_HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8001"))
    uvicorn.run(app, host=host, port=port)
