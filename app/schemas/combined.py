# Combiner and Formatter schemas
from pydantic import BaseModel, Field

class NextStepItem(BaseModel):
    owner: str
    step: str
    due_days: int

class CombinerSchema(BaseModel):
    direct_answer: str
    why: list[str]
    risks: list[str]
    next_steps: list[NextStepItem]
    data_requests: list[str]
    provenance: list[str]
    confidence: float = Field(ge=0, le=1)

class NextTaskItem(BaseModel):
    owner: str
    task: str
    due: str  # ISO date or '7d' format

class FormatterSchema(BaseModel):
    title: str = Field(max_length=60)
    tldr: str = Field(max_length=160)
    decision: str
    next: list[NextTaskItem]
    risks: list[str]
    assumptions: list[str]
    metrics_to_watch: list[str]
    confidence: float = Field(ge=0, le=1)
    provenance: list[str]

