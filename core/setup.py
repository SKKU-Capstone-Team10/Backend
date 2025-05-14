from sqlmodel import select
from core.db import SessionDep
from models import Stock

import yfinance as yf

def setup_stock_records(db: SessionDep) -> None:
    tickers = [
        'MSFT', 'AAPL', 'NVDA', 'AMZN', 'GOOG', 'META', 'SOFI', 'AVGO', 'TSLA', 'WMT',
        'JPM', 'LLY', 'V', 'MA', 'NFLX', 'XOM', 'ORCL', 'COST', 'PG', 'HD',
        'JNJ', 'BAC', 'ABBV', 'BABA', 'PLTR', 'KO', 'UNH', 'CRM', 'HOOD', 'TMUS'
    ]

    for ticker in tickers:
        exists = db.exec(select(Stock).where(Stock.ticker == ticker))
        if exists.first():
            continue # Pass already exist stock
        
        tkr = yf.Ticker(ticker)
        price = tkr.info.get('regularMarketPrice')
        name = tkr.info.get('longName')
        data = {'ticker': ticker, 'name': name, 'price': price}
        db.add(Stock(**data))
    db.commit()