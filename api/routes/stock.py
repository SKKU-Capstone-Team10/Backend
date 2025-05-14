from typing import List, Dict, Any

from fastapi import APIRouter, HTTPException

from core.db import SessionDep
from core.auth import CurrentUser

from models import Stock, FavoriteStock
from schemas.stock import StockResponse

from crud.stock import create_stock, read_stock, update_stock_price
from crud.favorite_stock import create_fav_stock, read_fav_stock, fetch_fav_stocks, delete_fav_stock
import yfinance as yf

router = APIRouter(prefix='/stock', tags=['Stock'])


@router.get('/{ticker}/short', response_model=StockResponse)
def get_stock(db: SessionDep, ticker: str):
    # Get Price from yfinance
    tkr = yf.Ticker(ticker)
    price = tkr.info.get('regularMarketPrice')

    # Check if the stock exist in DB
    stock = read_stock(db, ticker)
    if stock: # If so, update the price
        stock = update_stock_price(db, stock, price)
    else: # If not, insert into DB
        name = tkr.info.get('longName')
        stock = create_stock(db, ticker, name, price)
    
    return stock

@router.post("/{ticker}/favorite", response_model=StockResponse)
def add_favorite_stock(db: SessionDep, ticker: str, current_user: CurrentUser):
    # Check if the stock exist in DB
    stock = read_stock(db, ticker)
    tkr = yf.Ticker(ticker)
    price = tkr.info.get("regularMarketPrice")
    if stock:
        stock = update_stock_price(db, stock, price)
    else:
        name = tkr.info.get("longName")
        stock = create_stock(db, ticker, name, price)

    # Check if it already in favorite stock DB
    fav_stock = read_fav_stock(db, current_user.id, stock.ticker)
    if fav_stock:
        raise HTTPException(
            status_code=400,
            detail=f"'{ticker}' is already in favorite stock list"
        )

    # Add to Favorite Stock DB
    fav = create_fav_stock(db, current_user.id, stock.ticker)
    if not fav:
        raise HTTPException(
            status_code=500,
            detail=f"Favorite '{ticker}' Failed"
        )

    return stock

@router.get("/fetch/favorites", response_model=List[StockResponse])
def fetch_favorite_stocks(db: SessionDep, current_user: CurrentUser):
    fav_stock_tickers = fetch_fav_stocks(db, current_user.id)
    fav_stocks = []

    for ticker in fav_stock_tickers:
        stock = read_stock(db, ticker)
        fav_stocks.append(stock)
    
    return fav_stocks