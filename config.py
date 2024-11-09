# config.py
from pydantic import BaseSettings
from typing import Dict

class Settings(BaseSettings):
    APP_NAME: str = "AI Content Detector"
    API_VERSION: str = "1.0"
    DEBUG: bool = False
    MIN_TEXT_LENGTH: int = 50
    MAX_TEXT_LENGTH: int = 50000
    
    # Model weights for different analysis components
    MODEL_WEIGHTS: Dict[str, float] = {
        "semantic": 0.3,
        "statistical": 0.3,
        "stylometric": 0.4
    }
    
    # API rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    # Cache settings
    CACHE_TTL: int = 3600  # 1 hour
    
    class Config:
        env_file = ".env"

settings = Settings()