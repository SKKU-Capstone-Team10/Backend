from uuid import UUID, uuid4
from typing import List

from sqlmodel import Session, select

from models import FavoriteStock
from schemas.stock import *

def create_fav_stock(db: Session, user_id: UUID, stock_id: UUID) -> FavoriteStock:
    new_fav = FavoriteStock(
        user_id=user_id,
        stock_id=stock_id
    )
    db.add(new_fav)
    db.commit()
    db.refresh(new_fav)
    return new_fav

def read_fav_stock(db: Session, user_id: UUID, stock_id: UUID) -> FavoriteStock:
    statement = select(FavoriteStock).where(
            FavoriteStock.user_id == user_id,
            FavoriteStock.stock_id == stock_id
        )
    fav_stock = db.exec(statement).first()
    return fav_stock

def fetch_fav_stock():
    pass

def delete_fav_stock():
    pass