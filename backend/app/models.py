from pydantic import BaseModel, Field

class ResearchRequest(BaseModel):
    query: str = Field(min_length=3, max_length=500)

class Source(BaseModel):
    title: str
    url: str
    published_date: str | None = None
    snippet: str
    score: float = 0.0

class TraceStep(BaseModel):
    node: str
    status: str
    detail: str

class ResearchResponse(BaseModel):
    query: str
    final_query: str
    answer: str
    sources: list[Source]
    trace: list[TraceStep]
    mode: str
