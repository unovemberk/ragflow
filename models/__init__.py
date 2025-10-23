from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
from config import MYSQL_CONFIG

# 数据库连接
DB_URL = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}"
engine = create_engine(DB_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    """用户表（可与前端项目用户体系关联）"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)  # 用户名（唯一）
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关联会话
    sessions = relationship("Session", back_populates="user", cascade="all, delete-orphan")


class Session(Base):
    """会话表（每个会话属于一个用户）"""
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # 所属用户
    session_name = Column(String(100), default="新会话")  # 会话名称
    is_deleted = Column(Boolean, default=False)  # 软删除标记
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关联用户和消息
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session", cascade="all, delete-orphan")


class Message(Base):
    """消息表（每条消息属于一个会话）"""
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)  # 所属会话
    role = Column(String(10))  # 角色：user/ai
    content = Column(Text)  # 消息内容
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关联会话
    session = relationship("Session", back_populates="messages")


# 创建表（首次运行时执行）
Base.metadata.create_all(bind=engine)