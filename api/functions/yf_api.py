from typing import List, Dict, Any
import yfinance as yf

def get_price(ticker: str) -> float:
    # Get Price from yfinance
    tkr = yf.Ticker(ticker)
    price = tkr.info.get('regularMarketPrice')
    
    return price

def get_name(ticker: str) -> str:
    # Get Name from yfinance
    tkr = yf.Ticker(ticker)
    name = tkr.info.get('longName')
    
    return name

def get_history(ticker: str, period: str, interval: str) -> Dict[str, List[str]]:
    tkr = yf.Ticker(ticker)
    history = tkr.history(period=period, interval=interval)
    if history.empty:
        return {}
    
    return history.reset_index().to_dict(orient="list")

def get_dividends(ticker: str) -> Dict[str, List[str]]:
    tkr = yf.Ticker(ticker)
    dividends = tkr.dividends
    if dividends.empty:
        return {}
    return dividends.reset_index().to_dict(orient="list")

def get_splits(ticker: str) -> Dict[str, List[str]]:
    tkr = yf.Ticker(ticker)
    splits = tkr.splits
    if splits.empty:
        return {}
    return splits.reset_index().to_dict(orient="list")

def get_earning_calendar(ticker: str):
    tkr = yf.Ticker(ticker)
    calendar = tkr.calendar
    if not calendar:
        return {}
    return calendar

def get_news(ticker: str) -> List[Dict[str, Any]]:
    tkr = yf.Ticker(ticker)
    news = []
    if hasattr(tkr, 'news'):
        news = tkr.news
    return news