import httpx
from config import SERVICE_CONFIG

OLLAMA_URL = SERVICE_CONFIG["ollama"]["base_url"]
OLLAMA_MODEL = SERVICE_CONFIG["ollama"]["default_model"]


async def call_ollama(prompt: str) -> str:
    """调用Ollama生成回答"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{OLLAMA_URL}/api/generate",
                json={
                    "model": "qwen:7b-chat",
                    "prompt": prompt,
                    "stream": True
                }
            )
            response.raise_for_status()
            result = response.json()
            return result.get("response", "模型未返回结果")
    except Exception as e:
        print(f"Ollama调用失败: {str(e)}")
        return f"模型服务异常: {str(e)}"


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