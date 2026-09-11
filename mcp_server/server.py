import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("newsbot")

@mcp.tool()
def search_news(query: str, max_results: int = 5) -> list[dict]:
    """Search current news with Tavily and return reusable structured results."""
    key = os.getenv("TAVILY_API_KEY")
    if not key:
        return [{"error": "TAVILY_API_KEY is not configured"}]
    from tavily import TavilyClient
    response = TavilyClient(api_key=key).search(
        query=query, topic="news", search_depth="advanced", max_results=max_results
    )
    return response.get("results", [])

@mcp.tool()
def evaluate_sources(results: list[dict]) -> dict:
    """Evaluate whether retrieved sources are sufficient for answer generation."""
    strong = [r for r in results if float(r.get("score", 0) or 0) >= 0.5 and len(r.get("content", "")) > 40]
    return {"sufficient": len(strong) >= 2, "strong_sources": len(strong), "total_sources": len(results)}

if __name__ == "__main__":
    mcp.run()
