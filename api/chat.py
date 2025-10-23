from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from pydantic import BaseModel
from services.db_service import get_db, get_or_create_user, add_message, get_session_messages, get_user_sessions
from services.rag_service import rag_retrieve, upload_file_to_ragflow
from services.model_service import call_ollama  # 可切换为call_xinference

router = APIRouter()


class ChatRequest(BaseModel):
    username: str
    session_id: int
    message: str  # 用户输入的消息
    use_rag: bool = True  # 是否使用知识库（默认使用）


@router.post("/chat")
async def chat_with_model(req: ChatRequest, db: Session = Depends(get_db)):
    """发送消息，获取模型回答（结合RAG）"""
    # 1. 验证用户和会话
    user = get_or_create_user(db, req.username)
    sessions = get_user_sessions(db, user.id)
    if not any(s.id == req.session_id for s in sessions):
        raise HTTPException(status_code=404, detail="会话不存在")

    # 2. 存储用户消息
    add_message(db, req.session_id, "user", req.message)

    # 3. RAG流程：检索知识库（如果启用）
    context = ""
    if req.use_rag:
        context = await rag_retrieve(req.message)

    # 4. 构造Prompt调用模型
    prompt = f"根据以下上下文回答问题（如果没有上下文则直接回答）：\n{context}\n\n问题：{req.message}"
    ai_response = await call_ollama(prompt)  # 可替换为call_xinference

    # 5. 存储AI回答
    add_message(db, req.session_id, "ai", ai_response)

    return {
        "code": 200,
        "data": {
            "ai_response": ai_response,
            "context_used": bool(context)  # 标识是否使用了知识库
        }
    }


@router.get("/session/messages")
def get_session_chat_history(username: str, session_id: int, db: Session = Depends(get_db)):
    """获取会话的历史消息"""
    user = get_or_create_user(db, username)
    messages = get_session_messages(db, session_id, user.id)
    return {
        "code": 200,
        "data": [
            {
                "id": m.id,
                "role": m.role,
                "content": m.content,
                "created_at": m.created_at
            } for m in messages
        ]
    }


@router.post("/file/upload")
async def upload_text_file(
    username: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """上传纯文本文件到知识库（支持.txt/.md等）"""
    # 验证文件类型（仅纯文本）
    if not file.content_type.startswith("text/"):
        raise HTTPException(status_code=400, detail="仅支持纯文本文件")
    
    # 读取文件内容
    content = await file.read()
    try:
        content_str = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="文件编码错误，无法解析为文本")
    
    # 上传到Ragflow
    success = await upload_file_to_ragflow(content_str, file.filename)
    if success:
        return {"code": 200, "data": "文件上传并添加到知识库成功"}
    else:
        raise HTTPException(status_code=500, detail="文件上传失败")