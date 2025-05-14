from typing import Dict, Any

from fastapi import APIRouter, HTTPException

import yfinance as yf

router = APIRouter(prefix='/stock', tags=['Stock'])


