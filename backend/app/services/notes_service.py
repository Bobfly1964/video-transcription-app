from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import Note
from app.models.schemas import NoteCreate, NoteUpdate
from datetime import datetime

class NotesService:
    def __init__(self, db: Session):
        self.db = db

    async def get_user_notes(self, user_id: str) -> List[Note]:
        """Get all notes for a user"""
        notes = self.db.query(Note).filter(Note.user_id == user_id).order_by(Note.created_at.desc()).all()
        return notes

    async def get_note(self, note_id: str, user_id: str) -> Optional[Note]:
        """Get a specific note by ID"""
        note = self.db.query(Note).filter(
            Note.id == note_id,
            Note.user_id == user_id
        ).first()
        return note

    async def create_note(self, note_data: NoteCreate, user_id: str) -> Note:
        """Create a new note"""
        note = Note(
            title=note_data.title,
            tags=note_data.tags,
            segments=note_data.segments,
            source_url=note_data.source_url,
            user_id=user_id
        )
        self.db.add(note)
        self.db.commit()
        self.db.refresh(note)
        return note

    async def update_note(self, note_id: str, note_update: NoteUpdate, user_id: str) -> Optional[Note]:
        """Update an existing note"""
        note = self.db.query(Note).filter(
            Note.id == note_id,
            Note.user_id == user_id
        ).first()
        
        if not note:
            return None
        
        if note_update.title is not None:
            note.title = note_update.title
        if note_update.tags is not None:
            note.tags = note_update.tags
        
        note.updated_at = datetime.utcnow()
        self.db.commit()
        self.db.refresh(note)
        return note

    async def delete_note(self, note_id: str, user_id: str) -> bool:
        """Delete a note"""
        note = self.db.query(Note).filter(
            Note.id == note_id,
            Note.user_id == user_id
        ).first()
        
        if not note:
            return False
        
        self.db.delete(note)
        self.db.commit()
        return True 