from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # API Settings
    API_TITLE: str = "ContentForge AI API"
    API_VERSION: str = "1.0.0"
    API_KEY: str = "demo-api-key-123"
    
    # JWT Settings
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 1440  # 24 hours
    
    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "https://your-frontend-domain.com"
    ]
    
    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS: List[str] = ["txt", "md"]
    
    # Rate Limiting
    RATE_LIMIT_PER_HOUR: int = 10
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
