from sqlmodel import select
from core.db import SessionDep
from models import Stock, ETF, ETFStockLink

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

def setup_etf_records(db: SessionDep) -> None:
    tickers = [
        'SOXL', 'SOXS', 'SPY', 'SPXS', 'HYG', 'XLF', 'FXI', 'EWZ', 'PSLV', 'BKLN',
        'GDX', 'IWM', 'LQD', 'EEM', 'XLV', 'TZA', 'EWJ', 'SCHD', 'KWEB', 'FAZ',
        'ARKK', 'GLD', 'SPXD', 'RWM', 'SLV', 'XBI', 'TMF', 'UVXY', 'SRLN', 'SCHG'
    ]

    for ticker in tickers:
        exists = db.exec(select(ETF).where(ETF.ticker == ticker))
        if exists.first():
            continue # Pass already exist stock

        try:
            etf = yf.Ticker(ticker)
            price = etf.info.get('regularMarketPrice')
            name = etf.info.get('longName')
            data = {'ticker': ticker, 'name': name, 'price': price}
            db.add(ETF(**data))

            top_holdings = yf.Ticker(ticker).funds_data.top_holdings.index.to_list()
            for stock_tkr in top_holdings:
                if not db.exec(select(Stock).where(Stock.ticker == stock_tkr)).first():
                    db.add(Stock(ticker=stock_tkr))
                db.add(ETFStockLink(etf_ticker=ticker, stock_ticker=stock_tkr))
        except Exception:
            pass
    db.commit()