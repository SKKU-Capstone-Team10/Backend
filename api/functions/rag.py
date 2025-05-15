import requests

from fastapi import HTTPException

from core.config import settings

# Pass the user query to RAG server
# Get reply from the RAG server
def get_ai_reply(content: str) -> str:
    try:
        response = requests.post(
            f"{settings.RAG_HOST}{settings.RAG_ROUTE}",
            json={"query": content},
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return result.get("reply", "No reply from RAG server")
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="Exception while requesting RAG server")