from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.database import TranscriptionJob

class DatabaseService:
    def __init__(self):
        self.db: Session = SessionLocal()

    def update_job_status(self, job_id: str, status: str, progress: int, s3_key: str = None, error_message: str = None):
        """Update transcription job status"""
        try:
            job = self.db.query(TranscriptionJob).filter(TranscriptionJob.id == job_id).first()
            if job:
                job.status = status
                job.progress = progress
                if s3_key:
                    job.result_s3_key = s3_key
                if error_message:
                    job.error_message = error_message
                self.db.commit()
        except Exception as e:
            print(f"Error updating job status: {e}")
            self.db.rollback()
        finally:
            self.db.close() 