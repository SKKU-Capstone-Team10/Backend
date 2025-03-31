from uuid import UUID
from typing import Any

from fastapi import APIRouter, HTTPException

from core.db import SessionDep
from core.auth import CurrentUser, verify_password

from schemas.user import (
    UserCreate,
    UserUpdateUsername,
    UserUpdatePassword,
    UserDelete,
    UserPublic
)
from schemas.message import Message

from crud.user import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    patch_password,
    delete_user
)


router = APIRouter(prefix="/user", tags=['User'])

# Create a user
@router.post('/register', response_model=UserPublic)
def register_user(db: SessionDep, req: UserCreate):
    """
    Create new user.
    """
    user = get_user_by_email(db, req.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists.",
        )

    # Password length check
    # Password rule?

    user = create_user(db, req)
    # Send Email authentication number

    return user
# Get current login user using token
@router.get('/me', response_model=UserPublic)
def read_user_me(current_user: CurrentUser) -> Any:
    return current_user

# Read a user by id
@router.get('/{id}', response_model=UserPublic)
def read_user_by_id(db: SessionDep, id: UUID, current_user: CurrentUser) -> Any:
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
@router.patch('/username', response_model=Message)
def update_username(
    db: SessionDep,
    current_user: CurrentUser,
    req: UserUpdateUsername
) -> Any:
    # Check if Requested UUID is Current User
    if str(current_user.id) != str(req.id):
        raise HTTPException(status_code=403, detail="Users can update only themselves.")
    # Check if Requested Password is valid.
    if not verify_password(req.password, current_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    # Read user
    user = get_user_by_id(db, req.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Patch the username
    user.username = req.username
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        print(f"[update_username] ERROR: {e}")
        raise HTTPException(status_code=500, detail="Update Failed.")

    return Message(message="Updated successfully.")

# Update password
@router.patch('/password', response_model=Message)
def update_password(
    db: SessionDep,
    current_user: CurrentUser,
    req: UserUpdatePassword
) -> Any:
    # Check if Requested UUID is Current User
    if str(current_user.id) != str(req.id):
        raise HTTPException(status_code=403, detail="Users can update only themselves.")
    # Check if Requested Password is valid.
    if not verify_password(req.current_password, current_user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    # Read user
    user = get_user_by_id(db, req.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Patch the password
    success = patch_password(db, user, req.new_password1)
    if not success: # Failed to write in DB
        raise HTTPException(status_code=500, detail="Password update failed. Check server log.")

    return Message(message="Updated successfully.")

# Delete user
@router.delete('/', response_model=Message)
def delete_user_by_id(db: SessionDep, current_user: CurrentUser, req: UserDelete) -> Any:
    user = get_user_by_id(db, req.id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user != current_user:
        raise HTTPException(
            status_code=403, detail="Users can delete only themselves."
        )
    if not verify_password(req.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    
    delete_user(db, user) # Cascade delete chat session -> chat

    return Message(message="User deleted successfully")

