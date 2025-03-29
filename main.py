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
from core.db import create_db_and_tables
def on_startup():
    create_db_and_tables()
# <<<<< Local Database Config