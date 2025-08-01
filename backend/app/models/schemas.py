from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Segment(BaseModel):
    timestamp: float
    text: str

class TranscriptionRequest(BaseModel):
    url: str
    topics: List[str]

class TranscriptionResponse(BaseModel):
    jobId: str

class TranscriptionStatus(BaseModel):
    status: str  # pending, processing, completed, failed
    progress: int
    message: Optional[str] = None

class TranscriptionResult(BaseModel):
    segments: List[Segment]

class NoteBase(BaseModel):
    title: str
    tags: List[str]
    segments: List[Segment]
    source_url: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    tags: Optional[List[str]] = None

class Note(NoteBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str
    username: Optional[str] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True 