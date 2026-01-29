from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.database.connection import Base

class Workflow(Base):
    __tablename__ = "workflows"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    n8n_webhook_url = Column(Text, nullable=False)
    http_method = Column(String(10), default="POST")  # POST, GET, PUT, DELETE
    icon = Column(String(255))
    category = Column(String(100), default="办公助手")  # 办公助手, 数据分析, 客户服务, 开发工具
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class CompanyWorkflow(Base):
    __tablename__ = "company_workflows"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    
    __table_args__ = (UniqueConstraint('company_id', 'workflow_id'),)

class UserWorkflow(Base):
    __tablename__ = "user_workflows"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    
    __table_args__ = (UniqueConstraint('user_id', 'workflow_id'),)

class ChatSession(Base):
    """会话表"""
    __tablename__ = "chat_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False, index=True)
    title = Column(String(255))
    is_deleted = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ChatLog(Base):
    """聊天记录表"""
    __tablename__ = "chat_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False, index=True)
    role = Column(String(50), nullable=False)  # user or ai
    message = Column(Text, nullable=False)
    
    # 元数据
    response_time_ms = Column(Integer)
    token_count = Column(Integer)
    error_message = Column(Text)
    
    # 软删除
    is_deleted = Column(Boolean, default=False, index=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    __table_args__ = (
        Index('idx_session_created', 'session_id', 'created_at'),
        Index('idx_user_workflow', 'user_id', 'workflow_id', 'is_deleted'),
    )