from fastapi import APIRouter
from fastapi.responses import JSONResponse
from langchain_core.prompts import ChatPromptTemplate
from langchain_deepseek import ChatDeepSeek
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_core.messages import BaseMessage
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# Redis 配置
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# 定义 Prompt 模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一名善于总结的助手，请根据下面这段对话内容，生成一个简短（越短越好，最长不超过20字）的对话标题，能够准确反映对话的主题。请注意，标题应当和聊天的语言保持相同，例如人类和ai用英文聊天，你就应该输出英文标题；例如人类和ai用中文聊天，你就应该输出中文标题。"),
    ("user", "{input}")
])

# 初始化 DeepSeek LLM
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.2,
    max_tokens=1024,
)

# 构建链
summarize_llm = prompt | llm

def get_session_history_text(session_id: str) -> str:
    """
    使用 RedisChatMessageHistory 获取会话历史并转为格式化字符串
    """
    history = RedisChatMessageHistory(
        session_id=session_id,
        url=REDIS_URL
    )

    messages: list[BaseMessage] = history.messages

    if not messages:
        return ""

    # 格式化为：用户：... 助手：... 的形式
    lines = []
    for msg in messages:
        if msg.type == "human":
            lines.append(f"human：{msg.content}")
        elif msg.type == "AIMessageChunk":
            lines.append(f"ai：{msg.content}")
    return "\n".join(lines)


router = APIRouter()

# 封装接口
@router.get("/summary/{session_id}")
async def generate_title(session_id: str):
    history_text = get_session_history_text(session_id)

    if not history_text:
        return JSONResponse(content={"title": ""})

    try:
        response = summarize_llm.invoke({"input": history_text})
        return JSONResponse(content={"title": response.content.strip()})
    except Exception as e:
        return JSONResponse(content={"title": ""})

"""
if __name__ == '__main__':
    session_id = "session_1746697374822_eb475112-0646-4491-8dd0-25bbf8be27ac"

    history_text = get_session_history_text(session_id)

    print("历史记录：", history_text)

    if not history_text:
        print("未找到历史记录，无法生成标题")
    else:
        response = summarize_llm.invoke({"input": history_text})
        print("生成的标题：", response.content)
"""