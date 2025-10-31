# Shared AsyncOpenAI client (used by function tools)
from openai import AsyncOpenAI
from app.core.config import settings

# Only pass org_id and project_id if they're actually set (not comments or empty)
def is_valid_value(val):
    if not val:
        return False
    val_str = str(val).strip()
    if val_str.startswith('#') or val_str == '':
        return False
    return True

client_kwargs = {'api_key': settings.OPENAI_API_KEY}
if is_valid_value(settings.OPENAI_ORG_ID):
    client_kwargs['organization'] = settings.OPENAI_ORG_ID
if is_valid_value(settings.OPENAI_PROJECT_ID):
    client_kwargs['project'] = settings.OPENAI_PROJECT_ID

client = AsyncOpenAI(**client_kwargs)

