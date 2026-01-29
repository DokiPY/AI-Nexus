# 用户管理API路由

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from app.database.connection import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.api.deps import get_current_admin_user
from app.services.admin.users.UserTable import UserTableService
from app.services.admin.users.UserFormDialog import UserFormDialogService
from app.services.admin.users.WorkflowPermissionDialog import WorkflowPermissionDialogService

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
    return UserTableService.get_users(db, page, page_size, search, role, company_id, is_active)


@router.post("/", summary="创建用户", tags=["用户管理"])
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """创建新用户"""
    return UserFormDialogService.create_user(db, user_data)


@router.get("/{user_id}", summary="获取用户详情", tags=["用户管理"])
async def get_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取用户详情"""
    return UserFormDialogService.get_user_by_id(db, user_id)


@router.put("/{user_id}", summary="更新用户信息", tags=["用户管理"])
async def update_user(
    user_id: UUID,
    user_data: dict,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """更新用户信息"""
    return UserFormDialogService.update_user(db, user_id, user_data)


@router.delete("/{user_id}", summary="删除用户", tags=["用户管理"])
async def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """删除用户"""
    UserTableService.delete_user(db, user_id)
    return {"message": "删除成功"}


@router.post("/{user_id}/reset-password", summary="重置用户密码", tags=["用户管理"])
async def reset_password(
    user_id: UUID,
    data: dict,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """重置用户密码"""
    return UserFormDialogService.reset_password(db, user_id, data.get("new_password"))


@router.get("/{user_id}/workflows", summary="获取用户工作流权限", tags=["用户管理"])
async def get_user_workflows(
    user_id: UUID,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取用户的工作流权限"""
    return WorkflowPermissionDialogService.get_user_workflows(db, user_id)


@router.put("/{user_id}/workflows", summary="更新用户工作流权限", tags=["用户管理"])
async def update_user_workflows(
    user_id: UUID,
    data: dict,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """更新用户的工作流权限"""
    workflow_ids = data.get("workflow_ids", [])
    return WorkflowPermissionDialogService.update_user_workflows(db, user_id, workflow_ids)