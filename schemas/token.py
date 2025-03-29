from uuid import UUID
from pydantic import BaseModel

# JWT return type
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Parsing Requested Token
class TokenPayload(BaseModel):
    sub: UUID | None = None