# 用户管理服务层

from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import List, Optional

from app.models.user import User
from app.models.company import Company
from app.models.workflow import Workflow, UserWorkflow
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


class UserService:
    """用户管理服务"""
    
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
        """获取用户列表并支持分页和筛选"""
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
        companies = {c.id: c.name for c in db.query(Company).all()}
        
        # 获取所有工作流信息
        all_workflows = {w.id: {"name": w.name, "icon": w.icon} for w in db.query(Workflow).all()}
        
        # 获取所有用户的工作流权限
        user_workflows = {}
        if include_workflows:
            for user_workflow in db.query(UserWorkflow).all():
                if user_workflow.user_id not in user_workflows:
                    user_workflows[user_workflow.user_id] = []
                user_workflows[user_workflow.user_id].append(user_workflow.workflow_id)
        
        result_users = []
        for user in users:
            user_data = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "is_active": user.is_active,
                "company_name": companies.get(user.company_id, "未知"),
                "company_id": user.company_id,
                "created_at": user.created_at,
                "last_login_at": user.last_login_at
            }
            
            if include_workflows:
                user_workflow_ids = user_workflows.get(user.id, [])
                user_data["workflows"] = [
                    {
                        "id": wid,
                        "name": all_workflows[wid]["name"],
                        "icon": all_workflows[wid]["icon"]
                    } for wid in user_workflow_ids if wid in all_workflows
                ]
                user_data["workflow_count"] = len(user_workflow_ids)
            
            result_users.append(user_data)
        
        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "users": result_users
        }
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """
        创建新用户
        
        Args:
            db: 数据库会话
            user_data: 用户创建数据（用户名、邮箱、密码、公司名称等）
            
        Returns:
            创建成功的用户对象
            
        Raises:
            HTTPException: 用户名或邮箱已存在，或公司不存在
        """
        # 检查用户名是否已存在
        existing_user = db.query(User).filter(User.username == user_data.username).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="用户名已存在")
        
        # 检查邮箱是否已存在
        if user_data.email:
            existing_email = db.query(User).filter(User.email == user_data.email).first()
            if existing_email:
                raise HTTPException(status_code=400, detail="邮箱已存在")
        
        # 根据公司名称查找公司ID
        company = db.query(Company).filter(Company.name == user_data.company_name).first()
        if not company:
            raise HTTPException(status_code=400, detail=f"公司 '{user_data.company_name}' 不存在")
        
        # 创建用户
        hashed_password = get_password_hash(user_data.password)
        db_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password,
            company_id=company.id,
            role=user_data.role,
            is_active=user_data.is_active
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        return db_user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id) -> dict:
        """根据ID获取用户详情"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        company = db.query(Company).filter(Company.id == user.company_id).first()
        return {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "company_id": user.company_id,
            "company_name": company.name if company else "未知",
            "created_at": user.created_at,
            "last_login_at": user.last_login_at
        }
    
    @staticmethod
    def update_user(db: Session, user_id, user_data: dict) -> dict:
        """更新用户信息"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        allowed_fields = ['email', 'role', 'is_active', 'username']
        for field, value in user_data.items():
            if field in allowed_fields and hasattr(user, field):
                setattr(user, field, value)
        
        db.commit()
        db.refresh(user)
        
        company = db.query(Company).filter(Company.id == user.company_id).first()
        return {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active,
            "company_id": user.company_id,
            "company_name": company.name if company else "未知",
            "created_at": user.created_at
        }
    
    @staticmethod
    def delete_user(db: Session, user_id) -> None:
        """删除用户"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 删除用户的工作流权限
        db.query(UserWorkflow).filter(UserWorkflow.user_id == user_id).delete()
        db.delete(user)
        db.commit()
    
    @staticmethod
    def batch_delete_users(db: Session, user_ids: List) -> None:
        """批量删除用户"""
        for user_id in user_ids:
            UserService.delete_user(db, user_id)
    
    @staticmethod
    def reset_password(db: Session, user_id, new_password: str) -> None:
        """重置用户密码"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        user.password_hash = get_password_hash(new_password)
        db.commit()
    
    @staticmethod
    def assign_workflows(db: Session, user_id, workflow_ids: List[int]) -> dict:
        """给用户分配工作流权限"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 清除用户现有权限
        db.query(UserWorkflow).filter(UserWorkflow.user_id == user.id).delete()
        
        # 添加新权限
        for workflow_id in workflow_ids:
            # 检查workflow是否存在
            workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
            if not workflow:
                raise HTTPException(status_code=400, detail=f"Workflow {workflow_id} 不存在")
            
            # 创建权限记录
            user_workflow = UserWorkflow(user_id=user.id, workflow_id=workflow_id)
            db.add(user_workflow)
        
        db.commit()
        return {"message": "更新成功", "workflow_ids": workflow_ids}
    
    @staticmethod
    def get_user_workflows(db: Session, user_id) -> dict:
        """获取用户的工作流权限"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 获取用户已分配的工作流ID
        user_workflow_ids = [uw.workflow_id for uw in db.query(UserWorkflow).filter(
            UserWorkflow.user_id == user_id
        ).all()]
        
        return {"workflow_ids": user_workflow_ids}