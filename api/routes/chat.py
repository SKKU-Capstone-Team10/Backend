from fastapi import APIRouter, HTTPException

from models import (
    Chat
)

router = APIRouter(prefix="/chat", tags=['Chat'])

# Initial chat -> Create a new Chat Session
@router.post('/initial')
def init_chat():
    return "tmp"

# New Chat
@router.post('/')
def upload_chat():
    return "tmp"