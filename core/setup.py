from typing import List, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
from sqlmodel import select, Session
from core.db import SessionDep, engine
from models import Stock, ETF, ETFStockLink

import yfinance as yf
from tqdm import tqdm

import pandas as pd

def setup_stock_records(db: SessionDep) -> None:
    """
    Check if the stock already exists in the database.
    If not, fetch the stock data from yfinance and insert it into the database.
    """
    tickers = [
        'MSFT', 'AAPL', 'NVDA', 'AMZN', 'GOOG', 'META', 'SOFI', 'AVGO', 'TSLA', 'WMT',
        'JPM', 'LLY', 'V', 'MA', 'NFLX', 'XOM', 'ORCL', 'COST', 'PG', 'HD',
        'JNJ', 'BAC', 'ABBV', 'BABA', 'PLTR', 'KO', 'UNH', 'CRM', 'HOOD', 'TMUS'
    ]

    loop = tqdm(tickers, desc="📈 Stocks setup")
    for ticker in loop:
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
    """
    Check if the ETF already exists in the database.
    If not, fetch the ETF data from yfinance and insert it into the database.
    Also, fetch the top holdings of the ETF and insert them into the ETFStockLink table.
    """
    tickers = [
        'SOXL', 'SOXS', 'SPY', 'SPXS', 'HYG', 'XLF', 'FXI', 'EWZ', 'PSLV', 'BKLN',
        'GDX', 'IWM', 'LQD', 'EEM', 'XLV', 'TZA', 'EWJ', 'SCHD', 'KWEB', 'FAZ',
        'ARKK', 'GLD', 'SPXD', 'RWM', 'SLV', 'XBI', 'TMF', 'UVXY', 'SRLN', 'SCHG'
    ]

    loop = tqdm(tickers, desc="📊 ETFs setup")
    for ticker in loop:
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

# Parallelized version with US stock and ETF data list
def _fetch_stock(ticker: str) -> Optional[Dict]:
    try:
        tkr = yf.Ticker(ticker)
        return {
            "ticker": ticker,
            "name":   tkr.info.get("longName"),
            "price":  tkr.info.get("regularMarketPrice"),
        }
    except Exception:   # 네트워크 오류 등
        return None


def _fetch_etf(ticker: str) -> Optional[Tuple[Dict, List[str]]]:
    try:
        etf = yf.Ticker(ticker)
        info = {
            "ticker": ticker,
            "name":   etf.info.get("longName"),
            "price":  etf.info.get("regularMarketPrice"),
        }
        holdings = etf.funds_data.top_holdings.index.to_list()
        return (info, holdings)
    except Exception:
        return None


def setup_stock_records_parallel() -> None:
    stock_df = pd.read_csv("core/data/stock.csv")
    tickers = stock_df["Symbol"].to_list()

    # ── 1) yfinance 병렬 호출 ───────────────────────────
    results: List[Dict] = []
    with ThreadPoolExecutor(max_workers=16) as ex:
        futures = {ex.submit(_fetch_stock, tkr): tkr for tkr in tickers}
        for fut in tqdm(as_completed(futures),
                        total=len(futures),
                        desc="📈 Stocks setup (fetch)"):
            data = fut.result()
            if data:   # None 이 아니면 성공
                results.append(data)

    # ── 2) DB 쓰기 (단일 세션) ───────────────────────────
    with Session(engine) as db:
        for data in tqdm(results,
                         desc="📈 Stocks setup (DB)"):
            exists = db.exec(
                select(Stock).where(Stock.ticker == data["ticker"])
            ).first()
            if exists:
                continue
            db.add(Stock(**data))
        db.commit()


def setup_etf_records_parallel() -> None:
    etf_df = pd.read_csv("core/data/etf.csv")
    tickers = etf_df["Symbol"].to_list()

    # ── 1) yfinance 병렬 호출 ───────────────────────────
    etf_results: List[Tuple[Dict, List[str]]] = []
    with ThreadPoolExecutor(max_workers=16) as ex:
        futures = {ex.submit(_fetch_etf, tkr): tkr for tkr in tickers}
        for fut in tqdm(as_completed(futures),
                        total=len(futures),
                        desc="📊 ETFs setup (fetch)"):
            res = fut.result()
            if res:
                etf_results.append(res)

    # ── 2) DB 쓰기 (단일 세션) ───────────────────────────
    with Session(engine) as db:
        for etf_info, holdings in tqdm(etf_results,
                                       desc="📊 ETFs setup (DB)"):
            ticker = etf_info["ticker"]

            if not db.exec(select(ETF).where(ETF.ticker == ticker)).first():
                db.add(ETF(**etf_info))

            for stock_tkr in holdings:
                # Stock 테이블에 없으면 먼저 insert
                if not db.exec(select(Stock).where(Stock.ticker == stock_tkr)).first():
                    db.add(Stock(ticker=stock_tkr))

                # ETFStockLink 는 중복 키(복합 PK 등)로 보호돼 있다고 가정
                if not db.exec(
                    select(ETFStockLink).where(
                        (ETFStockLink.etf_ticker == ticker) &
                        (ETFStockLink.stock_ticker == stock_tkr)
                    )
                ).first():
                    db.add(ETFStockLink(
                        etf_ticker=ticker,
                        stock_ticker=stock_tkr
                    ))

        db.commit()
