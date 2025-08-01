import os
import tempfile
import json
from typing import List, Dict, Any
import yt_dlp
import openai
from celery import current_task
from app.core.celery_app import celery_app
from app.core.config import settings
from app.services.s3_service import S3Service
from app.services.database_service import DatabaseService

@celery_app.task(bind=True)
def transcribe_video_task(self, job_id: str, url: str, topics: List[str], user_id: str):
    """Celery task to transcribe a video"""
    try:
        # Update job status to processing
        db_service = DatabaseService()
        db_service.update_job_status(job_id, "processing", 10)
        
        # Download video
        current_task.update_state(state="PROGRESS", meta={"progress": 20})
        video_path = download_video(url)
        
        # Update progress
        db_service.update_job_status(job_id, "processing", 40)
        current_task.update_state(state="PROGRESS", meta={"progress": 40})
        
        # Transcribe video
        transcription_result = transcribe_audio(video_path)
        
        # Update progress
        db_service.update_job_status(job_id, "processing", 80)
        current_task.update_state(state="PROGRESS", meta={"progress": 80})
        
        # Filter segments by topics
        filtered_segments = filter_segments_by_topics(transcription_result, topics)
        
        # Save to S3
        s3_service = S3Service()
        s3_key = f"transcriptions/{job_id}/result.json"
        s3_service.upload_json(filtered_segments, s3_key)
        
        # Update job status to completed
        db_service.update_job_status(job_id, "completed", 100, s3_key)
        current_task.update_state(state="SUCCESS", meta={"progress": 100})
        
        # Cleanup
        os.remove(video_path)
        
        return {"status": "completed", "job_id": job_id}
        
    except Exception as e:
        # Update job status to failed
        db_service = DatabaseService()
        db_service.update_job_status(job_id, "failed", 0, error_message=str(e))
        current_task.update_state(state="FAILURE", meta={"error": str(e)})
        raise

def download_video(url: str) -> str:
    """Download video using yt-dlp"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        video_id = info['id']
        return f"{video_id}.mp3"

def transcribe_audio(audio_path: str) -> List[Dict[str, Any]]:
    """Transcribe audio using OpenAI Whisper"""
    if not settings.openai_api_key:
        raise ValueError("OpenAI API key not configured")
    
    openai.api_key = settings.openai_api_key
    
    with open(audio_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe(
            "whisper-1",
            audio_file,
            response_format="verbose_json",
            timestamp_granularities=["segment"]
        )
    
    return transcript.get("segments", [])

def filter_segments_by_topics(segments: List[Dict[str, Any]], topics: List[str]) -> List[Dict[str, Any]]:
    """Filter segments based on topics/keywords"""
    if not topics:
        return segments
    
    filtered_segments = []
    topics_lower = [topic.lower() for topic in topics]
    
    for segment in segments:
        text_lower = segment.get("text", "").lower()
        if any(topic in text_lower for topic in topics_lower):
            filtered_segments.append({
                "timestamp": segment.get("start", 0),
                "text": segment.get("text", "")
            })
    
    return filtered_segments 