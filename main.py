# main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any
from detector import AdvancedAIContentDetector

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
    scores: Dict[str, float]
    features: Dict[str, Any]
    summary: str

@app.get("/", response_class=HTMLResponse)
async def read_root():
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
