# schemas/email.py
from typing import Dict

from pydantic import BaseModel


class SendEmailSchema(BaseModel):
    subject: str
    recipient: str
    template_name: str
    context: Dict[str, str] = {}
