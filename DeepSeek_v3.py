from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_deepseek import ChatDeepSeek

from langchain_community.chat_message_histories import ChatMessageHistory, RedisChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# 定义 Prompt 模板，加入 history
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一款智能 AI 助手，你的目标是为用户提供准确、有用且符合上下文的回答。"),
        MessagesPlaceholder(variable_name="history"),
        ("user", "{input}")
    ]
)

# 初始化 deepseek LLM
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.7,
    max_tokens=1024,
)

# 记忆管理
def get_session_history(session_id: str):
    # Redis 持久化记忆
    return RedisChatMessageHistory(
        session_id=session_id,
        url=os.environ.get("REDIS_URL", "redis://localhost:6379/0"),
        ttl=None  # None 表示永久保存记录；你也可以设置为 86400 表示 1 天
    )

# 构建支持对话记忆的 chain
deepseek_v3_chain_with_memory = RunnableWithMessageHistory(
    prompt | llm,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

"""
response = deepseek_v3_chain_with_memory.invoke(
    input={"input": "余弦是什么意思？请用最简单的语言解释"},
    config={"configurable": {"session_id": "1"}}
)

print(response)

response = deepseek_v3_chain_with_memory.invoke(
    input={"input": "还是没懂。"},
    config={"configurable": {"session_id": "2"}}
)

print(response)

response = deepseek_v3_chain_with_memory.invoke(
    input={"input": "还是没懂。"},
    config={"configurable": {"session_id": "1"}}
)

print(response)
"""
