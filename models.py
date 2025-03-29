import uuid
from datetime import datetime, timezone
from typing import Optional, Literal, List

from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str
    password: str
    username: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # 관계 정의: 유저는 여러 채팅 세션을 가질 수 있음
    chat_sessions: List["ChatSession"] = Relationship(back_populates="user")

class ChatSession(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    title: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # 관계 정의
    user: "User" = Relationship(back_populates="chat_sessions")
    chats: List["Chat"] = Relationship(back_populates="session")

class Chat(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    session_id: uuid.UUID = Field(foreign_key="chatsession.id")
    sender: Literal["user", "host"]
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # 관계 정의
    session: Optional["ChatSession"] = Relationship(back_populates="chats")