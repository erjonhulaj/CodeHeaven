# app.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.engine import explain

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ExplainRequest(BaseModel):
    code: str
    language: str = "python"
    mode: str = "local"

@app.get("/")
def home():
    return {"message": "Hello from CodeHeaven!"}

@app.post("/api/explain")
def explain_code(request: ExplainRequest):
    #Endpoint that dispatches between local or AI explanations
    
    result = explain(request.code, request.language, request.mode)
    return {
        "mode": request.mode,
        "language": request.language,
        "explanation": result
    }