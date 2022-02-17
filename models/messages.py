from datetime import datetime

from pydantic import BaseModel


class Message(BaseModel):
    user_pk: int
    celebrity_pk: int
    title: str
    created: datetime = datetime.now()
