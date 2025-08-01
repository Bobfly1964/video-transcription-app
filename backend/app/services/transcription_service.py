from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.database import TranscriptionJob
from app.models.schemas import TranscriptionStatus, TranscriptionResult, Segment
from app.tasks.transcription_tasks import transcribe_video_task
from app.services.s3_service import S3Service
import json

class TranscriptionService:
    def __init__(self, db: Session):
        self.db = db
        self.s3_service = S3Service()

    async def start_transcription(self, url: str, topics: List[str], user_id: str) -> str:
        """Start a transcription job"""
        # Create job record
        job = TranscriptionJob(
            url=url,
            topics=topics,
            user_id=user_id,
            status="pending",
            progress=0
        )
        self.db.add(job)
        self.db.commit()
        self.db.refresh(job)
        
        # Start Celery task
        transcribe_video_task.delay(job.id, url, topics, user_id)
        
        return job.id

    async def get_job_status(self, job_id: str, user_id: str) -> TranscriptionStatus:
        """Get the status of a transcription job"""
        job = self.db.query(TranscriptionJob).filter(
            TranscriptionJob.id == job_id,
            TranscriptionJob.user_id == user_id
        ).first()
        
        if not job:
            raise ValueError("Job not found")
        
        return TranscriptionStatus(
            status=job.status,
            progress=job.progress,
            message=job.error_message
        )

    async def get_filtered_result(self, job_id: str, user_id: str, topics: List[str]) -> TranscriptionResult:
        """Get the filtered transcription result"""
        job = self.db.query(TranscriptionJob).filter(
            TranscriptionJob.id == job_id,
            TranscriptionJob.user_id == user_id
        ).first()
        
        if not job:
            raise ValueError("Job not found")
        
        if job.status != "completed":
            raise ValueError("Job not completed")
        
        if not job.result_s3_key:
            raise ValueError("No result available")
        
        # Get result from S3
        result_data = self.s3_service.download_json(job.result_s3_key)
        
        # Convert to Segment objects
        segments = [
            Segment(timestamp=seg["timestamp"], text=seg["text"])
            for seg in result_data
        ]
        
        return TranscriptionResult(segments=segments)

    def update_job_status(self, job_id: str, status: str, progress: int, s3_key: Optional[str] = None, error_message: Optional[str] = None):
        """Update job status (called by Celery task)"""
        job = self.db.query(TranscriptionJob).filter(TranscriptionJob.id == job_id).first()
        if job:
            job.status = status
            job.progress = progress
            if s3_key:
                job.result_s3_key = s3_key
            if error_message:
                job.error_message = error_message
            self.db.commit() 