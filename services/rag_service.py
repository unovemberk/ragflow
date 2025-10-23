import httpx
from config import SERVICE_CONFIG

RAGFLOW_URL = SERVICE_CONFIG["ragflow"]["base_url"]
KB_ID = SERVICE_CONFIG["ragflow"]["knowledge_base_id"]


async def rag_retrieve(query: str) -> str:
    """调用Ragflow检索知识库相关内容"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{RAGFLOW_URL}/api/v1/retrieve",
                json={
                    "knowledge_base_id": KB_ID,
                    "query": query,
                    "top_k": 3  # 取最相关的3条片段
                }
            )
            response.raise_for_status()
            results = response.json()
            # 拼接检索到的上下文
            context = "\n\n".join([item["content"] for item in results.get("documents", [])])
            return context
    except Exception as e:
        print(f"Ragflow检索失败: {str(e)}")
        return ""  # 检索失败时返回空上下文（仅用模型回答）


async def upload_file_to_ragflow(file_content: str, file_name: str) -> bool:
    """上传纯文本文件到Ragflow知识库"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{RAGFLOW_URL}/api/v1/documents",
                files={
                    "file": (file_name, file_content, "text/plain")
                },
                data={"knowledge_base_id": KB_ID}
            )
            response.raise_for_status()
            return True
    except Exception as e:
        print(f"文件上传到Ragflow失败: {str(e)}")
        return False