from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import transcribe, notes
from app.core.config import settings

app = FastAPI(
    title="Video Transcription API",
    description="API for transcribing videos and managing notes",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(transcribe.router, prefix="/api", tags=["transcribe"])
app.include_router(notes.router, prefix="/api", tags=["notes"])

@app.get("/")
async def root():
    return {"message": "Video Transcription API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 