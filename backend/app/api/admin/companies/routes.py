# 公司管理API路由

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.schemas.company import CompanyCreate, CompanyResponse
from app.models.user import User
from app.api.deps import get_current_admin_user
from app.services.admin.companies.company_service import CompanyService

router = APIRouter()


@router.get("", summary="获取公司列表")
async def get_companies(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取所有公司列表"""
    return CompanyService.get_companies(db)


@router.post("", response_model=CompanyResponse, summary="创建公司")
async def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """创建新公司"""
    return CompanyService.create_company(db, company)


@router.put("/{company_id}", response_model=CompanyResponse, summary="更新公司")
async def update_company(
    company_id: int,
    company: CompanyCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """更新公司信息"""
    return CompanyService.update_company(db, company_id, company)


@router.delete("/{company_id}", summary="删除公司")
async def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """删除公司"""
    return CompanyService.delete_company(db, company_id)


@router.get("/{company_id}", response_model=CompanyResponse, summary="获取公司详情")
async def get_company_detail(
    company_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取公司详情"""
    return CompanyService.get_company_detail(db, company_id)


@router.get("/{company_id}/users", summary="获取公司用户列表")
async def get_company_users(
    company_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取指定公司的所有用户"""
    return CompanyService.get_company_users(db, company_id)