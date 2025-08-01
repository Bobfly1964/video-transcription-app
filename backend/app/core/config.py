from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql://user:password@localhost/video_transcription"
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # OpenAI
    openai_api_key: Optional[str] = None
    
    # S3/MinIO
    s3_access_key: Optional[str] = None
    s3_secret_key: Optional[str] = None
    s3_bucket: str = "transcriptions"
    s3_endpoint: str = "http://localhost:9000"
    
    # Security
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # OAuth
    google_client_id: Optional[str] = None
    google_client_secret: Optional[str] = None
    github_client_id: Optional[str] = None
    github_client_secret: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings() 