# FastAPI entrypoint
# What this file contains:
# - FastAPI app
# - /health and /ask endpoints
# - Wires request to workflow engine

import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.core.config import settings
from app.workflow.engine import run_workflow

logging.basicConfig(level=getattr(logging, settings.LOG_LEVEL.upper(), "INFO"))

app = FastAPI(title="Zylox Ask Engine (Agents SDK)", version="0.2.0")

# CORS configuration
# Note: allow_credentials=True cannot be used with allow_origins=["*"]
# So we explicitly list origins or disable credentials
origins = []
if settings.CORS_ALLOW_ORIGINS:
    if settings.CORS_ALLOW_ORIGINS == "*":
        # Wildcard: allow all origins but disable credentials
        origins = ["*"]
        allow_credentials = False
    else:
        # Specific origins: can use credentials
        origins = [o.strip() for o in settings.CORS_ALLOW_ORIGINS.split(",")]
        allow_credentials = True
else:
    # Default: allow common development origins
    origins = ["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000"]
    allow_credentials = True

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=allow_credentials,
)

class AskRequest(BaseModel):
    question: str

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/ask-test")
async def ask_test(req: AskRequest):
    """Mock endpoint for testing frontend without using OpenAI credits"""
    q = (req.question or "").strip()
    if not q:
        raise HTTPException(status_code=400, detail="Missing 'question'")
    
    # Return mock data instantly
    return {
        "executive_brief": f"**Mock Response for: {q}**\n\nThis is a test response that demonstrates the format without calling OpenAI.\n\n**Why this matters**\n- Fast response for testing\n- No API costs\n- Shows expected data structure\n\n**✅ Actions**\n- Test your frontend integration\n- Add OpenAI credits when ready for real responses\n- Switch to /ask endpoint for production\n\n**🧩 Team views**\n- All agents would analyze this question from their perspective\n- Debate would surface key conflicts\n- Combiner would synthesize insights\n\n**🗓️ Cadence**\n- Ready to go live once OpenAI credits are added",
        "weights": {
            "legal": 15.0,
            "marketing": 20.0,
            "operations": 10.0,
            "strategy": 25.0,
            "analyst": 20.0,
            "finance": 10.0
        },
        "debate": {
            "issues": [
                {
                    "id": "TEST-001",
                    "summary": "This is mock data for testing",
                    "roles_involved": ["strategy", "marketing"],
                    "type": "test",
                    "evidence": "Mock evidence for testing",
                    "weight_impact": 0.3,
                    "severity": "low",
                    "recommendation": "Use /ask endpoint for real analysis",
                    "needs_data": ["OpenAI API credits"],
                    "status": "test"
                }
            ],
            "minority_reports": [],
            "quick_consensus": ["This is test data", "Add OpenAI credits for real responses"],
            "open_questions": ["When will OpenAI credits be added?"],
            "overall_risk_score": 0.1,
            "notes_for_combiner": "Test mode - no real analysis performed"
        },
        "combined": {
            "final_summary": f"Mock response for question: {q}",
            "key_takeaways": [
                "This is a test response",
                "Frontend integration can be tested",
                "Switch to /ask for real analysis"
            ],
            "agent_contributions": {
                "legal": "Mock legal analysis",
                "marketing": "Mock marketing analysis",
                "operations": "Mock operations analysis",
                "strategy": "Mock strategy analysis",
                "analyst": "Mock analyst analysis",
                "finance": "Mock finance analysis"
            },
            "disagreements": ["No real analysis in test mode"],
            "confidence_overall": 0.5
        },
        "roles": {
            "legal": {"summary": "Mock legal response", "identified_risks": [], "relevant_regulations": [], "confidence": 0.5},
            "marketing": {"market_impact": "Mock marketing response", "messaging_recommendations": "Test", "audience_notes": "Test", "confidence": 0.5},
            "operations": {"execution_steps": "Mock steps", "dependencies": "None", "risk_analysis": "Test", "confidence": 0.5},
            "strategy": {"strategic_implications": "Mock strategy", "tradeoffs": "Test", "recommendations": "Test", "confidence": 0.5},
            "analyst": {"metrics_summary": "Mock metrics", "quantitative_estimates": "Test", "data_sources": "Test", "confidence": 0.5},
            "finance": {"financial_projection": "Mock projection", "budget_notes": "Test", "efficiency_recommendations": "Test", "confidence": 0.5}
        }
    }

@app.post("/ask")
async def ask(req: AskRequest):
    q = (req.question or "").strip()
    if not q:
        raise HTTPException(status_code=400, detail="Missing 'question'")
    
    try:
        return await run_workflow(q)
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        
        # Handle OpenAI-specific errors
        if "RateLimitError" in error_type or "429" in error_msg:
            raise HTTPException(
                status_code=429,
                detail="OpenAI API quota exceeded. Please check your billing and plan."
            )
        elif "AuthenticationError" in error_type or "401" in error_msg:
            raise HTTPException(
                status_code=401,
                detail="OpenAI API authentication failed. Check your API key."
            )
        elif "insufficient_quota" in error_msg:
            raise HTTPException(
                status_code=402,
                detail="Insufficient OpenAI credits. Please add credits to your account."
            )
        else:
            # Log the full error for debugging
            logging.error(f"Workflow error: {error_type}: {error_msg}")
            raise HTTPException(
                status_code=500,
                detail=f"Internal error: {error_type}"
            )

