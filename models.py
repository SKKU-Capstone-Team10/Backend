import uuid
from datetime import datetime, timezone
from typing import Optional, List
from enum import Enum

from sqlmodel import SQLModel, Field, Relationship

class Sender(str, Enum):
    user = "user"
    host = "host"

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str
    username: str
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # 관계 정의: 유저는 여러 채팅 세션을 가질 수 있음
    chat_sessions: List["ChatSession"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class ChatSession(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    title: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # 관계 정의
    user: "User" = Relationship(back_populates="chat_sessions")
    chats: List["Chat"] = Relationship(
        back_populates="session",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class Chat(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    session_id: uuid.UUID = Field(foreign_key="chatsession.id")
    sender: Sender
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # 관계 정의
    session: Optional["ChatSession"] = Relationship(back_populates="chats")