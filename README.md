# NewsBot — Autonomous News Research Agent

NewsBot is an autonomous research agent that produces source-backed news briefings using a LangGraph workflow, Tavily web search, GPT-4o mini, FastAPI, React, and MCP.

## Highlights
- Query planning and refinement
- Real-time Tavily retrieval
- Relevance / recency / sufficiency evaluation
- Conditional retry loop using LangGraph
- Source-backed final briefings
- FastAPI REST API
- React research workspace
- MCP tools for reusable search + evaluation
- Local demo mode when API keys are unavailable

## Architecture

```text
React UI
   ↓
FastAPI
   ↓
LangGraph Agent
   ├─ plan_query
   ├─ search_web (Tavily)
   ├─ evaluate_results
   ├─ refine_query ↺
   └─ generate_briefing (GPT-4o mini)
            ↓
        citations

MCP Server
   ├─ search_news
   └─ evaluate_sources
```

## Quick start

### Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../.env.example ../.env
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## Environment

```bash
TAVILY_API_KEY=
OPENAI_API_KEY=
NEWSBOT_MODE=demo
OPENAI_MODEL=gpt-4o-mini
```

Use `NEWSBOT_MODE=live` with valid keys for real-time web research.

## API
- `GET /health`
- `POST /research`
- `GET /demo/topics`

## MCP
```bash
cd mcp_server
pip install -r requirements.txt
python server.py
```

## Recruiter demo
Run in demo mode to show the full LangGraph workflow without exposing credentials. Live mode uses Tavily + OpenAI.
