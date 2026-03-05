"""公司管理API路由"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.company import CompanyCreate
from app.schemas.response import success_response
from app.models.user import User
from app.api.deps import get_current_admin_user
from app.services.admin.companies.company_service import CompanyService

router = APIRouter()


@router.get("", summary="获取公司列表")
async def get_companies(
    page: int = 1,
    page_size: int = 10,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取所有公司列表（支持分页）"""
    result = CompanyService.get_companies(db, page, page_size)
    return success_response(data=result)


@router.post("", summary="创建公司", status_code=status.HTTP_201_CREATED)
async def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """创建新公司"""
    new_company = CompanyService.create_company(db, company)
    return success_response(
        data={
            "id": new_company.id,
            "name": new_company.name,
            "domain": new_company.domain,
            "is_active": new_company.is_active
        },
        message="公司创建成功",
        code=201
    )


@router.put("/{company_id}", summary="更新公司")
async def update_company(
    company_id: int,
    company: CompanyCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """更新公司信息"""
    updated_company = CompanyService.update_company(db, company_id, company)
    return success_response(
        data={
            "id": updated_company.id,
            "name": updated_company.name,
            "domain": updated_company.domain,
            "is_active": updated_company.is_active
        },
        message="公司信息更新成功"
    )


@router.delete("/{company_id}", summary="删除公司")
async def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """删除公司"""
    CompanyService.delete_company(db, company_id)
    return success_response(message="公司删除成功")


@router.get("/{company_id}", summary="获取公司详情")
async def get_company_detail(
    company_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取公司详情"""
    company = CompanyService.get_company_detail(db, company_id)
    return success_response(data={
        "id": company.id,
        "name": company.name,
        "domain": company.domain,
        "is_active": company.is_active,
        "created_at": company.created_at.isoformat() if company.created_at else None,
        "updated_at": company.updated_at.isoformat() if company.updated_at else None
    })


@router.get("/{company_id}/users", summary="获取公司用户列表")
async def get_company_users(
    company_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """获取指定公司的所有用户"""
    users = CompanyService.get_company_users(db, company_id)
    return success_response(data={"users": users})
