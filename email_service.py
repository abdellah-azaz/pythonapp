import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate, make_msgid
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
ENV_PATH = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

class EmailService:
    def __init__(self):
        self.host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
        self.port = int(os.environ.get("SMTP_PORT", "587"))
        self.user = os.environ.get("SMTP_USER", "")
        self.password = os.environ.get("SMTP_PASS", "")
        self.default_recipient = os.environ.get("RECIPIENT_EMAIL", "efatim443@gmail.com")
        self.from_name = os.environ.get("EMAIL_FROM_NAME", "PythonApp Service")
        self.subject = os.environ.get("EMAIL_SUBJECT", "Notification automatique - PythonApp")

    def send_text_email(self, content: str, recipient: str = None):
        """
        Envoie un email simple avec le contenu textuel fourni.
        """
        if not recipient:
            recipient = self.default_recipient

        if not self.user or not self.password:
            print("Erreur: SMTP_USER ou SMTP_PASS non configuré dans .env")
            return False

        # Création du message
        message = MIMEMultipart("alternative")
        message["From"] = f"{self.from_name} <{self.user}>"
        message["To"] = recipient
        message["Subject"] = self.subject
        message["Date"] = formatdate(localtime=True)
        message["Message-ID"] = make_msgid()
        message["Auto-Submitted"] = "auto-generated"

        # Version texte brut
        text_plain = f"""
        Bonjour,

        Vous avez reçu une nouvelle notification de PythonApp :

        --------------------------------------------------
        {content}
        --------------------------------------------------

        Ceci est un message automatique, merci de ne pas y répondre.
        """

        # Version HTML
        text_html = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; border: 1px solid #ddd; padding: 20px; border-radius: 8px;">
              <h2 style="color: #4285F4;">Nouvelle Notification</h2>
              <p>Bonjour,</p>
              <p>Le message suivant a été envoyé via PythonApp :</p>
              <div style="background-color: #f8f9fa; border-left: 4px solid #4285F4; padding: 15px; margin: 20px 0; font-family: monospace; white-space: pre-wrap;">
                {content}
              </div>
              <p style="font-size: 12px; color: #777; border-top: 1px solid #eee; padding-top: 10px; margin-top: 20px;">
                Ceci est un message généré automatiquement.
              </p>
            </div>
          </body>
        </html>
        """

        message.attach(MIMEText(text_plain, "plain", "utf-8"))
        message.attach(MIMEText(text_html, "html", "utf-8"))

        try:
            print(f"DEBUG: Tentative d'envoi via {self.host}:{self.port} avec l'utilisateur {self.user}...")
            with smtplib.SMTP(self.host, self.port) as server:
                server.set_debuglevel(1)  # Active les logs détaillés de la conversation SMTP
                print("DEBUG: Connexion établie, passage en TLS...")
                server.starttls()
                print("DEBUG: Authentification en cours...")
                server.login(self.user, self.password)
                print("DEBUG: Envoi du message...")
                server.send_message(message)
            print(f"Email envoyé avec succès à {recipient}")
            return True
        except Exception as e:
            print(f"ERREUR CRITIQUE lors de l'envoi de l'email : {type(e).__name__}: {e}")
            return False
