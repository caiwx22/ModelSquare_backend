from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_deepseek import ChatDeepSeek

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from dotenv import load_dotenv

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
    max_tokens=512,
)

# 存储对话历史
store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

# 构建支持对话记忆的 chain
chain_with_memory = RunnableWithMessageHistory(
    prompt | llm,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

"""
response = chain_with_memory.invoke(
    input={"input": "余弦是什么意思？请用最简单的语言解释"},
    config={"configurable": {"session_id": "1"}}
)

print(response)

response = chain_with_memory.invoke(
    input={"input": "还是没懂。"},
    config={"configurable": {"session_id": "2"}}
)

print(response)

response = chain_with_memory.invoke(
    input={"input": "还是没懂。"},
    config={"configurable": {"session_id": "1"}}
)

print(response)
"""
