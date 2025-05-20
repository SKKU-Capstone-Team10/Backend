import requests

from fastapi import HTTPException

from core.config import settings

# Pass the user query to RAG server
# Get reply from the RAG server
def get_ai_reply(content: str, is_first_chat: bool) -> str:
    try:
        response = requests.post(
            f"{settings.RAG_HOST}{settings.RAG_ROUTE}",
            json={
                "query": content,
                "is_first_chat": is_first_chat
            },
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        title = result.get("title", None)
        reply = result.get("reply", "No reply from RAG server")
        ticker = result.get("ticker", "No ticker pased from RAG server")
        res = {
            "title": title,
            "reply": reply,
            "ticker": ticker
        }
        return res
    
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail="Exception while requesting RAG server")