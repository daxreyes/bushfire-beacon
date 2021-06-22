from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class ByAtBase(BaseModel):
    created: Optional[datetime]
    updated: Optional[datetime]
    created_by_id: Optional[int]
    modified_by_id: Optional[int] = None
