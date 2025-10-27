import httpx
from config import SERVICE_CONFIG

OLLAMA_URL = SERVICE_CONFIG["ollama"]["base_url"]
OLLAMA_MODEL = SERVICE_CONFIG["ollama"]["default_model"]


async def call_ollama(prompt: str) -> str:
    """调用Ollama的聊天接口（适配qwen:7b-chat等聊天模型）"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/chat",  # 改用聊天接口
                json={
                    "model": OLLAMA_MODEL,  # 即"qwen:7b-chat"
                    "messages": [{"role": "user", "content": prompt}],  # 聊天模型要求的消息格式
                    "stream": False  # 关闭流式响应
                }
            )
            response.raise_for_status()  # 抛出HTTP错误（如404、500）
            result = response.json()
            # 从聊天接口的响应中提取回答（格式与/generate不同）
            return result["message"]["content"]
    except Exception as e:
        print(f"Ollama调用失败: {str(e)}")  # 打印具体错误（便于排查）
        return f"模型服务异常: {str(e)}"  # 返回详细错误信息


# 如需支持Xinference，可添加类似调用函数
async def call_xinference(prompt: str) -> str:
    """调用Xinference生成回答（示例）"""
    XINFERENCE_URL = SERVICE_CONFIG["xinference"]["base_url"]
    XINFERENCE_MODEL = SERVICE_CONFIG["xinference"]["default_model"]
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{XINFERENCE_URL}/v1/chat/completions",
                json={
                    "model": XINFERENCE_MODEL,
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Xinference调用失败: {str(e)}")
        return f"模型服务异常: {str(e)}"