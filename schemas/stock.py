from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class StockResponse(BaseModel):
    ticker: str
    name: Optional[str]
    price: Optional[float]
    class Config():
        from_attributes = True