# 🌤️ CodeHeaven

> A calm space to understand, explain, and improve your code — with and without AI.

---

## 🧭 Project Overview

**CodeHeaven** is a web-based tool where you can paste your code (Python, JavaScript, C#, Swift, etc.)  
and the app will **analyze, explain, and give improvement suggestions**.

It has **two modes**:
1. **Local Mode (Rule-Based)** → analyzes the code using logical rules written in Python (no AI, works offline).  
2. **AI Mode (Smart)** → uses a local or API-based AI model to explain and review your code in natural language.

---

## 💡 Project Goals

- Build a **full-stack developer tool** from scratch.
- Learn and understand how **code analysis** works internally.
- Understand how to integrate **AI** into real applications.
- Create a **public GitHub project** that shows real engineering skills.
- Practice **Git commits, versioning, and documentation**.

---

## 🧱 Architecture Overview
code-heaven/
├─ backend/
│  ├─ app.py                # FastAPI backend
│  ├─ engine.py             # Dispatcher between local + AI
│  ├─ engines/
│  │   ├─ local_rules.py    # Rule-based analyzer
│  │   └─ ai_provider.py    # AI-based explainer (API/local LLM)
│  └─ utils/                # Helper functions (later)
├─ frontend/
│  ├─ index.html            # UI
│  ├─ styles.css            # Styling
│  └─ app.js                # Fetches results from API
├─ tests/                   # For unit tests later
├─ README.md
└─ requirements.txt

---

## 🧠 What You Will Learn

### 🐍 Python
- Setting up a **FastAPI** backend
- Creating **API endpoints** and validating requests with `pydantic`
- Writing **modular Python code** (import structure, packages)
- Working with the **AST (Abstract Syntax Tree)** for code analysis
- Using **Regex**, **loops**, **functions**, **error handling**
- Designing a **dispatcher pattern** (choosing between AI or local)
- Writing **unit tests** and using **virtual environments**

### 💻 JavaScript / Frontend
- Using **HTML/CSS/JS** to build a small web interface
- Sending **HTTP requests** to the backend with `fetch()`
- Updating the UI dynamically (switch between AI/Local modes)
- Understanding basic **DOM manipulation** and **event handling**

### ⚙️ Dev Skills
- Creating and managing **Git commits** and **branches**
- Writing clean **commit messages**
- Using **GitHub** to publish code publicly
- Writing a professional **README**
- Structuring and documenting a real project

### 🤖 Artificial Intelligence
- How to send code and prompts to a **local AI model** (like Ollama or Hugging Face)
- How to integrate an **API** (optional: OpenAI, OpenRouter)
- Understanding **prompt design** and **model responses**
- Combining **AI output** with your own logic

---

## 🧩 Technologies You Will Use

| Category | Tools / Libraries |
|-----------|-------------------|
| **Backend** | Python, FastAPI, Pydantic, Uvicorn |
| **Frontend** | HTML, CSS, JavaScript |
| **AI** | Local model (Ollama / Hugging Face), optional API |
| **Code Analysis** | Python `ast`, `re` (regular expressions) |
| **Dev Tools** | Git, GitHub, Notion, VS Code |
| **Testing** | Pytest (later) |

---

## 🚀 Step-by-Step Roadmap

| Step | Goal | What You Learn |
|------|------|----------------|
| **1️⃣ Setup** | Project folder, Git, README, .gitignore | Project structure, Git basics |
| **2️⃣ Backend Hello World** | Create FastAPI app, test endpoint | Backend setup, JSON responses |
| **3️⃣ Dual Mode Dispatcher** | “local” vs “ai” explanation stubs | Modular thinking |
| **4️⃣ Frontend Basics** | HTML page + fetch() to API | Connecting front and back |
| **5️⃣ Local Rule Analyzer** | Detect code smells (bare except, long functions, etc.) | Parsing, AST |
| **6️⃣ AI Integration** | Use a local AI (Ollama) or API | API calls, prompt design |
| **7️⃣ Multi-language Support** | Add C#, Swift, JS analyzers | Regex + modular design |
| **8️⃣ UI Polish** | Add mode toggle, styling, responsiveness | Frontend design |
| **9️⃣ Tests + Docs** | Unit tests, final README | Testing, documentation |
| **🔟 Showcase** | Publish and demo on GitHub | Portfolio presentation |

---

## 🧩 Future Ideas

- Add user login and history of analyzed code  
- Export explanations as Markdown or PDF  
- Add “shareable link” feature  
- Add syntax highlighting in frontend  
- Add code complexity graph (visualized with JS library)  
- Make a small **VS Code extension** version later

---

## 🏁 Vision Statement

> *“CodeHeaven is a learning-driven project where every step teaches something valuable — from how code is structured to how AI can make it easier to understand. It’s not just a tool, it’s a journey into becoming a better programmer.”*

---

## ✍️ Author

**Developer:** *[Your Name]*  
**Started:** November 2025  
**Stack:** Python • FastAPI • JS • HTML/CSS • Git • AI (Ollama/OpenAI)  
**Repo:** [github.com/yourusername/code-heaven](https://github.com/yourusername/code-heaven)

---