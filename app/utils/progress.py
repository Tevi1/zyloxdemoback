# Progress emitter (swap to SSE/WebSockets in prod)
import json
import logging
log = logging.getLogger("progress")

async def emit(stage: str, payload: dict | None = None):
    log.info("[progress] %s :: %s", stage, json.dumps(payload or {}))

