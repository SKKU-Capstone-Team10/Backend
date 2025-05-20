from typing import Annotated
from uuid import UUID
from sqlmodel import SQLModel, create_engine, Session
from fastapi import Depends, HTTPException
from core.config import settings
from models import *

DATABASE_URL = "sqlite:///./local_database.db"
engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session

def parse_uuid(id: str):
    try:
        uid = UUID(id)
    except ValueError:
        hex32 = id.strip()
        if len(hex32) == 32:
            formatted = f"{hex32[0:8]}-{hex32[8:12]}-{hex32[12:16]}-{hex32[16:20]}-{hex32[20:32]}"
            try:
                uid = UUID(formatted)
            except ValueError:
                raise HTTPException(status_code=422, detail="Invalid UUID format")
        else:
            raise HTTPException(status_code=422, detail="Invalid UUID format")
    return uid

SessionDep = Annotated[Session, Depends(get_db)]
UuidDep = Annotated[str, Depends(parse_uuid)]