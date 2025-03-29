from typing import Annotated
from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends
from core.config import settings
from models import *

DATABASE_URL = settings.DATABASE_URI
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_db)]