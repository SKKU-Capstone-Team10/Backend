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