from datetime import datetime

from pydantic import BaseModel


class Celebrity(BaseModel):
    pk: int
    name: str
    description: str
    created: datetime = datetime.now()
