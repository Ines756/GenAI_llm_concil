# LLM Council (Distributed)

**Group members:** Claire CUCHE & Inès DARDE  
**TD Group number:** CDOF2

---

## Project overview

The idea behind this project is that instead of asking a question to a single AI model, you can group them together within your own "LLM Council." This local web application, inspired by the ChatGPT interface, orchestrates several models running locally (via Ollama) on a distributed architecture.

In a bit more detail, here is what happens when you submit a query:

1. **Stage 1: First opinions**. The user query is given to all LLMs individually, and the responses are collected. The individual responses are shown in a "tab view", so that the user can inspect them all one by one.
2. **Stage 2: Review**. Each individual LLM is given the responses of the other LLMs. Under the hood, the LLM identities are anonymized so that the LLM can't play favorites when judging their outputs. The LLM is asked to rank them in accuracy and insight.
3. **Stage 3: Final response**. The designated Chairman of the LLM Council takes all of the model's responses and compiles them into a single final answer that is presented to the user.

Local changes and improvements included in this version:
- Ollama integration (`backend/ollama.py`) for running models locally and avoiding external API costs.
- Per-model metrics (latency, success rate) collected in `backend/metrics.py` and persisted to `data/metrics.json`.
- A Monitoring Dashboard (`frontend/src/components/Dashboard.jsx`) that polls `GET /api/models/status` to display health, latency, success rate, and node IP.
- Server-Sent Events streaming (`POST /api/conversations/{id}/message/stream`) to provide stage-by-stage progress updates to the UI.

---

## Project Structure

```
llm-council/
├─ CLAUDE.md
├─ main.py
├─ pyproject.toml
├─ old_readme.md            # (README from original repo)
├─ README.md                # (new_readme)
├─ start.sh
├─ uv.lock
├─ backend/
│  ├─ __init__.py
│  ├─ config.py         # configuration for models and endpoints
│  ├─ council.py        # 3-stage orchestration
│  ├─ main.py           # FastAPI application
│  ├─ ollama.py         # Ollama client (HTTP)
│  ├─ storage.py        # JSON persistence for conversations
│  ├─ metrics.py        # model metrics collection
│  └─ __pycache__/
├─ data/
│  ├─ metrics.json
│  └─ conversations/
│     └─ *.json
└─ frontend/
   ├─ package.json
   ├─ vite.config.js
   ├─ index.html
   ├─ src/
   │  ├─ api.js
   │  ├─ main.jsx
   │  ├─ App.jsx
   │  └─ components/
   │     ├─ ChatInterface.jsx
   │     ├─ Dashboard.jsx
   │     ├─ Stage1.jsx
   │     ├─ Stage2.jsx
   │     └─ Stage3.jsx
   └─ public/
```
---

## Setup & installation

The project uses [uv](https://docs.astral.sh/uv/) for project management.

Prerequisites
- Python 3.10+
- Node.js (recommended latest LTS) + npm
- Ollama to serve models locally

Python libraries (from `pyproject.toml`)
- fastapi
- uvicorn[standard]
- python-dotenv
- httpx
- pydantic

### Distributed Architecture (Multi-computer)

The main advantage of this project is that it allows you to distribute the computing load across several computers on your local network.

1.  **On each machine** : Install Ollama and allow remote connections by setting the environment variable `OLLAMA_HOST=0.0.0.0`.
2.  **Model** : Download the necessary templates onto each dedicated machine.
    ```bash
    ollama serve
    ollama pull gemma2:2b
    ollama pull llama3.2:latest
    ollama pull mistral:latest  
    ```

### Install backend dependencies (recommended workflow):
```bash
python -m venv .venv
# Windows: .\.venv\Scripts\activate, Unix: source .venv/bin/activate
pip install --upgrade pip
uv sync
```

### Install frontend dependencies:
```bash
cd frontend
npm install
cd ..
```

### Environment variables :
Create an `.env` file at the root of the project to define your network topology. You can mix localhost and remote IP addresses.

```bash
OLLAMA_ENDPOINT_1=http://localhost:11434
OLLAMA_ENDPOINT_2=http://localhost:11434
OLLAMA_CHAIRMAN=http://localhost:11434
OLLAMA_ENDPOINT_3=http://localhost:11434
```

---

## API Endpoints (summary)

- GET / → Health check
- GET /api/conversations → List conversations (metadata)
- POST /api/conversations → Create a new conversation
- GET /api/conversations/{conversation_id} → Get conversation with messages
- POST /api/conversations/{conversation_id}/message → Run the 3-stage process (synchronous)
- POST /api/conversations/{conversation_id}/message/stream → Run the 3-stage process and stream progress via SSE
- GET /api/models/status → Check model health/performance

---

## Instructions to run the demo

Quick start (single command):
```bash
./start.sh
```

Manual run (two terminals):
1) Backend
```bash
# activate your venv first
uv run python -m backend.main
# or
uvicorn backend.main:app --reload
```
2) Frontend
```bash
cd frontend
npm run dev
```

Open UI: http://localhost:5173 in your browser

---

