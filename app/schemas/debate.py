# Debate schema
from pydantic import BaseModel, Field

class AddDebateSchema_IssuesItem(BaseModel):
    id: str
    summary: str
    roles_involved: list[str]
    type: str
    evidence: str
    weight_impact: float
    severity: str
    recommendation: str
    needs_data: list[str]
    status: str

class AddDebateSchema_MinorityReportsItem(BaseModel):
    role: str
    position: str
    evidence: str
    risk_if_wrong: str

class AddDebateSchema(BaseModel):
    issues: list[AddDebateSchema_IssuesItem]
    minority_reports: list[AddDebateSchema_MinorityReportsItem]
    quick_consensus: list[str]
    open_questions: list[str]
    overall_risk_score: float = Field(ge=0, le=1)
    notes_for_combiner: str

