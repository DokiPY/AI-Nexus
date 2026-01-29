# WorkflowPermissionDialog 对应的服务层

from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List
from uuid import UUID

from app.models.user import User
from app.models.workflow import Workflow, UserWorkflow


class WorkflowPermissionDialogService:
    """WorkflowPermissionDialog 服务 - 对应前端 WorkflowPermissionDialog.vue"""
    
    @staticmethod
    def get_user_workflows(db: Session, user_id: UUID) -> dict:
        """获取用户的工作流权限"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 获取用户已分配的工作流ID
        user_workflow_ids = [
            uw.workflow_id for uw in db.query(UserWorkflow).filter(
                UserWorkflow.user_id == user_id
            ).all()
        ]
        
        return {"workflow_ids": user_workflow_ids}
    
    @staticmethod
    def update_user_workflows(db: Session, user_id: UUID, workflow_ids: List[int]) -> dict:
        """更新用户的工作流权限"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 清除用户现有权限
        db.query(UserWorkflow).filter(UserWorkflow.user_id == user_id).delete()
        
        # 添加新权限
        for workflow_id in workflow_ids:
            workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
            if not workflow:
                raise HTTPException(status_code=400, detail=f"工作流 {workflow_id} 不存在")
            
            user_workflow = UserWorkflow(user_id=user_id, workflow_id=workflow_id)
            db.add(user_workflow)
        
        db.commit()
        
        return {
            "message": "更新成功",
            "workflow_ids": workflow_ids
        }
