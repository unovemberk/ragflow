from fastapi import FastAPI
from api.chat import router as chat_router
from api.session import router as session_router
from config import API_PREFIX

app = FastAPI(title="RAG模型集成服务", version="1.0")

# 注册路由
app.include_router(chat_router, prefix=API_PREFIX)
app.include_router(session_router, prefix=API_PREFIX)


@app.get("/health")
def health_check():
    """服务健康检查"""
    return {"status": "healthy"}