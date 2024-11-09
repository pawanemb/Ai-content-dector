# main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import time
from detector import AdvancedAIContentDetector
from config import settings

app = FastAPI(title=settings.APP_NAME, version=settings.API_VERSION)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize detector
detector = AdvancedAIContentDetector()

# Rate limiting
request_timestamps = {}

class TextInput(BaseModel):
    text: str
    min_length: Optional[int] = settings.MIN_TEXT_LENGTH

class AnalysisResult(BaseModel):
    scores: dict
    features: dict
    summary: str

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware"""
    client_ip = request.client.host
    
    # Clean old timestamps
    current_time = time.time()
    request_timestamps[client_ip] = [
        ts for ts in request_timestamps.get(client_ip, [])
        if current_time - ts < 60
    ]
    
    # Check rate limit
    if len(request_timestamps.get(client_ip, [])) >= settings.RATE_LIMIT_PER_MINUTE:
        return JSONResponse(
            status_code=429,
            content={"error": "Rate limit exceeded. Please try again later."}
        )
    
    # Add timestamp
    request_timestamps.setdefault(client_ip, []).append(current_time)
    
    return await call_next(request)

@app.post("/api/analyze", response_model=AnalysisResult)
async def analyze_text(input_data: TextInput):
    """Analyze text for AI content detection"""
    try:
        if len(input_data.text.strip()) < input_data.min_length:
            raise HTTPException(
                status_code=400,
                detail=f"Text must be at least {input_data.min_length} characters long"
            )
        
        result = detector.analyze_text(input_data.text)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )