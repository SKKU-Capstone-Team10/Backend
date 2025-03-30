from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, field_validator, EmailStr
from pydantic_core.core_schema import FieldValidationInfo

# Request Type
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password1: str
    password2: str
    class Config():
        from_attributes = True
    
    @field_validator('username', 'email', 'password1', 'password1', 'email')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("Empty field not allowed.")
        return v
    
    @field_validator('password2')
    def passwords_match(cls, v, info: FieldValidationInfo):
        if 'password1' in info.data and v != info.data['password1']:
            raise ValueError("Passwords are differents.")
        return v

# Request Body for updating username
class UserUpdateUsername(BaseModel):
    id: UUID
    username: str
    password: str
    class Config():
        from_attributes = True

# Request Body for updating password
class UserUpdatePassword(BaseModel):
    id: UUID
    current_password: str
    new_password: str
    class Config():
        from_attributes = True

# Response Type
class UserPublic(BaseModel):
    id: UUID
    email: EmailStr
    username: str
    created_at: datetime
    class Config():
        from_attributes = True