from pydantic import BaseModel
from datetime import datetime


class Item(BaseModel):
    name: str
    email: str
    itemName: str
    quantity: int
    expiry_date: datetime
    insert_date: datetime = datetime.now()
