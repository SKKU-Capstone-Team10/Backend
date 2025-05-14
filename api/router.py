from fastapi import APIRouter
from api.routes import auth, user, chat, chat_session, stock

api_router = APIRouter() # imported by ~/main.py
api_router.include_router(auth.router) # realted to token
api_router.include_router(user.router) # user routes
api_router.include_router(chat.router) # chat routes
api_router.include_router(chat_session.router) # chat session routes
api_router.include_router(stock.router)