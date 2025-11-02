# Combiner schema
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

