from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: datetime


class TokenPayload(BaseModel):
    sub: Optional[UUID] = None
