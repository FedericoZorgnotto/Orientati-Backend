# services/email.py
import ssl

import aiosmtplib
from email.message import EmailMessage
from email.utils import formataddr

import certifi
from fastapi.templating import Jinja2Templates
from app.core.config import Settings
from app.services.email_queue import enqueue_email

templates = Jinja2Templates(directory="app/templates/emails")


class Mailer:
    def __init__(self):
        self._settings = Settings()

    async def _send_message_now(self, subject: str, recipient: str, html_body: str):
        try:
            print(f"Sending email to {recipient} with subject '{subject}'")
            msg = EmailMessage()
            msg["From"] = formataddr((self._settings.MAIL_FROM_NAME, self._settings.MAIL_FROM_ADDRESS))
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.set_content("Se il client non supporta HTML")
            msg.add_alternative(html_body, subtype="html")

            # Crea un contesto SSL con i certificati aggiornati
            ssl_context = ssl.create_default_context(cafile=certifi.where())

            await aiosmtplib.send(
                msg,
                hostname=self._settings.SMTP_HOST,
                port=self._settings.SMTP_PORT,
                username=self._settings.SMTP_USER,
                password=self._settings.SMTP_PASSWORD,
                start_tls=True,
                tls_context=ssl_context,  # <-- aggiunto qui
            )
        except Exception as e:
            print(f"Error sending email: {e}")

    async def send_message(self, subject: str, recipient: str, html_body: str):
        # Metti l'email in coda, verrà gestita dal worker
        await enqueue_email(self._send_message_now, subject, recipient, html_body)

    async def send_template(self, schema):
        template = templates.get_template(schema.template_name)
        html = template.render(**schema.context)
        await self.send_message(schema.subject, schema.recipient, html)
