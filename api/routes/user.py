from uuid import UUID
from typing import Any

from fastapi import APIRouter, HTTPException

from core.db import SessionDep
from core.auth import CurrentUser, verify_password

from schemas.user import (
    UserCreate,
    UserUpdateUsername,
    UserRead
)
from schemas.message import Message

from crud.user import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    delete_user
)


router = APIRouter(prefix="/user", tags=['User'])

# Create a user
@router.post('/register', response_model=UserRead)
def register_user(db: SessionDep, req: UserCreate):
    """
    Create new user.
    """
    # user = get_user_by_email()
    # if user:
    #     raise HTTPException(
    #         status_code=400,
    #         detail="The user with this email already exists in the system.",
    #     )

    user = create_user(db, req)
    # Send Email authentication number

    return user

@router.get('/me', response_model=UserRead)
def read_user_me(current_user: CurrentUser) -> Any:
    """
    Get current user using token
    """
    return current_user

# Read a user by id
@router.get('/{id}', response_model=UserRead)
def read_user_by_id(db: SessionDep, id: UUID, current_user: CurrentUser):
    user = get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user != current_user:
        raise HTTPException(
            status_code=403,
            detail="Users can read only themselves. Use /api/user/me instead."
        )
    return user


# Update username
@router.patch('/{id}', response_model=Message)
def update_username(
    db: SessionDep,
    id: UUID,
    current_user: CurrentUser,
    req: UserUpdateUsername
) -> Any:
    # Check if Requested Password is valid.
    if not verify_password(req.password, current_user.password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    # Check if Requested UUID is Current User
    if str(current_user.id) != str(id):
        raise HTTPException(status_code=403, detail="Users can update only themselves.")
    
    # Read user
    user = get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Patch the username
    user.username = req.username
    db.add(user)
    db.commit()
    db.refresh(user)

    return Message(message="Updated successfully.")

# Delete user
@router.delete('/{id}', response_model=Message)
def delete_user_by_id(db: SessionDep, id: UUID, current_user: CurrentUser):
    user = get_user_by_id(db, id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user != current_user:
        raise HTTPException(
            status_code=403, detail="Users can delete only themselves."
        )
    
    delete_user(db, user)
    # Cascade delete chat session -> chat

    return Message(message="User deleted successfully")

