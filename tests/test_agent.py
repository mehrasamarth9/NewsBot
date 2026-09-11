import os
os.environ["NEWSBOT_MODE"] = "demo"

from backend.app.agent import news_graph

def test_demo_research_returns_answer_and_sources():
    result = news_graph.invoke({"original_query": "latest AI agents", "trace": []})
    assert result["answer"]
    assert len(result["results"]) >= 2
    assert result["sufficient"] is True
    assert any(step["node"] == "evaluate_results" for step in result["trace"])
