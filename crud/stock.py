from uuid import UUID, uuid4
from typing import Dict, Any, List

from sqlmodel import Session, select
from fastapi import HTTPException

from models import Stock, FavoriteStock, ETFStockLink
from schemas.stock import *

from pandas import DataFrame
from api.functions.yf_api import (
    get_price,
    get_name,
    get_history,
    get_dividends,
    get_splits,
    get_earning_calendar,
    get_news
)

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

def read_detailed_stock_information(db: Session, ticker: str, period: str='1mo', interval='1d') -> Dict:
    ticker = ticker.upper()
    try:
        history = get_history(ticker, period, interval)
        dividends = get_dividends(ticker)
        splits = get_splits(ticker)
        earning_calendar = get_earning_calendar(ticker)
        news = get_news(ticker)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detailed Fetch '{ticker}'Failed: {e}")
    
    statement = select(ETFStockLink.etf_ticker).where(ETFStockLink.stock_ticker == ticker)
    related_etfs = db.exec(statement)
    related_etfs_info = dict()
    if related_etfs:
        for etf in related_etfs:
            related_etfs_info[etf] = get_history(etf, period, interval)

    result = {
        'history': history,
        'dividends': dividends,
        'splits': splits,
        'earning_calendar': earning_calendar,
        'related_etfs': related_etfs_info,
        'news': news
    }
    return result

def update_stock_price(db: Session, stock: Stock) -> Stock:
    stock.price = get_price(stock.ticker)
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock