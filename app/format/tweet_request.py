from pydantic import BaseModel
from typing import Optional


class Tweet(BaseModel):
    event_type: str
    ticker: str
    time: str
