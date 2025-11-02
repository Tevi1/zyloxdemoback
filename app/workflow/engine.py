# Workflow orchestrator
# What this file contains:
# - Deterministic chain using the Agents SDK agents from app/agents/roles.py
# - Calls classifier → runs role agents (with tool calling) → debate → combine → formatter
# - Strict schema validation using OpenAI JSON mode + Pydantic
# - Progress events via app/utils/progress.py

import json
import asyncio
from fastapi import HTTPException
from agents import Runner, set_default_openai_client
from app.services.openai_client import client as openai_client
from app.schemas.classifier import ClassifierSchema
from app.schemas.roles import (
    LegalSchema, MarketingSchema, OperationsSchema,
    StrategySchema, AnalystSchema, FinanceSchema
)
from app.schemas.debate import AddDebateSchema
from app.schemas.combined import CombinerSchema, FormatterSchema
from app.utils.progress import emit
from app.agents.roles import (
    classifier_agent, legal_agent, marketing_agent, ops_agent,
    strategy_agent, analyst_agent, finance_agent, debate_agent,
    combiner_agent, formatter_agent
)

# Set the default OpenAI client for the Agents SDK
set_default_openai_client(openai_client)

async def _json(agent, system_instructions: str, user_text: str, schema):
    """Invoke an Agent and parse strict JSON into a Pydantic schema.
    Uses Agents SDK Runner.run() with a string input. The agent's instructions are already set.
    With output_type configured, final_output should already be a Pydantic instance.
    """
    runner = Runner()
    result = await runner.run(starting_agent=agent, input=user_text)
    
    # Get the final output from the result - should already be a Pydantic object
    if result.final_output is None:
        raise HTTPException(status_code=500, detail="Empty model response")
    
    # If it's already a Pydantic model, return it; otherwise parse and validate
    if isinstance(result.final_output, schema):
        return result.final_output
    elif isinstance(result.final_output, dict):
        return schema.model_validate(result.final_output)
    else:
        # Fallback: try to parse as JSON string
        data = json.loads(str(result.final_output))
        return schema.model_validate(data)

async def _text(agent, user_text: str) -> str:
    runner = Runner()
    result = await runner.run(starting_agent=agent, input=user_text)
    
    # Get the final output from the result
    text = str(result.final_output) if result.final_output else ""
    if not text:
        raise HTTPException(status_code=500, detail="Empty model response")
    return text.strip()

async def run_workflow(question: str):
    # 1) Classifier (weights that sum to 100)
    await emit("classifier:start", {"q": question})
    classifier_user = (
        "Return JSON with keys: legal, marketing, operations, strategy, analyst, finance. "
        "Numbers must sum to 100. Round as needed.\n"
        f'Question: "{question}"'
    )
    weights: ClassifierSchema = await _json(classifier_agent, classifier_agent.instructions, classifier_user, ClassifierSchema)
    weights = weights.normalized()
    await emit("classifier:end", {"weights": weights.model_dump()})

    # 2) Role agents (with tool calling). Each role agent will call its retrieval tool as needed.
    async def role_call(agent, role_name: str, schema):
        await emit(f"{role_name}:start")
        user = (
            f"From a {role_name.capitalize()} perspective, analyze: \"{question}\".\n"
            "Use your role-private retrieval tool first to ground your answer.\n"
            "Output ONLY your role JSON."
        )
        out = await _json(agent, agent.instructions, user, schema)
        await emit(f"{role_name}:end")
        return out

    tasks = [
        role_call(legal_agent, "legal", LegalSchema),
        role_call(marketing_agent, "marketing", MarketingSchema),
        role_call(ops_agent, "operations", OperationsSchema),
        role_call(strategy_agent, "strategy", StrategySchema),
        role_call(analyst_agent, "analyst", AnalystSchema),
        role_call(finance_agent, "finance", FinanceSchema),
    ]

    legal, marketing, operations, strategy, analyst, finance = await asyncio.gather(*tasks)
    answers = {
        "legal": legal.model_dump(),
        "marketing": marketing.model_dump(),
        "operations": operations.model_dump(),
        "strategy": strategy.model_dump(),
        "analyst": analyst.model_dump(),
        "finance": finance.model_dump(),
    }
    await emit("roles:end")

    # 3) Debate
    await emit("debate:start")
    debate_user = f"User question: {question}\nWeights: {weights.model_dump_json()}\nAnswers: {json.dumps(answers, ensure_ascii=False)}"
    debate: AddDebateSchema = await _json(debate_agent, debate_agent.instructions, debate_user, AddDebateSchema)
    await emit("debate:end", {"risk_score": debate.overall_risk_score})

    # 4) Combine
    await emit("combine:start")
    combine_user = (
        f"Question: {question}\n"
        f"Weights: {weights.model_dump_json()}\n"
        f"Answers: {json.dumps(answers, ensure_ascii=False)}\n"
        f"Debate: {debate.model_dump_json()}"
    )
    combined: CombinerSchema = await _json(combiner_agent, combiner_agent.instructions, combine_user, CombinerSchema)
    await emit("combine:end", {"confidence": combined.confidence})

    # 5) Formatter (structured output)
    await emit("format:start")
    formatted: FormatterSchema = await _json(formatter_agent, formatter_agent.instructions, f"final_json:\n{combined.model_dump_json()}", FormatterSchema)
    await emit("format:end")

    return {
        "formatted": formatted.model_dump(),
        "weights": weights.model_dump(),
        "debate": debate.model_dump(),
        "combined": combined.model_dump(),
        "roles": answers
    }

