from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.schemas import TranscriptionRequest, TranscriptionResponse, TranscriptionStatus, TranscriptionResult
from app.services.transcription_service import TranscriptionService
from app.services.auth_service import get_current_user
from app.models.database import User

router = APIRouter()

@router.post("/transcribe", response_model=TranscriptionResponse)
async def start_transcription(
    request: TranscriptionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Start a transcription job for a video URL"""
    try:
        transcription_service = TranscriptionService(db)
        job_id = await transcription_service.start_transcription(
            url=request.url,
            topics=request.topics,
            user_id=current_user.id
        )
        return TranscriptionResponse(jobId=job_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/transcribe/{job_id}/status", response_model=TranscriptionStatus)
async def get_transcription_status(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the status of a transcription job"""
    try:
        transcription_service = TranscriptionService(db)
        status = await transcription_service.get_job_status(job_id, current_user.id)
        return status
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/transcribe/{job_id}/result", response_model=TranscriptionResult)
async def get_transcription_result(
    job_id: str,
    topics: str = Query(None, description="Comma-separated topics for filtering"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the filtered transcription result"""
    try:
        transcription_service = TranscriptionService(db)
        topics_list = topics.split(',') if topics else []
        result = await transcription_service.get_filtered_result(
            job_id, 
            current_user.id, 
            topics_list
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e)) 