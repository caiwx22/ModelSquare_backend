from DeepSeek_v3 import deepseek_v3_chain_with_memory
from DeepSeek_v3_agent import deepseek_v3_agent_chain_with_memory
from Chat_history import router as history_router

from fastapi import FastAPI
from langserve import add_routes


app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="基于 LangChain 的 LLM 及 Agent 的调用。",
)

# deepseek v3 路由
add_routes(app, deepseek_v3_chain_with_memory, path="/chat/deepseek_v3")

# deepseek v3 agent 路由
add_routes(app, deepseek_v3_agent_chain_with_memory, path="/chat/deepseek_v3_agent")

# 所有历史记录路由
app.include_router(history_router)


if __name__ == "__main__":
    from fastapi.middleware.cors import CORSMiddleware

    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
