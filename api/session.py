from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from services.db_service import get_db, get_or_create_user, create_session, delete_session, get_user_sessions

router = APIRouter()


class SessionCreateRequest(BaseModel):
    username: str  # 用户名（标识用户身份）
    session_name: str = "新会话"


class SessionDeleteRequest(BaseModel):
    username: str
    session_id: int


@router.post("/session/create")
def create_new_session(req: SessionCreateRequest, db: Session = Depends(get_db)):
    """创建新会话"""
    user = get_or_create_user(db, req.username)
    session = create_session(db, user.id, req.session_name)
    return {
        "code": 200,
        "data": {
            "session_id": session.id,
            "session_name": session.session_name,
            "created_at": session.created_at
        }
    }


@router.post("/session/delete")
def delete_existing_session(req: SessionDeleteRequest, db: Session = Depends(get_db)):
    """删除会话"""
    user = get_or_create_user(db, req.username)
    success = delete_session(db, req.session_id, user.id)
    if not success:
        raise HTTPException(status_code=404, detail="会话不存在或不属于该用户")
    return {"code": 200, "data": "删除成功"}


@router.get("/sessions")
def get_user_session_list(username: str, db: Session = Depends(get_db)):
    """获取用户的所有会话"""
    user = get_or_create_user(db, req.username)
    sessions = get_user_sessions(db, user.id)
    return {
        "code": 200,
        "data": [
            {
                "session_id": s.id,
                "session_name": s.session_name,
                "updated_at": s.updated_at
            } for s in sessions
        ]
    }