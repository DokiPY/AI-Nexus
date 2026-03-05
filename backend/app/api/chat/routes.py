"""聊天API路由"""

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database.connection import get_db
from app.api.deps import get_current_active_user
from app.models.user import User
from app.schemas.response import success_response
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
    """获取指定工作流的聊天历史"""
    data = ChatService.get_chat_history(db, current_user, workflow_id)
    return success_response(data=data)


@router.post("/{workflow_id}/messages", summary="发送消息（流式）")
async def send_message_stream(
    workflow_id: int,
    message_data: ChatMessage,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """流式发送聊天消息，返回 SSE 事件流"""
    return StreamingResponse(
        ChatService.send_message_stream(
            db, current_user, workflow_id, message_data.message
        ),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )


@router.delete("/{workflow_id}", summary="清空聊天记录")
async def clear_chat_history(
    workflow_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """清空聊天记录（软删除）"""
    ChatService.clear_chat_history(db, current_user.id, workflow_id)
    return success_response(message="聊天记录已清空")
