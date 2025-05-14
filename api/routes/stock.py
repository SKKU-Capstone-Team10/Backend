from typing import Dict, Any

from fastapi import APIRouter, HTTPException

from core.db import SessionDep
from core.auth import CurrentUser

from models import Stock, FavoriteStock
from schemas.stock import StockResponse

from crud.stock import create_stock, read_stock, update_stock_price

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