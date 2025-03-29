from pydantic import BaseModel

# Response Message type
class Message(BaseModel):
    message: str