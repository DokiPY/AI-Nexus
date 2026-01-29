from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime
import time

from app.models.workflow import Workflow, UserWorkflow, ChatLog, ChatSession
from app.models.user import User
from app.services.n8n_service import N8NService


class ChatService:
    """聊天服务"""
    
    @staticmethod
    def check_workflow_permission(db: Session, user: User, workflow_id: int) -> Workflow:
        """检查用户是否有权限访问工作流"""
        if user.role != "admin":
            permission = db.query(UserWorkflow).filter(
                UserWorkflow.user_id == user.id,
                UserWorkflow.workflow_id == workflow_id
            ).first()
            
            if not permission:
                raise HTTPException(
                    status_code=403,
                    detail="您没有权限使用该工作流，请联系管理员开通权限"
                )
        
        workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
        if not workflow:
            raise HTTPException(status_code=404, detail="工作流不存在")
        
        return workflow
    
    @staticmethod
    def get_or_create_session(db: Session, user_id: int, workflow_id: int, title: str = "新对话") -> ChatSession:
        """获取或创建聊天会话"""
        session = db.query(ChatSession).filter(
            ChatSession.user_id == user_id,
            ChatSession.workflow_id == workflow_id,
            ChatSession.is_deleted == False
        ).order_by(ChatSession.updated_at.desc()).first()
        
        if not session:
            session = ChatSession(
                user_id=user_id,
                workflow_id=workflow_id,
                title=title
            )
            db.add(session)
            db.commit()
            db.refresh(session)
        
        return session
    
    @staticmethod
    def get_chat_history(db: Session, user: User, workflow_id: int):
        """获取聊天历史"""
        workflow = ChatService.check_workflow_permission(db, user, workflow_id)
        session = ChatService.get_or_create_session(db, user.id, workflow_id)
        
        chat_logs = db.query(ChatLog).filter(
            ChatLog.session_id == session.id,
            ChatLog.is_deleted == False
        ).order_by(ChatLog.created_at.asc()).all()
        
        return {
            "workflow": {
                "id": workflow.id,
                "name": workflow.name,
                "description": workflow.description,
                "icon": workflow.icon
            },
            "session_id": session.id,
            "messages": [{
                "id": log.id,
                "role": log.role,
                "message": log.message,
                "created_at": log.created_at.isoformat()
            } for log in chat_logs]
        }
    
    @staticmethod
    async def send_message(db: Session, user: User, workflow_id: int, message: str):
        """发送聊天消息"""
        workflow = ChatService.check_workflow_permission(db, user, workflow_id)
        session = ChatService.get_or_create_session(db, user.id, workflow_id, message[:50])
        
        # 保存用户消息
        user_message = ChatLog(
            session_id=session.id,
            user_id=user.id,
            workflow_id=workflow_id,
            role="user",
            message=message
        )
        db.add(user_message)
        db.commit()
        db.refresh(user_message)
        
        # 调用N8N工作流
        user_info = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "company_id": user.company_id
        }
        
        start_time = time.time()
        ai_response = await N8NService.call_workflow(
            webhook_url=workflow.n8n_webhook_url,
            user_message=message,
            user_info=user_info
        )
        response_time_ms = int((time.time() - start_time) * 1000)
        
        # 保存AI回复
        ai_message = ChatLog(
            session_id=session.id,
            user_id=user.id,
            workflow_id=workflow_id,
            role="ai",
            message=ai_response,
            response_time_ms=response_time_ms
        )
        db.add(ai_message)
        
        # 更新会话时间
        session.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(ai_message)
        
        return {
            "user_message": {
                "id": user_message.id,
                "role": "user",
                "message": user_message.message,
                "created_at": user_message.created_at.isoformat()
            },
            "ai_message": {
                "id": ai_message.id,
                "role": "ai",
                "message": ai_message.message,
                "created_at": ai_message.created_at.isoformat()
            }
        }
    
    @staticmethod
    def clear_chat_history(db: Session, user_id: int, workflow_id: int):
        """清空聊天记录（软删除）"""
        session = db.query(ChatSession).filter(
            ChatSession.user_id == user_id,
            ChatSession.workflow_id == workflow_id,
            ChatSession.is_deleted == False
        ).order_by(ChatSession.updated_at.desc()).first()
        
        if session:
            db.query(ChatLog).filter(
                ChatLog.session_id == session.id
            ).update({"is_deleted": True})
            
            session.is_deleted = True
            db.commit()
        
        return {"message": "聊天记录已清空"}
