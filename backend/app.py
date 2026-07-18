from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
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

@app.post("/api/explain")
def explain_code(request: ExplainRequest):
    result = explain(request.code, request.language, request.mode)
    return {
        "mode": request.mode,
        "language": request.language,
        "explanation": result
    }

app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def home():
    return FileResponse("frontend/index.html")
