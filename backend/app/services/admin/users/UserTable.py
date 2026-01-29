# UserTable 对应的服务层

from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional
from uuid import UUID

from app.models.user import User
from app.models.company import Company
from app.models.workflow import Workflow, UserWorkflow


class UserTableService:
    """UserTable 服务 - 对应前端 UserTable.vue"""
    
    @staticmethod
    def get_users(
        db: Session,
        page: int = 1,
        page_size: int = 10,
        search: Optional[str] = None,
        role: Optional[str] = None,
        company_id: Optional[int] = None,
        is_active: Optional[bool] = None
    ) -> dict:
        """获取用户列表"""
        query = db.query(User)
        
        # 筛选条件
        if search:
            query = query.filter(
                (User.username.ilike(f"%{search}%")) | 
                (User.email.ilike(f"%{search}%"))
            )
        if role:
            query = query.filter(User.role == role)
        if company_id:
            query = query.filter(User.company_id == company_id)
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        
        total = query.count()
        users = query.offset((page - 1) * page_size).limit(page_size).all()
        
        # 获取公司信息
        companies = {c.id: c.name for c in db.query(Company).all()}
        
        # 获取所有活跃的工作流信息（只统计未删除的）
        all_workflows = {w.id: {"name": w.name, "icon": w.icon} for w in db.query(Workflow).filter(Workflow.is_active == True).all()}
        
        # 获取用户的工作流权限（只统计活跃的工作流）
        user_workflows = {}
        for user_workflow in db.query(UserWorkflow).join(Workflow).filter(Workflow.is_active == True).all():
            if user_workflow.user_id not in user_workflows:
                user_workflows[user_workflow.user_id] = []
            user_workflows[user_workflow.user_id].append(user_workflow.workflow_id)
        
        # 组装返回数据 - 匹配前端 UserTable.vue 的 User 接口
        result_users = []
        for user in users:
            user_workflow_ids = user_workflows.get(user.id, [])
            result_users.append({
                "id": str(user.id),  # 前端需要字符串格式的ID
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "company_name": companies.get(user.company_id, "未知"),
                "company_id": user.company_id,
                "is_active": user.is_active,
                "workflow_count": len(user_workflow_ids),
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "workflows": [
                    {
                        "id": wid,
                        "name": all_workflows[wid]["name"],
                        "icon": all_workflows[wid]["icon"]
                    } for wid in user_workflow_ids if wid in all_workflows
                ]
            })
        
        return {
            "users": result_users,
            "total": total,
            "page": page,
            "page_size": page_size
        }
    
    @staticmethod
    def delete_user(db: Session, user_id: UUID) -> None:
        """删除用户"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 删除用户的工作流权限
        db.query(UserWorkflow).filter(UserWorkflow.user_id == user_id).delete()
        db.delete(user)
        db.commit()
