def explain_local(code: str, language: str) -> str:
    """
    Local rule-based explanation (placeholder).
    Later this will analyze code using AST or regex.
    """
    preview = "\n".join(code.strip().splitlines()[:3] or "(empty)")
    return(
        f"[LOCAL MODE]\n"
        f"Language: {language}\n"
        f"This is a local placeholder explanation.\n"
        f"Preview:\n{preview}"
    )