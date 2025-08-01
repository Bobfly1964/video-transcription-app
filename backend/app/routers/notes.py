from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.schemas import Note, NoteCreate, NoteUpdate
from app.services.notes_service import NotesService
from app.services.auth_service import get_current_user
from app.models.database import User

router = APIRouter()

@router.get("/notes", response_model=List[Note])
async def get_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all notes for the current user"""
    notes_service = NotesService(db)
    return await notes_service.get_user_notes(current_user.id)

@router.get("/notes/{note_id}", response_model=Note)
async def get_note(
    note_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific note by ID"""
    notes_service = NotesService(db)
    note = await notes_service.get_note(note_id, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.post("/notes", response_model=Note)
async def create_note(
    note: NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new note"""
    notes_service = NotesService(db)
    return await notes_service.create_note(note, current_user.id)

@router.put("/notes/{note_id}", response_model=Note)
async def update_note(
    note_id: str,
    note_update: NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing note"""
    notes_service = NotesService(db)
    note = await notes_service.update_note(note_id, note_update, current_user.id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.delete("/notes/{note_id}")
async def delete_note(
    note_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a note"""
    notes_service = NotesService(db)
    success = await notes_service.delete_note(note_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"} 