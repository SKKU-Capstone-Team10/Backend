from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from core.db import SessionDep
from models import Stock

def setup_stock_records(db: SessionDep) -> None:
    initial = [{"ticker": "AAPL",   "name": "Apple Inc.", "current_price": 180.0}]

    for data in initial:
        exists = db.exec(
            select(Stock).where(Stock.ticker == data["ticker"])
        )
        if not exists.first():
            pass
    db.commit()