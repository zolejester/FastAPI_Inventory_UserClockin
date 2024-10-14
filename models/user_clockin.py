from pydantic import BaseModel
from datetime import datetime


class ClockInRecord(BaseModel):
    email: str
    location: str
    clockin: datetime = datetime.now()
