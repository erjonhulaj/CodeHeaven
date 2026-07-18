import httpx

OLLAMA_URL = "http://192.168.1.15:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:3b-instruct-q4_K_M"


def explain_ai(code: str, language: str) -> str:
    prompt = (
        f"You are a senior {language} code reviewer. Analyze the following code "
        f"and respond in exactly this format:\n\n"
        f"Explanation: <2-3 sentences explaining what the code does>\n\n"
        f"Suggestions: <2-4 concise, actionable clean-code improvements. "
        f"Focus on readability, structure, and best practices. "
        f"Do not rename functions or variables unless the current name is "
        f"genuinely unclear or misleading — prefer short, conventional names "
        f"over long descriptive ones. If the code is already clean, say so briefly.>\n\n"
        f"Code:\n{code}"
    )

    try:
        response = httpx.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {"num_thread": 4}
            },
            timeout=180.0
        )
        response.raise_for_status()
        return response.json()["response"].strip()
    except httpx.TimeoutException:
        return "AI explanation timed out. The local model may be under heavy load — try again."
    except httpx.HTTPError as e:
        return f"AI service error: {str(e)}"
