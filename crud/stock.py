from uuid import UUID, uuid4
from typing import Dict, Any, List

from sqlmodel import Session, select
from fastapi import HTTPException
from concurrent.futures import ThreadPoolExecutor, as_completed

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

# Excute yf api call in parallel
executor = ThreadPoolExecutor()

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
        fut_history = executor.submit(get_history, ticker, period, interval)
        fut_dividends = executor.submit(get_dividends, ticker)
        fut_splits = executor.submit(get_splits, ticker)
        fut_earnings = executor.submit(get_earning_calendar, ticker)
        fut_news = executor.submit(get_news, ticker)

        stmt = select(ETFStockLink.etf_ticker).where(ETFStockLink.stock_ticker == ticker)
        related_etfs = db.exec(stmt)

        etf_futures = {}
        if related_etfs:
            for etf in related_etfs:
                etf_futures[etf] = executor.submit(get_history, etf, period, interval)

        history         = fut_history.result()
        dividends       = fut_dividends.result()
        splits          = fut_splits.result()
        earning_calendar= fut_earnings.result()
        news            = fut_news.result()

        related_etfs_info = {
            etf: fut.result()
            for etf, fut in etf_futures.items()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detailed Fetch '{ticker}'Failed: {e}")
    
    return {
        'history': history,
        'dividends': dividends,
        'splits': splits,
        'earning_calendar': earning_calendar,
        'related_etfs': related_etfs_info,
        'news': news
    }

def update_stock_price(db: Session, stock: Stock) -> Stock:
    stock.price = get_price(stock.ticker)
    db.add(stock)
    db.commit()
    db.refresh(stock)
    return stock