from uuid import UUID, uuid4
from typing import Any, List

from sqlmodel import Session, select

from models import Stock, FavoriteStock
from schemas.stock import *

def create_stock(db: Session, ticker: str, name: str, price: float) -> None:
    new_stock = Stock(
        ticker=ticker,
        name=name,
        price=price
    )

    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)

    return new_stock

def read_stock(db: Session, ticker: str) -> Stock | None:
    statement = select(Stock).where(Stock.ticker == ticker)
    stock = db.exec(statement).first()
    return stock

def update_stock_price(db: Session, stock: Stock, price: float) -> Stock:
    stock.price = price
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock