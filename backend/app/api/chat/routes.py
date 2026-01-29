from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.connection import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.services.chat.chat_service import ChatService

router = APIRouter()

class ChatMessage(BaseModel):
    message: str

@router.get("/{workflow_id}", summary="获取聊天历史")
async def get_chat_history(
    workflow_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取聊天历史"""
    return ChatService.get_chat_history(db, current_user, workflow_id)

@router.post("/{workflow_id}/messages", summary="发送消息")
async def send_message(
    workflow_id: int,
    message_data: ChatMessage,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """发送聊天消息"""
    return await ChatService.send_message(db, current_user, workflow_id, message_data.message)

@router.delete("/{workflow_id}", summary="清空聊天记录")
async def clear_chat_history(
    workflow_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """清空聊天记录（软删除）"""
    return ChatService.clear_chat_history(db, current_user.id, workflow_id)