# schemas/email.py
from pydantic import BaseModel, EmailStr
from typing import Dict

class SendEmailSchema(BaseModel):
    subject: str
    recipient: str
    template_name: str
    context: Dict[str, str] = {}
