### Cursor build rules (Python + OpenAI Agents SDK)
- Use FastAPI for HTTP.
- Use OpenAI **Agents SDK** for agents/tools/handoffs.
- Retrieval must use per-role vector stores via function tools.
- Classifier weights must sum to 100 (round, then drift-correct).
- Formatter must output bold headers + bullets, no code fences/tables.
- Ensure all files are Python where applicable.

