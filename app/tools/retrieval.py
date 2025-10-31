# Function tools for role-private retrieval using Vector Stores (Agents SDK tool calling)
# What this file contains:
# - One Python function per role, decorated as an Agents SDK function tool.
# - Each calls OpenAI Vector Stores search and returns a text blob (title + snippet lines).

from typing import Annotated
from agents import function_tool
from app.services.openai_client import client
from app.core.config import settings

async def _search(store_id: str, query: str, k: int = 6) -> str:
    try:
        res = await client.vector_stores.search(vector_store_id=store_id, query=query, max_num_results=k)
        lines = []
        for r in res:
            title = getattr(r, "filename", None) or getattr(r, "document_id", None) or "doc"
            snippet = getattr(r, "snippet", None) or getattr(r, "text", None) or ""
            lines.append(f"[{title}] {snippet}".strip())
        return "\n".join(lines) if lines else "(no role-private context found)"
    except Exception as e:
        return f"(search error: {e})"

@function_tool
def legal_retrieval(question: Annotated[str, "User question string"]) -> Annotated[str, "Legal private context text blob"]:
    """Retrieve legal/compliance passages for the question (privacy/AI/state laws, sectoral rules, IP/licensing, TCPA/CAN-SPAM, accessibility, export/sanctions). Returns a newline-joined blob with [title] snippet."""
    return _search.__wrapped__(settings.VECTOR_STORE_LEGAL, f'Question: "{question}"\nRetrieve legal/compliance clauses and checklists; include titles/IDs.')  # type: ignore

@function_tool
def marketing_retrieval(question: Annotated[str, "User question string"]) -> Annotated[str, "Marketing private context text blob"]:
    """Retrieve messaging frameworks, disclosure/endorsement rules, brand voice guides for the question."""
    return _search.__wrapped__(settings.VECTOR_STORE_MARKETING, f'Question: "{question}"\nRetrieve messaging frameworks and disclosure rules; include titles/IDs.')  # type: ignore

@function_tool
def ops_retrieval(question: Annotated[str, "User question string"]) -> Annotated[str, "Ops private context text blob"]:
    """Retrieve SOPs, runbooks, risk registers, governance procedures, rollout checklists for the question."""
    return _search.__wrapped__(settings.VECTOR_STORE_OPS, f'Question: "{question}"\nRetrieve SOPs/runbooks/checklists; include titles/IDs.')  # type: ignore

@function_tool
def strategy_retrieval(question: Annotated[str, "User question string"]) -> Annotated[str, "Strategy private context text blob"]:
    """Retrieve strategy memos, competitive notes, prioritization, pricing/segmentation for the question."""
    return _search.__wrapped__(settings.VECTOR_STORE_STRATEGY, f'Question: "{question}"\nRetrieve strategy memos/competitive notes; include titles/IDs.')  # type: ignore

@function_tool
def analyst_retrieval(question: Annotated[str, "User question string"]) -> Annotated[str, "Analyst private context text blob"]:
    """Retrieve KPI definitions, benchmarks, forecast sheets, experiment results, market sizing for the question."""
    return _search.__wrapped__(settings.VECTOR_STORE_ANALYST, f'Question: "{question}"\nRetrieve KPIs/benchmarks/forecasts; include titles/IDs.')  # type: ignore

@function_tool
def finance_retrieval(question: Annotated[str, "User question string"]) -> Annotated[str, "Finance private context text blob"]:
    """Retrieve budgets, pro formas, unit economics, tooling costs, ROI analyses for the question."""
    return _search.__wrapped__(settings.VECTOR_STORE_FINANCE, f'Question: "{question}"\nRetrieve budgets/unit economics/ROI; include titles/IDs.')  # type: ignore

