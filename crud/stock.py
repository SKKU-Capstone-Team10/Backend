from uuid import UUID, uuid4
from typing import Any, List

from sqlmodel import Session, select

from models import Stock, FavoriteStock
from schemas.stock import *

def create_stock(db: Session) -> Any:
    pass