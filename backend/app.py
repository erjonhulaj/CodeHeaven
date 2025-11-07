from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ExplainRequest(BaseModel):
    code: str
    language: str = "python"
    mode: str = "mode"

@app.get("/")
def home():
    return {"message": "Hello from CodeHeaven!"}

@app.post("/api/explain")
def explain_code(request: ExplainRequest):
    """
    Simple stub endpoint that returns a fake explanation.
    Later this will use local rules or AI, based on 'mode'
    """
    preview = "\n".join(request.code.strip().splitlines()[:3]) or "(empty)"

    explanation = (
        f"Mode: {request.mode} | Language: {request.language}\n"
        f"This is a placeholder explanation for your code.\n"
        f"Preview:\n{preview}"
    )

    return {
        "mode": request.mode,
        "language": request.language,
        "explanation": explanation
    }