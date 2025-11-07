from backend.engines.local_rules import explain_local
from backend.engines.ai_provider import explain_ai

def explain(code: str, language: str, mode: str) -> str:
    """
    Dispatch to local or AI engine based on mode.
    """
    if mode.lower() == "ai":
        return explain_ai(code, language)
    return explain_local(code, language)