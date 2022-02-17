from datetime import datetime

from pydantic import BaseModel


class User(BaseModel):
    pk: int
    tg_id: int
    username: str
    description: str
    created: datetime = datetime.now()
