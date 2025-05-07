from Agent_tools import tools

from langchain.agents import AgentExecutor, create_react_agent
from langchain_deepseek import ChatDeepSeek
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain import hub

from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# Agent 的提示词
prompt = hub.pull("hwchase17/react")

# 初始化 LLM
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0.7,
    max_tokens=1024,
)

# 初始化带工具的 Agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent,
                               tools=tools,
                               verbose=True,
                               handle_parsing_errors=True,
                               max_iterations=10)

# prompt 实际上由 Agent 封装，无需自定义，但 memory 需要加上
def get_session_history(session_id: str):
    return RedisChatMessageHistory(
        session_id=session_id,
        url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        ttl=None
    )

# 将 agent 封装为支持历史的 chain
deepseek_v3_agent_chain_with_memory = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

"""
response = deepseek_v3_agent_chain_with_memory.stream(
    input={"input": "北京的天气如何？"},
    config={"configurable": {"session_id": "session_1746627103884_fa9ac049-c626-4dc1-982b-1f45b0e434ab"}}
)

for chunk in response:
    print(chunk)
"""