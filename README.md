# Zylox Ask Engine (FastAPI + OpenAI Agents SDK)

This backend implements a multi-agent workflow (Classifier → Role Agents → Debate → Combiner → Formatter) using the **OpenAI Agents SDK (Python)** with per-role **vector store** retrieval.

## Quickstart
1. `cp .env.example .env` and fill values
2. `python -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `uvicorn app.main:app --reload` → http://localhost:8000/docs

## API
**POST /ask**
```json
{ "question": "What would it take to launch in the US healthcare market?" }
```
Returns formatted executive brief + internals (weights, role outputs, debate, combined).

## Structure (what each file contains)
- `app/agents/roles.py`: Agent SDK **Agent** definitions for Classifier, Legal, Marketing, Ops, Strategy, Analyst, Finance, Debate, Combiner, Formatter.
- `app/tools/retrieval.py`: **function tools** wrapping vector store search per role (private buckets).
- `app/workflow/engine.py`: Orchestrator calling Agents SDK to run the chain; deterministic weights; validation; progress hooks.
- `app/schemas/*`: Pydantic schemas for structured outputs.
- `app/services/openai_client.py`: Async OpenAI client shared by tools.
- `app/core/config.py`: Settings from `.env`.
- `app/utils/progress.py`: Progress emitter (swap to SSE/WebSockets).
- `app/main.py`: FastAPI app exposing `/ask`.

References: OpenAI Agents SDK & Vector Stores docs.

