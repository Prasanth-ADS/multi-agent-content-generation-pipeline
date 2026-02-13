from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from pathlib import Path
import uuid
from datetime import datetime

from .models import GenerateRequest, GenerateResponse, JobStatusResponse
from .auth import verify_token, get_api_key
from .tasks import process_pipeline_job
from .config import settings

# Initialize FastAPI app
app = FastAPI(
    title=settings.API_TITLE,
    description="Multi-Agent Content Generation Pipeline API",
    version=settings.API_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for downloads
os.makedirs("outputs", exist_ok=True)
app.mount("/downloads", StaticFiles(directory="outputs"), name="downloads")

# In-memory job storage (use Redis in production)
jobs = {}

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": settings.API_TITLE,
        "version": settings.API_VERSION,
        "status": "operational",
        "endpoints": {
            "docs": "/docs",
            "generate": "/api/generate",
            "status": "/api/status/{job_id}",
            "download": "/downloads/{filename}"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/generate", response_model=GenerateResponse)
async def generate_content(
    request: GenerateRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(get_api_key)
):
    """
    Generate blog post from PRD
    
    This endpoint accepts a PRD and queues it for processing.
    Returns a job_id that can be used to check status.
    """
    
    # Validate input
    if len(request.prd_text) < 50:
        raise HTTPException(
            status_code=400,
            detail="PRD text too short (minimum 50 characters)"
        )
    
    # Create job
    job_id = str(uuid.uuid4())
    
    jobs[job_id] = {
        "job_id": job_id,
        "status": "pending",
        "progress": 0,
        "current_step": None,
        "result": None,
        "error": None,
        "created_at": datetime.utcnow(),
        "completed_at": None,
        "request": request.dict()
    }
    
    # Queue background task
    background_tasks.add_task(
        process_pipeline_job,
        job_id=job_id,
        prd_text=request.prd_text,
        title=request.title,
        output_format=request.format,
        jobs_dict=jobs
    )
    
    return GenerateResponse(
        job_id=job_id,
        status="pending",
        message="Job queued for processing",
        estimated_time=120 # Estimate 2 minutes on average
    )

@app.get("/api/status/{job_id}", response_model=JobStatusResponse)
async def get_job_status(
    job_id: str,
    api_key: str = Depends(get_api_key)
):
    """
    Get job status
    
    Returns current status and progress of a generation job.
    """
    
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    return JobStatusResponse(**job)

@app.get("/api/download/{job_id}")
async def download_result(
    job_id: str,
    api_key: str = Depends(get_api_key)
):
    """
    Download generated content
    
    Returns the generated file for a completed job.
    """
    
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    if job["status"] != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Job not completed yet (status: {job['status']})"
        )
    
    file_path = job["result"].get("file_path")
    
    if not file_path or not Path(file_path).exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    # Determine media type
    format_type = job["request"]["format"]
    media_types = {
        "md": "text/markdown",
        "html": "text/html",
        "pdf": "application/pdf",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    }
    
    return FileResponse(
        path=file_path,
        media_type=media_types.get(format_type, "application/octet-stream"),
        filename=Path(file_path).name
    )

@app.delete("/api/jobs/{job_id}")
async def delete_job(
    job_id: str,
    api_key: str = Depends(get_api_key)
):
    """Delete a job and its associated files"""
    
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    # Delete file if exists
    if job.get("result") and job["result"].get("file_path"):
        file_path = Path(job["result"]["file_path"])
        if file_path.exists():
            file_path.unlink()
    
    # Remove from jobs dict
    del jobs[job_id]
    
    return {"message": "Job deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
