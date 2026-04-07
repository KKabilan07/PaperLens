from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Message(BaseModel):
    role: str  # "user" or "assistant"
    content: str


class ChatBase(BaseModel):
    question: str
    paper_id: str


class ChatCreate(ChatBase):
    pass


class Chat(ChatBase):
    id: str
    user_id: str
    answer: Optional[str] = None
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    id: str
    question: str
    answer: Optional[str] = None
    paper_id: str
    created_at: Optional[str] = None


class ChatHistory(BaseModel):
    paper_id: str
    chats: List[ChatResponse] = []


class QuestionRequest(BaseModel):
    question: str
    paper_id: str


class QuestionResponse(BaseModel):
    success: bool
    answer: str
    chat_id: str
