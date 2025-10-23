from sqlalchemy.orm import Session
from models import SessionLocal, User, Session, Message
from datetime import datetime


def get_db():
    """获取数据库会话（依赖注入用）"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 用户相关操作
def get_or_create_user(db: Session, username: str):
    """获取用户，不存在则创建"""
    user = db.query(User).filter(User.username == username).first()
    if not user:
        user = User(username=username)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user


# 会话相关操作
def create_session(db: Session, user_id: int, session_name: str = "新会话"):
    """创建新会话"""
    session = Session(user_id=user_id, session_name=session_name)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def delete_session(db: Session, session_id: int, user_id: int):
    """删除会话（软删除）"""
    session = db.query(Session).filter(
        Session.id == session_id,
        Session.user_id == user_id
    ).first()
    if session:
        session.is_deleted = True
        db.commit()
        return True
    return False


def get_user_sessions(db: Session, user_id: int):
    """获取用户的所有有效会话"""
    return db.query(Session).filter(
        Session.user_id == user_id,
        Session.is_deleted == False
    ).order_by(Session.updated_at.desc()).all()


# 消息相关操作
def add_message(db: Session, session_id: int, role: str, content: str):
    """添加消息到会话"""
    message = Message(session_id=session_id, role=role, content=content)
    db.add(message)
    # 更新会话的更新时间
    db.query(Session).filter(Session.id == session_id).update({
        Session.updated_at: datetime.utcnow()
    })
    db.commit()
    db.refresh(message)
    return message


def get_session_messages(db: Session, session_id: int, user_id: int):
    """获取会话的消息（验证会话归属）"""
    # 先验证会话是否属于该用户
    session = db.query(Session).filter(
        Session.id == session_id,
        Session.user_id == user_id,
        Session.is_deleted == False
    ).first()
    if not session:
        return []
    # 获取消息（按时间升序）
    return db.query(Message).filter(
        Message.session_id == session_id
    ).order_by(Message.created_at.asc()).all()