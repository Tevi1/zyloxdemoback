# Agents SDK agent definitions
# What this file contains:
# - Agent objects (Classifier, Legal, Marketing, Operations, Strategy, Analyst, Finance, Debate, Combiner, Formatter)
# - Each role agent uses tool calling to pull role-private context (function tools defined in app/tools/retrieval.py)
# - Instructions mirror your original workflow

from agents import Agent
from app.schemas.classifier import ClassifierSchema
from app.schemas.roles import (
    LegalSchema, MarketingSchema, OperationsSchema,
    StrategySchema, AnalystSchema, FinanceSchema
)
from app.schemas.debate import AddDebateSchema
from app.schemas.combined import CombinerSchema
from app.tools.retrieval import (
    legal_retrieval, marketing_retrieval, ops_retrieval,
    strategy_retrieval, analyst_retrieval, finance_retrieval
)

# System prompts
CLASSIFIER_SYS = (
    "You are a router that assigns relevance weights (0–100) for each C-suite role "
    "(legal, marketing, operations, strategy, analyst, finance) based on the user's question. "
    "The six numbers MUST sum to 100. Return strict JSON only with those keys."
)

LEGAL_SYS = """You are the Legal Agent (laws, compliance, privacy, IP). Use role-private context first; then general knowledge only to connect dots. Be precise and conservative.
Output STRICT JSON:
- summary (string)
- identified_risks (array of strings)
- relevant_regulations (array of strings)
- confidence (number 0–1)
If context is weak/empty, say so in summary and set confidence ≤ 0.4. JSON only."""

MARKETING_SYS = """You are the Marketing Agent (positioning, messaging, ad/disclosure compliance). Use role-private context first.
Output STRICT JSON:
- market_impact (string)
- messaging_recommendations (string)
- audience_notes (string)
- confidence (number 0–1)
If no context found, state that and set confidence ≤ 0.4. JSON only."""

OPS_SYS = """You are the Operations Agent (process, scalability, execution risk). Use role-private SOPs first.
Output STRICT JSON:
- execution_steps (string; numbered plan)
- dependencies (string; people/tools/docs)
- risk_analysis (string; top risks + mitigations)
- confidence (number 0–1)
If context is weak/empty, say so and set confidence ≤ 0.4. JSON only."""

STRATEGY_SYS = """You are the Strategy Agent (direction, moat, tradeoffs, prioritization). Use role-private strategy notes first.
Output STRICT JSON:
- strategic_implications (string)
- tradeoffs (string; bullet-style)
- recommendations (string; prioritized)
- confidence (number 0–1)
If context is weak/empty, say so and set confidence ≤ 0.4. JSON only."""

ANALYST_SYS = """You are the Analyst Agent (KPIs, ranges, quant). Use role-private data first; show realistic ranges.
Output STRICT JSON:
- metrics_summary (string)
- quantitative_estimates (string; bullets with ranges/assumptions)
- data_sources (string; describe internal metrics used)
- confidence (number 0–1)
If context is weak/empty, say so and set confidence ≤ 0.4. JSON only."""

FINANCE_SYS = """You are the Finance Agent (costs, runway, ROI). Use role-private finance docs first.
Output STRICT JSON:
- financial_projection (string)
- budget_notes (string; bullets)
- efficiency_recommendations (string)
- confidence (number 0–1)
If context is weak/empty, say so and set confidence ≤ 0.4. JSON only."""

DEBATE_SYS = """You are the Moderator (COO/Chief-of-Staff). Critique the six role JSONs in `answers`.
Find contradictions, assumptions, compliance blockers, and data gaps. Propose concrete next steps. Down-rank claims with empty sources[]. Mark them "assumption". Prefer well-cited contributions.
Return JSON only using the schema provided."""

COMBINER_SYS = """You are the COO Combiner. Merge the six role JSONs using the Classifier weights.
Use Debate to resolve conflicts, surface minority views, and compute an overall confidence (1 - overall_risk_score). Prefer higher-confidence outputs. Return JSON only in the final schema."""

FORMATTER_SYS = """You are the Executive Synthesizer for a multi-agent reasoning system.
Convert the structured final_json (combined legal, marketing, operations, strategy, analyst, finance) into a conversational, executive-brief style response.
Rules: bold headers, short headline, why memo, ✅ actions, 🧩 team views, 🗓️ cadence. No tables or code fences. If confidence < 0.6, start with the low-confidence line.
"""

# Agent definitions (Agents SDK). Tools: function tools from retrieval.py
classifier_agent = Agent(
    name="Classifier",
    instructions=CLASSIFIER_SYS,
    model="gpt-5",
    tools=[],
    output_type=ClassifierSchema
)

legal_agent = Agent(
    name="Legal",
    instructions=LEGAL_SYS,
    model="gpt-5",
    tools=[legal_retrieval],
    output_type=LegalSchema
)

marketing_agent = Agent(
    name="Marketing",
    instructions=MARKETING_SYS,
    model="gpt-5",
    tools=[marketing_retrieval],
    output_type=MarketingSchema
)

ops_agent = Agent(
    name="Operations",
    instructions=OPS_SYS,
    model="gpt-5",
    tools=[ops_retrieval],
    output_type=OperationsSchema
)

strategy_agent = Agent(
    name="Strategy",
    instructions=STRATEGY_SYS,
    model="gpt-5",
    tools=[strategy_retrieval],
    output_type=StrategySchema
)

analyst_agent = Agent(
    name="Analyst",
    instructions=ANALYST_SYS,
    model="gpt-5",
    tools=[analyst_retrieval],
    output_type=AnalystSchema
)

finance_agent = Agent(
    name="Finance",
    instructions=FINANCE_SYS,
    model="gpt-5",
    tools=[finance_retrieval],
    output_type=FinanceSchema
)

debate_agent = Agent(
    name="Debate",
    instructions=DEBATE_SYS,
    model="gpt-5",
    tools=[],
    output_type=AddDebateSchema
)

combiner_agent = Agent(
    name="Combiner",
    instructions=COMBINER_SYS,
    model="gpt-5",
    tools=[],
    output_type=CombinerSchema
)

formatter_agent = Agent(
    name="Formatter",
    instructions=FORMATTER_SYS,
    model="gpt-5",
    tools=[]
    # No output_type for formatter - it returns plain text
)

