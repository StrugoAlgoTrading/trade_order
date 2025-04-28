from pydantic import BaseModel
from typing import Optional


class Event(BaseModel):
    event_type: str
    ticker: str
    time: str
    context: str
