"""统一 API 响应模型"""

from typing import TypeVar, Generic, Optional, Any
from pydantic import BaseModel
from fastapi import Request

T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """统一 API 响应格式"""
    success: bool
    code: int
    message: str
    data: Optional[T] = None
    request_id: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "code": 200,
                "message": "操作成功",
                "data": {},
                "request_id": "uuid-string"
            }
        }


def get_request_id(request: Request) -> Optional[str]:
    """
    从 Request 对象中获取 request_id
    
    Args:
        request: FastAPI Request 对象
        
    Returns:
        request_id 字符串，如果不存在则返回 None
    """
    return getattr(request.state, "request_id", None)


def success_response(
    data: Any = None,
    message: str = "操作成功",
    code: int = 200,
    request_id: Optional[str] = None
) -> dict:
    """
    成功响应
    
    Args:
        data: 业务数据
        message: 提示信息
        code: 业务状态码
        request_id: 请求追踪ID（可选，如果不传则为 None）
        
    Returns:
        统一格式的响应字典
        
    Example:
        # 不带 request_id
        return success_response(data={"user": "admin"})
        
        # 带 request_id
        request_id = get_request_id(request)
        return success_response(data={"user": "admin"}, request_id=request_id)
    """
    return {
        "success": True,
        "code": code,
        "message": message,
        "data": data,
        "request_id": request_id
    }


def error_response(
    message: str = "操作失败",
    code: int = 400,
    data: Any = None,
    request_id: Optional[str] = None
) -> dict:
    """
    错误响应
    
    Args:
        message: 错误信息
        code: 错误状态码
        data: 额外数据（如验证错误详情）
        request_id: 请求追踪ID（可选，如果不传则为 None）
        
    Returns:
        统一格式的错误响应字典
    """
    return {
        "success": False,
        "code": code,
        "message": message,
        "data": data,
        "request_id": request_id
    }
