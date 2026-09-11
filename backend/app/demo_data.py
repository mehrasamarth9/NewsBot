DEMO_TOPICS = {
    "ai agents": [
        {
            "title": "Enterprises expand use of AI agents for workflow automation",
            "url": "https://example.com/enterprise-ai-agents",
            "published_date": "2026-09-09",
            "content": "Enterprises are moving from chat assistants toward agentic systems that can plan, call tools, verify intermediate results, and complete multi-step workflows. Governance and observability remain major deployment concerns.",
            "score": 0.96,
        },
        {
            "title": "Agent evaluation shifts toward task completion and reliability",
            "url": "https://example.com/agent-evaluation",
            "published_date": "2026-09-08",
            "content": "Teams evaluating AI agents increasingly measure end-to-end task completion, retry behavior, tool accuracy, latency, and human escalation rates rather than relying on model-only benchmarks.",
            "score": 0.92,
        },
        {
            "title": "Tool interoperability grows around MCP-style integrations",
            "url": "https://example.com/mcp-interoperability",
            "published_date": "2026-09-07",
            "content": "Developers are standardizing how agents discover and invoke external tools, reducing custom integration code and making search, databases, and business systems reusable across multiple agents.",
            "score": 0.89,
        },
    ],
    "cloud ai": [
        {
            "title": "Cloud platforms compete on managed generative AI infrastructure",
            "url": "https://example.com/cloud-genai",
            "published_date": "2026-09-09",
            "content": "Major cloud platforms continue expanding managed inference, vector search, observability, and security controls for enterprise generative AI workloads.",
            "score": 0.93,
        },
        {
            "title": "Cost optimization becomes central to production LLM deployments",
            "url": "https://example.com/llm-costs",
            "published_date": "2026-09-08",
            "content": "Engineering teams are combining smaller models, caching, retrieval, batching, and selective tool use to reduce inference costs while preserving response quality.",
            "score": 0.91,
        },
    ],
}

def get_demo_results(query: str):
    q = query.lower()
    if "cloud" in q or "aws" in q:
        return DEMO_TOPICS["cloud ai"]
    return DEMO_TOPICS["ai agents"]
