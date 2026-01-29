from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.api.deps import get_current_admin_user
from app.models.user import User
from app.models.workflow import Workflow
from app.schemas.workflow import WorkflowCreate, WorkflowUpdate

router = APIRouter()

@router.get("/", summary="获取所有工作流")
async def get_all_workflows(
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """管理员获取所有工作流列表"""
    workflows = db.query(Workflow).filter(Workflow.is_active == True).all()
    return [{
        "id": w.id,
        "name": w.name,
        "description": w.description,
        "icon": w.icon,
        "category": w.category,
        "n8n_webhook_url": w.n8n_webhook_url,
        "http_method": getattr(w, 'http_method', 'POST'),
        "created_at": w.created_at.isoformat() if w.created_at else None
    } for w in workflows]

@router.post("/", summary="创建工作流")
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
    return {"message": "工作流创建成功", "id": db_workflow.id}

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
        return {"error": "工作流不存在"}
    
    for key, value in workflow.dict(exclude_unset=True).items():
        setattr(db_workflow, key, value)
    
    db.commit()
    return {"message": "工作流更新成功"}

@router.delete("/{workflow_id}", summary="删除工作流")
async def delete_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):
    """管理员删除工作流（软删除）"""
    from app.models.workflow import UserWorkflow, CompanyWorkflow
    
    db_workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
    if not db_workflow:
        return {"error": "工作流不存在"}
    
    # 软删除工作流
    db_workflow.is_active = False
    
    # 清理用户权限关联
    db.query(UserWorkflow).filter(UserWorkflow.workflow_id == workflow_id).delete()
    
    # 清理公司权限关联
    db.query(CompanyWorkflow).filter(CompanyWorkflow.workflow_id == workflow_id).delete()
    
    db.commit()
    return {"message": "工作流删除成功"}
