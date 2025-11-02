# Role output schemas (strict JSON targets)
from pydantic import BaseModel, Field

class LegalSchema(BaseModel):
    summary: str
    identified_risks: list[str]
    relevant_regulations: list[str]
    provenance: list[str]
    assumptions: list[str]
    confidence: float = Field(ge=0, le=1)
    needs_data: list[str]

class MarketingSchema(BaseModel):
    market_impact: str
    messaging_recommendations: str
    channel_plan: str
    metrics: list[str]
    provenance: list[str]
    assumptions: list[str]
    confidence: float = Field(ge=0, le=1)
    needs_data: list[str]

class OwnerAssignment(BaseModel):
    step: int
    owner: str

class OperationsSchema(BaseModel):
    execution_steps: str
    owners: list[OwnerAssignment]
    dependencies: str
    risk_analysis: str
    provenance: list[str]
    assumptions: list[str]
    confidence: float = Field(ge=0, le=1)
    needs_data: list[str]

class PrioritizedMove(BaseModel):
    move: str
    expected_outcome: str
    time_horizon_weeks: int

class StrategySchema(BaseModel):
    strategic_implications: str
    tradeoffs: list[str]
    prioritized_moves: list[PrioritizedMove]
    provenance: list[str]
    assumptions: list[str]
    confidence: float = Field(ge=0, le=1)
    needs_data: list[str]

class ScenarioTableItem(BaseModel):
    scenario: str
    inputs: str
    outputs: str

class AnalystSchema(BaseModel):
    metrics_summary: str
    guardrails: list[str]
    projection_method: str
    scenario_table: list[ScenarioTableItem]
    provenance: list[str]
    assumptions: list[str]
    confidence: float = Field(ge=0, le=1)
    needs_data: list[str]

class FinanceSchema(BaseModel):
    financial_projection: str
    budget_gates: list[str]
    runway_sensitivity: str
    controls: list[str]
    provenance: list[str]
    assumptions: list[str]
    confidence: float = Field(ge=0, le=1)
    needs_data: list[str]

