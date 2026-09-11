from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .agent import news_graph
from .config import settings
from .models import ResearchRequest, ResearchResponse, Source, TraceStep

app = FastAPI(title="NewsBot API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok", "mode": settings.newsbot_mode, "model": settings.openai_model}

@app.get("/demo/topics")
def demo_topics():
    return {"topics": ["AI agents", "cloud AI infrastructure", "agent evaluation", "MCP interoperability"]}

@app.post("/research", response_model=ResearchResponse)
def research(payload: ResearchRequest):
    result = news_graph.invoke({"original_query": payload.query, "trace": []})
    return ResearchResponse(
        query=payload.query,
        final_query=result.get("query", payload.query),
        answer=result["answer"],
        sources=[
            Source(
                title=r["title"],
                url=r["url"],
                published_date=r.get("published_date"),
                snippet=r.get("content", ""),
                score=float(r.get("score", 0.0) or 0.0),
            ) for r in result.get("results", [])
        ],
        trace=[TraceStep(**step) for step in result.get("trace", [])],
        mode=settings.newsbot_mode,
    )
