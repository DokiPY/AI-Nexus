"""管理员工作流管理API路由"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.api.deps import get_current_admin_user
from app.models.user import User
from app.models.workflow import Workflow, UserWorkflow, CompanyWorkflow
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate
from app.schemas.response import success_response
from app.core.errors.exceptions import NotFoundException

router = APIRouter()


@router.get("/categories", summary="获取所有工作流分类")
async def get_workflow_categories(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """管理员获取所有工作流分类（从已有工作流中提取）"""
    categories = db.query(Workflow.category).filter(
        Workflow.is_active == True
    ).distinct().all()

    category_list = sorted(set(cat[0] for cat in categories if cat[0]))

    return success_response(data={"categories": category_list})


@router.get("/", summary="获取所有工作流")
async def get_all_workflows(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """管理员获取所有工作流列表"""
    workflows = db.query(Workflow).filter(Workflow.is_active == True).all()
    
    workflow_list = [{
        "id": w.id,
        "name": w.name,
        "description": w.description,
        "icon": w.icon,
        "category": w.category,
        "n8n_webhook_url": w.n8n_webhook_url,
        "http_method": getattr(w, 'http_method', 'POST'),
        "stream_enabled": getattr(w, 'stream_enabled', True),
        "created_at": w.created_at.isoformat() if w.created_at else None
    } for w in workflows]
    
    return success_response(data={"workflows": workflow_list})


@router.post("/", summary="创建工作流", status_code=status.HTTP_201_CREATED)
async def create_workflow(
    workflow: WorkflowCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """管理员创建新工作流"""
    db_workflow = Workflow(**workflow.dict())
    db.add(db_workflow)
    db.commit()
    db.refresh(db_workflow)
    
    return success_response(
        data={
            "id": db_workflow.id,
            "name": db_workflow.name,
            "category": db_workflow.category
        },
        message="工作流创建成功",
        code=201
    )


@router.put("/{workflow_id}", summary="更新工作流")
async def update_workflow(
    workflow_id: int,
    workflow: WorkflowUpdate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """管理员更新工作流"""
    db_workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not db_workflow:
        raise NotFoundException("工作流不存在")
    
    for key, value in workflow.dict(exclude_unset=True).items():
        setattr(db_workflow, key, value)
    
    db.commit()
    db.refresh(db_workflow)
    
    return success_response(
        data={
            "id": db_workflow.id,
            "name": db_workflow.name
        },
        message="工作流更新成功"
    )


@router.delete("/{workflow_id}", summary="删除工作流")
async def delete_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """管理员删除工作流（软删除）"""
    db_workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not db_workflow:
        raise NotFoundException("工作流不存在")
    
    # 软删除工作流
    db_workflow.is_active = False
    
    # 清理用户权限关联
    db.query(UserWorkflow).filter(UserWorkflow.workflow_id == workflow_id).delete()
    
    # 清理公司权限关联
    db.query(CompanyWorkflow).filter(CompanyWorkflow.workflow_id == workflow_id).delete()
    
    db.commit()
    
    return success_response(message="工作流删除成功")
