from contextlib import asynccontextmanager # fastapi lifespan

from fastapi import FastAPI

from api.router import api_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    on_startup() # create local database
    yield
    pass

# execute the server: uvicorn fileName:instanceName --reload
app = FastAPI(lifespan=lifespan) # Call lifespan function
# /docs : Swagger
# /redoc : ReDoc

@app.get('/') # Greeting Page
def root():
    return {'message': "Capstone Team 10 Backend"}

# Include api routers
app.include_router(api_router, prefix='/api')

# >>>>> Local Database Config
from sqlmodel import Session
from core.db import create_db_and_tables, engine
from core.setup import (
    setup_stock_records,
    setup_etf_records,
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