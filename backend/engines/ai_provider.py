def explain_ai(code: str, language: str) -> str:
    """
    AI explanation (placeholder)
    Later this will call a local or API-based LLM.
    """
    preview = "\n".join(code.strip().splitlines()[:3]) or "(empty)"
    return (
        f"[AI MODE]\n"
        f"Language: {language}\n"
        f"This is an AI placeholder explanation.\n"
        f"Preview:\n{preview}"
    )