from uuid import UUID, uuid4
from typing import Any, List

from sqlmodel import Session, select

from models import Stock, FavoriteStock
from schemas.stock import *

from api.functions.yf_api import get_price, get_name

def create_stock(db: Session, ticker: str) -> None:
    ticker = ticker.upper()
    new_stock = Stock(
        ticker=ticker,
        name=get_name(ticker),
        price=get_price(ticker)
    )

    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)

    return new_stock

def read_stock(db: Session, ticker: str) -> Stock | None:
    ticker = ticker.upper()
    statement = select(Stock).where(Stock.ticker == ticker)
    stock = db.exec(statement).first()
    
    if stock:
        stock.price = get_price(ticker)
        db.add(stock)
        db.commit()
        db.refresh(stock)

    return stock

def update_stock_price(db: Session, stock: Stock) -> Stock:
    stock.price = get_price(stock.ticker)
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock