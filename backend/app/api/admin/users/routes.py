"""用户管理API路由"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.database.connection import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, ResetPassword, UpdateWorkflows
from app.schemas.response import success_response
from app.api.deps import get_current_admin_user
from app.services.admin.users.user_service import UserService

router = APIRouter()


@router.get("/", summary="获取用户列表", tags=["用户管理"])
async def get_users(
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    role: Optional[str] = None,
    company_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取用户列表"""
    result = UserService.get_users(db, page, page_size, search, role, company_id, is_active)
    return success_response(data=result)


@router.post("/", summary="创建用户", tags=["用户管理"], status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """创建新用户"""
    user = UserService.create_user(db, user_data)
    return success_response(
        data={
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role
        },
        message="用户创建成功",
        code=201
    )


@router.get("/{user_id}", summary="获取用户详情", tags=["用户管理"])
async def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取用户详情"""
    user_info = UserService.get_user_by_id(db, user_id)
    return success_response(data=user_info)


@router.put("/{user_id}", summary="更新用户信息", tags=["用户管理"])
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """更新用户信息"""
    updated_user = UserService.update_user(db, user_id, user_data)
    return success_response(data=updated_user, message="用户信息更新成功")


@router.delete("/{user_id}", summary="删除用户", tags=["用户管理"])
async def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """删除用户"""
    UserService.delete_user(db, user_id)
    return success_response(message="用户删除成功")


@router.post("/{user_id}/reset-password", summary="重置用户密码", tags=["用户管理"])
async def reset_password(
    user_id: UUID,
    data: ResetPassword,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """重置用户密码"""
    UserService.reset_password(db, user_id, data.new_password)
    return success_response(message="密码重置成功")


@router.get("/{user_id}/workflows", summary="获取用户工作流权限", tags=["用户管理"])
async def get_user_workflows(
    user_id: UUID,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取用户的工作流权限"""
    workflows = UserService.get_user_workflows(db, user_id)
    return success_response(data=workflows)


@router.put("/{user_id}/workflows", summary="更新用户工作流权限", tags=["用户管理"])
async def update_user_workflows(
    user_id: UUID,
    data: UpdateWorkflows,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """更新用户的工作流权限"""
    result = UserService.update_user_workflows(db, user_id, data.workflow_ids)
    return success_response(data=result, message="工作流权限更新成功")
