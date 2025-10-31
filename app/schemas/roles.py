# Role output schemas (strict JSON targets)
from pydantic import BaseModel, Field

class LegalSchema(BaseModel):
    summary: str
    identified_risks: list[str]
    relevant_regulations: list[str]
    confidence: float = Field(ge=0, le=1)

class MarketingSchema(BaseModel):
    market_impact: str
    messaging_recommendations: str
    audience_notes: str
    confidence: float = Field(ge=0, le=1)

class OperationsSchema(BaseModel):
    execution_steps: str
    dependencies: str
    risk_analysis: str
    confidence: float = Field(ge=0, le=1)

class StrategySchema(BaseModel):
    strategic_implications: str
    tradeoffs: str
    recommendations: str
    confidence: float = Field(ge=0, le=1)

class AnalystSchema(BaseModel):
    metrics_summary: str
    quantitative_estimates: str
    data_sources: str
    confidence: float = Field(ge=0, le=1)

class FinanceSchema(BaseModel):
    financial_projection: str
    budget_notes: str
    efficiency_recommendations: str
    confidence: float = Field(ge=0, le=1)

