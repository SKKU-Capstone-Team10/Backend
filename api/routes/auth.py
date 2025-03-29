from typing import Any, Annotated
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from core.config import settings
from core.auth import create_access_token, CurrentUser
from core.db import SessionDep

from schemas.user import UserRead
from schemas.token import Token

from crud.auth import authenticate

router = APIRouter(prefix="/auth", tags=['Authentification'])

@router.post('/login/access-token')
def login_access_token(
    db: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = authenticate(
        db=db,
        email=form_data.username,
        password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = Token(
        access_token=create_access_token(
            subject=user.id,
            expires_delta=access_token_expires
        )
    )
    return token

@router.post("/login/test-token", response_model=UserRead)
def test_token(current_user: CurrentUser) -> Any:
    """
    Test access token
    """
    return current_user