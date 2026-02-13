from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime

class GenerateRequest(BaseModel):
    prd_text: str = Field(..., min_length=50, max_length=10000, description="Product Requirements Document text")
    title: Optional[str] = Field(None, max_length=200, description="Blog post title")
    format: Literal['md', 'html', 'pdf', 'docx'] = Field('md', description="Output format")
    
    class Config:
        json_schema_extra = {
            "example": {
                "prd_text": "# Blog Post: AI Agents\n\nWrite an 800-word blog about AI agents...",
                "title": "Introduction to AI Agents",
                "format": "html"
            }
        }

class GenerateResponse(BaseModel):
    job_id: str = Field(..., description="Unique job identifier")
    status: Literal['pending', 'processing', 'completed', 'failed'] = Field(..., description="Job status")
    message: str = Field(..., description="Status message")
    estimated_time: int = Field(..., description="Estimated completion time in seconds")

class JobStatusResponse(BaseModel):
    job_id: str
    status: Literal['pending', 'processing', 'completed', 'failed']
    progress: int = Field(..., ge=0, le=100, description="Progress percentage")
    current_step: Optional[str] = Field(None, description="Current pipeline step")
    result: Optional[dict] = Field(None, description="Final result if completed")
    error: Optional[str] = Field(None, description="Error message if failed")
    created_at: datetime
    completed_at: Optional[datetime] = None

class AgentProgress(BaseModel):
    agent: str
    status: Literal['pending', 'running', 'completed', 'failed']
    message: str
    timestamp: datetime

class PipelineResult(BaseModel):
    run_id: str
    content: str
    format: str
    download_url: str
    metrics: dict
    duration_seconds: float
