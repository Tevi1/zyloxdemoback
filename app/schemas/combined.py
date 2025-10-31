# Combiner schema
from pydantic import BaseModel, Field

class CombinerSchema_AgentContributions(BaseModel):
    legal: str
    marketing: str
    operations: str
    strategy: str
    analyst: str
    finance: str

class CombinerSchema(BaseModel):
    final_summary: str
    key_takeaways: list[str]
    agent_contributions: CombinerSchema_AgentContributions
    disagreements: list[str]
    confidence_overall: float = Field(ge=0, le=1)

