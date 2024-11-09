# main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import Optional
import os
from detector import AdvancedAIContentDetector

# Initialize FastAPI
app = FastAPI(title="AI Content Detector")

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

class TextInput(BaseModel):
    text: str
    min_length: Optional[int] = 50

class AnalysisResult(BaseModel):
    scores: dict
    features: dict
    summary: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Read and return the index.html file
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.post("/api/analyze", response_model=AnalysisResult)
async def analyze_text(input_data: TextInput):
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

# Mount static files if not on Vercel
if not os.getenv("VERCEL"):
    app.mount("/static", StaticFiles(directory="static"), name="static")
