from pydantic import BaseModel
from typing import Optional


class Tweet(BaseModel):
    tweet: Optional[str]
    text: Optional[str]
