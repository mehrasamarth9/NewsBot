from __future__ import annotations
from typing import TypedDict
from langgraph.graph import StateGraph, END
from .config import settings
from .demo_data import get_demo_results

class AgentState(TypedDict, total=False):
    original_query: str
    query: str
    results: list[dict]
    answer: str
    retry_count: int
    sufficient: bool
    trace: list[dict]


def _trace(state: AgentState, node: str, detail: str):
    state.setdefault("trace", []).append({"node": node, "status": "complete", "detail": detail})


def plan_query(state: AgentState):
    query = state["original_query"].strip()
    state["query"] = query
    state["retry_count"] = 0
    _trace(state, "plan_query", f"Prepared research query: {query}")
    return state


def search_web(state: AgentState):
    if settings.newsbot_mode == "live" and settings.tavily_api_key:
        from tavily import TavilyClient
        client = TavilyClient(api_key=settings.tavily_api_key)
        response = client.search(
            query=state["query"],
            topic="news",
            search_depth="advanced",
            max_results=6,
            include_answer=False,
        )
        state["results"] = [
            {
                "title": r.get("title", "Untitled"),
                "url": r.get("url", ""),
                "published_date": r.get("published_date"),
                "content": r.get("content", ""),
                "score": float(r.get("score", 0.0) or 0.0),
            }
            for r in response.get("results", [])
        ]
        detail = f"Retrieved {len(state['results'])} live news results with Tavily."
    else:
        state["results"] = get_demo_results(state["query"])
        detail = f"Retrieved {len(state['results'])} seeded demo sources."
    _trace(state, "search_web", detail)
    return state


def evaluate_results(state: AgentState):
    results = state.get("results", [])
    strong = [r for r in results if r.get("score", 0) >= 0.5 and len(r.get("content", "")) > 40]
    state["sufficient"] = len(strong) >= 2
    _trace(
        state,
        "evaluate_results",
        f"{len(strong)} sources passed relevance/sufficiency checks; "
        + ("research is sufficient." if state["sufficient"] else "query refinement required."),
    )
    return state


def route_after_evaluation(state: AgentState):
    if state.get("sufficient") or state.get("retry_count", 0) >= settings.max_retries:
        return "generate_briefing"
    return "refine_query"


def refine_query(state: AgentState):
    state["retry_count"] = state.get("retry_count", 0) + 1
    state["query"] = f"{state['original_query']} latest developments impact analysis"
    _trace(state, "refine_query", f"Refined query for retry {state['retry_count']}: {state['query']}")
    return state


def _demo_answer(query: str, results: list[dict]):
    bullets = []
    for idx, item in enumerate(results[:4], start=1):
        bullets.append(f"{idx}. {item['content']} [{idx}]")
    return (
        f"## News briefing\n\nFor **{query}**, the strongest signals are:\n\n"
        + "\n\n".join(bullets)
        + "\n\n### Impact\nThe common theme is a shift from experimental AI features toward production systems measured on reliability, cost, interoperability, and task completion."
    )


def generate_briefing(state: AgentState):
    if settings.newsbot_mode == "live" and settings.openai_api_key:
        from langchain_openai import ChatOpenAI
        sources = "\n\n".join(
            f"[{i}] {r['title']}\nURL: {r['url']}\nDate: {r.get('published_date')}\n{r['content']}"
            for i, r in enumerate(state["results"], start=1)
        )
        llm = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key, temperature=0.2)
        prompt = f"""You are a news research analyst. Answer the user's query using only the supplied sources.
Produce a concise briefing with: Key developments, Why it matters, and What to watch next.
Use inline citations like [1], [2]. Do not invent facts.

Query: {state['original_query']}

Sources:\n{sources}"""
        state["answer"] = llm.invoke(prompt).content
        detail = f"Generated source-backed briefing with {settings.openai_model}."
    else:
        state["answer"] = _demo_answer(state["original_query"], state["results"])
        detail = "Generated deterministic source-backed demo briefing."
    _trace(state, "generate_briefing", detail)
    return state


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("plan_query", plan_query)
    graph.add_node("search_web", search_web)
    graph.add_node("evaluate_results", evaluate_results)
    graph.add_node("refine_query", refine_query)
    graph.add_node("generate_briefing", generate_briefing)

    graph.set_entry_point("plan_query")
    graph.add_edge("plan_query", "search_web")
    graph.add_edge("search_web", "evaluate_results")
    graph.add_conditional_edges(
        "evaluate_results",
        route_after_evaluation,
        {"refine_query": "refine_query", "generate_briefing": "generate_briefing"},
    )
    graph.add_edge("refine_query", "search_web")
    graph.add_edge("generate_briefing", END)
    return graph.compile()

news_graph = build_graph()
