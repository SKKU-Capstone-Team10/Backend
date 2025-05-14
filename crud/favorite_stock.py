from uuid import UUID, uuid4
from typing import List

from sqlmodel import Session, select

from models import FavoriteStock
from schemas.stock import *

def create_fav_stock(db: Session, user_id: UUID, ticker: str) -> FavoriteStock:
    new_fav = FavoriteStock(
        user_id=user_id,
        ticker=ticker.upper()
    )
    db.add(new_fav)
    db.commit()
    db.refresh(new_fav)
    return new_fav

def read_fav_stock(db: Session, user_id: UUID, ticker: str) -> FavoriteStock:
    statement = select(FavoriteStock).where(
            FavoriteStock.user_id == user_id,
            FavoriteStock.ticker == ticker.upper()
        )
    fav_stock = db.exec(statement).first()
    return fav_stock

def fetch_fav_stocks(db: Session, user_id: UUID):
    statement = select(FavoriteStock.ticker).where(FavoriteStock.user_id == user_id)
    fav_stocks = db.exec(statement)
    return fav_stocks

def delete_fav_stock(db: Session, fav_stock: FavoriteStock) -> bool:
    try:
        db.delete(fav_stock)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        print(f"[delete_session] ERROR: {e}")
        return False