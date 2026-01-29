from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.connection import get_db
from app.api.deps import get_current_active_user, get_current_admin_user
from app.models.user import User
from app.models.workflow import Workflow, CompanyWorkflow, UserWorkflow
from app.schemas.workflow import WorkflowResponse, WorkflowCreate, WorkflowUpdate

router = APIRouter()

@router.get("/", summary="获取用户可用的工作流列表")
async def get_user_workflows(
    category: str = None,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取工作流列表"""
    
    # 获取用户被授权的工作流ID
    user_workflow_ids = set(
        row[0] for row in db.query(UserWorkflow.workflow_id).filter(
            UserWorkflow.user_id == current_user.id
        ).all()
    )
    
    # 管理员看到所有工作流，普通用户只看到自己被授权的
    if current_user.role == "admin":
        query = db.query(Workflow).filter(Workflow.is_active == True)
    else:
        if not user_workflow_ids:
            return {"total_workflows": 0, "available_count": 0, "workflows": []}
        query = db.query(Workflow).filter(
            Workflow.id.in_(user_workflow_ids),
            Workflow.is_active == True
        )
    
    # 分类筛选
    if category and category != "全部":
        query = query.filter(Workflow.category == category)
    
    workflows = query.all()
    
    # 组装返回数据
    result = []
    for workflow in workflows:
        has_permission = current_user.role == "admin" or workflow.id in user_workflow_ids
        result.append({
            "id": workflow.id,
            "name": workflow.name,
            "description": workflow.description,
            "icon": workflow.icon,
            "category": workflow.category,
            "n8n_webhook_url": workflow.n8n_webhook_url,
            "is_active": workflow.is_active,
            "has_permission": has_permission,
            "status": "available",
            "created_at": workflow.created_at.isoformat() if workflow.created_at else None
        })
    
    return {
        "total_workflows": len(result),
        "available_count": len(result),
        "workflows": result
    }

@router.get("/categories", summary="获取用户可见的工作流分类")
async def get_user_workflow_categories(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """获取工作流分类列表"""
    
    # 管理员看所有分类，普通用户看自己有权限的分类
    if current_user.role == "admin":
        categories = db.query(Workflow.category).filter(
            Workflow.is_active == True
        ).distinct().all()
    else:
        user_workflow_ids = [
            row[0] for row in db.query(UserWorkflow.workflow_id).filter(
                UserWorkflow.user_id == current_user.id
            ).all()
        ]
        if not user_workflow_ids:
            return {"categories": ["全部"]}
        
        categories = db.query(Workflow.category).filter(
            Workflow.id.in_(user_workflow_ids),
            Workflow.is_active == True
        ).distinct().all()
    
    category_list = ["全部"] + [cat[0] for cat in categories if cat[0]]
    
    return {"categories": category_list}

