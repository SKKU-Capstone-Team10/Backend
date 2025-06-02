from contextlib import asynccontextmanager # fastapi lifespan

from fastapi import FastAPI

from api.router import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Create local database if not exist.
    Insert stock and ETF records into the database.
    """
    on_startup()
    yield
    pass

# execute the server: uvicorn fileName:instanceName --reload
app = FastAPI(lifespan=lifespan) # Call lifespan function
# /docs : Swagger
# /redoc : ReDoc

# Greeting Page
@app.get('/')
def root():
    return {'message': "Capstone Team 10 Backend"}

# Include api routers
app.include_router(api_router, prefix='/api')

# >>>>> Local Database Config
from sqlmodel import Session
from core.db import create_db_and_tables, engine
from core.setup import (
    # Load Sotck and ETF from hard-coded small list
    setup_stock_records,
    setup_etf_records,
    # Load Sotck and ETF from CSV
    # Fetch information in parallel
    setup_stock_records_parallel,
    setup_etf_records_parallel
)

def on_startup():
    create_db_and_tables()
    with Session(engine) as db:
        # setup_stock_records(db)
        # setup_etf_records(db)
        setup_stock_records_parallel()
        setup_etf_records_parallel()
# <<<<< Local Database Config