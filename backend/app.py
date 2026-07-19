import asyncio
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from backend.engine import explain
from backend.rate_limiter import check_rate_limit

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Only one AI request processed at a time — the local Ollama server is CPU-only,
# so parallel AI calls would just slow each other down instead of running faster.
ai_semaphore = asyncio.Semaphore(1)

class ExplainRequest(BaseModel):
    code: str
    language: str = "python"
    mode: str = "local"

@app.post("/api/explain")
async def explain_code(request: ExplainRequest, http_request: Request):
    check_rate_limit(http_request)

    if request.mode.lower() == "ai":
        if ai_semaphore.locked():
            raise HTTPException(
                status_code=429,
                detail="AI is currently busy processing another request. Please try again in a moment."
            )
        async with ai_semaphore:
            result = explain(request.code, request.language, request.mode)
    else:
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
