# services/email.py
import aiosmtplib
from email.message import EmailMessage
from email.utils import formataddr
from fastapi.templating import Jinja2Templates
from app.core.config import Settings

templates = Jinja2Templates(directory="app/templates/emails")


class Mailer:
    def __init__(self):
        self._settings = Settings()

    async def send_message(self, subject: str, recipient: str, html_body: str):
        try:
            msg = EmailMessage()
            msg["From"] = formataddr((self._settings.MAIL_FROM_NAME, self._settings.MAIL_FROM_ADDRESS))
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.set_content("Se il client non supporta HTML")  # TODO: gestire le email senza HTML
            msg.add_alternative(html_body, subtype="html")

            await aiosmtplib.send(
                msg,
                hostname=self._settings.SMTP_HOST,
                port=self._settings.SMTP_PORT,
                username=self._settings.SMTP_USER,
                password=self._settings.SMTP_PASSWORD,
                start_tls=True,
            )
        except Exception as e:
            print(f"Error sending email: {e}")

    async def send_template(self, schema):
        template = templates.get_template(schema.template_name)
        html = template.render(**schema.context)
        await self.send_message(schema.subject, schema.recipient, html)
