# CodeHeaven

> A calm space to understand and improve your code, with or without AI.

🔗 **Live:** [codeheaven.duckdns.org](https://codeheaven.duckdns.org)

---

## Why I built this

I wanted to go deeper into Python by building something that forced me to actually understand how code works, not just how to write it. CodeHeaven does exactly that: **a Python tool, written in Python, that analyzes Python code.**

Building the AST-based analysis engine meant learning how Python actually parses and interprets code under the hood. The AI integration came later, as a way to compare rule-based analysis against natural-language explanations from a language model, and to learn how to wire a real LLM into a web app end to end.

---

## What it does

CodeHeaven has two independent analysis modes:

### Local Mode (rule-based, offline)
Parses your code into an Abstract Syntax Tree (`ast` module) and checks for:
- Bare `except:` blocks (catches everything, including `KeyboardInterrupt`)
- Functions over 25 lines (readability threshold)
- Missing docstrings
- Unused variables

No network calls, no AI, fully deterministic. Runs entirely on the server's CPU in milliseconds.

### AI Mode (natural language, self-hosted)
Sends your code to a local LLM (see Infrastructure below) and asks it to:
1. Explain what the code does, in plain English
2. Suggest concrete clean-code improvements

The AI output is intentionally not treated as ground truth. The UI includes a visible disclaimer, because small local models can produce suggestions that are technically plausible but not always correct (an early version of the prompt caused the model to suggest renaming `price` to `price`). Explanation and Suggestions are parsed and rendered as separate, clearly labeled blocks in the UI.

---

## Infrastructure

CodeHeaven runs on a Proxmox homelab I built and maintain myself, not a cloud provider. Everything below is self-hosted:

| Component | Details |
|---|---|
| **Hypervisor** | Proxmox VE, bare-metal |
| **Backend** | Dedicated LXC container running FastAPI + Uvicorn |
| **AI model host** | Separate LXC container running [Ollama](https://ollama.com) |
| **Model** | `qwen2.5-coder:3b-instruct-q4_K_M`, a quantized, code-specialized model small enough to run acceptably on CPU (no GPU passthrough yet, planned) |
| **Reverse proxy** | Caddy, automatic HTTPS via Let's Encrypt |
| **Domain** | Dynamic DNS via DuckDNS |

The backend and the AI model run in separate containers communicating over the internal network. This mirrors how you'd separate an application server from an inference server in a real production setup, just at homelab scale.

### Why a 3B model instead of something bigger

Without a GPU, larger models became impractically slow on this hardware (a 7B model took 5+ minutes for a two-sentence explanation, mostly due to a CPU thread misconfiguration I had to debug: Ollama was defaulting to more threads than the container had cores available). The 3B model responds in roughly 5 to 15 seconds, which is an acceptable tradeoff for a demo project. GPU passthrough is on the roadmap to make larger models practical.

---

## Reliability & limits

Since this runs on personal hardware with a single shared AI model, a few protections are in place:

- **Rate limiting**: 5 requests per minute per IP address, enforced in FastAPI (sliding window, in-memory)
- **AI concurrency limit**: only one AI request is processed at a time. The local model is CPU-bound, so parallel requests would just slow each other down rather than run faster
- Requests beyond the limit get a clear, friendly in-UI message rather than a raw error

---

## Tech stack

| Layer | Tools |
|---|---|
| Backend | Python, FastAPI, Pydantic, Uvicorn |
| Code analysis | Python `ast` module |
| AI | Ollama (self-hosted, local inference) |
| Frontend | HTML, CSS, vanilla JavaScript (no frameworks) |
| Infrastructure | Proxmox VE, LXC containers, Caddy, DuckDNS, Let's Encrypt |

No frontend framework, on purpose. The goal was to understand `fetch()`, DOM manipulation, and state handling directly rather than through a framework's abstractions.

---

## Project structure

```
CodeHeaven/
  backend/
    app.py              FastAPI app, routes, rate limiting, CORS
    engine.py            Dispatches between local and AI analysis
    rate_limiter.py       Sliding-window rate limiter
    models.py            Pydantic models (Finding)
    engines/
      local_rules.py       AST-based rule engine
      ai_provider.py       Ollama integration
  frontend/
    index.html
    styles.css
    app.js
  requirements.txt
  README.md
```

FastAPI serves the frontend directly (`StaticFiles` plus a root route returning `index.html`). No separate frontend server, one process, one port.

---

## Running it locally

```bash
git clone https://github.com/erjonhulaj/CodeHeaven.git
cd CodeHeaven
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app:app --host 0.0.0.0 --reload
```

Visit `http://localhost:8000`. Local Mode works out of the box. AI Mode requires a running Ollama instance. Update `OLLAMA_URL` in `backend/engines/ai_provider.py` to point at your own instance, or run Ollama locally on the default port.

---

## What I learned building this

- How Python's `ast` module actually works: parsing source into a tree and walking it to detect patterns, rather than treating code as text
- Designing a dispatcher pattern to cleanly switch between two very different analysis strategies
- Debugging a real infrastructure problem end to end: an LLM taking 6 minutes to respond turned out to be a CPU thread misconfiguration, not a hardware limit, diagnosed by comparing `nproc`, `htop`, and Ollama's own logs
- Why prompt design matters even for small tasks. The AI model's suggestions noticeably improved after adding explicit constraints to the prompt (for example, "don't rename variables unless the current name is genuinely unclear")
- Basic production concerns that don't come up in tutorials: rate limiting, CORS, reverse proxying, graceful degradation when a shared resource is busy

---

## Roadmap

- [ ] GPU passthrough for the Ollama container, for larger and faster models
- [ ] Multi-language support beyond Python (JavaScript, C#, Swift)
- [ ] Unit tests (pytest)
- [ ] Syntax highlighting in the code input
- [ ] Export findings as Markdown/PDF

---

## Author

**Erjon Hulaj**

Started: November 2025