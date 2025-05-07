from fastapi import APIRouter
from fastapi.responses import JSONResponse
from langchain_community.chat_message_histories import RedisChatMessageHistory
import os

router = APIRouter()

redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379/0")

@router.get("/history/{session_id}")
async def get_history(session_id: str):
    history = RedisChatMessageHistory(session_id=session_id, url=redis_url)
    messages = history.messages

    formatted_messages = [
        {
            "type": 0 if msg.type == "human" else 1,
            "content": msg.content
        }
        for msg in messages
    ]

    return JSONResponse(content={"history": formatted_messages})
