from uuid import UUID
from datetime import datetime
from pydantic import BaseModel

# Request Type
class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    class Config():
        from_attributes = True

# Request Body for updating username
class UserUpdateUsername(BaseModel):
    username: str
    password: str
    class Config():
        from_attributes = True

# Response Type
class UserRead(BaseModel):
    id: UUID
    email: str
    username: str
    created_at: datetime
    class Config():
        from_attributes = True