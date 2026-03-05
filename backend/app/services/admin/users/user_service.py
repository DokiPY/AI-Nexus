"""用户管理服务层"""

from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID

from app.models.user import User
from app.models.company import Company
from app.models.workflow import Workflow, UserWorkflow
from app.schemas.user import UserCreate, UserUpdate
from app.core.auth.security import get_password_hash
from app.core.errors.exceptions import (
    NotFoundException,
    ConflictException,
    BadRequestException
)


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
        """获取用户列表（分页 + 筛选）"""
        query = db.query(User)

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

        # 公司名称映射
        companies = {c.id: c.name for c in db.query(Company).all()}

        # 活跃工作流信息
        all_workflows = {
            w.id: {"name": w.name, "icon": w.icon}
            for w in db.query(Workflow).filter(Workflow.is_active == True).all()
        }

        # 用户工作流权限（只统计活跃工作流）
        user_workflows = {}
        for uw in db.query(UserWorkflow).join(Workflow).filter(Workflow.is_active == True).all():
            if uw.user_id not in user_workflows:
                user_workflows[uw.user_id] = []
            user_workflows[uw.user_id].append(uw.workflow_id)

        result_users = []
        for user in users:
            wf_ids = user_workflows.get(user.id, [])
            result_users.append({
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "company_name": companies.get(user.company_id, "未知"),
                "company_id": user.company_id,
                "is_active": user.is_active,
                "workflow_count": len(wf_ids),
                "created_at": user.created_at.isoformat() if user.created_at else None,
                "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None,
                "workflows": [
                    {"id": wid, "name": all_workflows[wid]["name"], "icon": all_workflows[wid]["icon"]}
                    for wid in wf_ids if wid in all_workflows
                ]
            })

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

        Raises:
            ConflictException: 用户名或邮箱已存在
            NotFoundException: 公司不存在
        """
        if db.query(User).filter(User.username == user_data.username).first():
            raise ConflictException("用户名已存在")

        if user_data.email and db.query(User).filter(User.email == user_data.email).first():
            raise ConflictException("邮箱已存在")

        company = db.query(Company).filter(Company.name == user_data.company_name).first()
        if not company:
            raise NotFoundException(f"公司 '{user_data.company_name}' 不存在")

        db_user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            company_id=company.id,
            role=user_data.role,
            is_active=user_data.is_active
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> dict:
        """
        根据ID获取用户详情

        Raises:
            NotFoundException: 用户不存在
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("用户不存在")

        company = db.query(Company).filter(Company.id == user.company_id).first()
        return {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "company_id": user.company_id,
            "company_name": company.name if company else "未知",
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None,
            "last_login_at": user.last_login_at.isoformat() if user.last_login_at else None
        }

    @staticmethod
    def update_user(db: Session, user_id: UUID, user_data: UserUpdate) -> dict:
        """
        更新用户信息

        Raises:
            NotFoundException: 用户不存在 / 公司不存在
            ConflictException: 邮箱已被使用
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("用户不存在")

        update_dict = user_data.model_dump(exclude_unset=True)

        # 邮箱冲突检查
        if 'email' in update_dict and update_dict['email']:
            existing = db.query(User).filter(
                User.email == update_dict['email'],
                User.id != user_id
            ).first()
            if existing:
                raise ConflictException("邮箱已被使用")

        # 公司名称 → 公司ID
        if 'company_name' in update_dict:
            company = db.query(Company).filter(Company.name == update_dict.pop('company_name')).first()
            if not company:
                raise NotFoundException("公司不存在")
            user.company_id = company.id

        # 更新允许的字段
        allowed_fields = ['username', 'email', 'role', 'is_active']
        for field, value in update_dict.items():
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
            "company_id": user.company_id,
            "company_name": company.name if company else "未知",
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }

    @staticmethod
    def delete_user(db: Session, user_id: UUID) -> None:
        """
        删除用户

        Raises:
            NotFoundException: 用户不存在
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("用户不存在")

        db.query(UserWorkflow).filter(UserWorkflow.user_id == user_id).delete()
        db.delete(user)
        db.commit()

    @staticmethod
    def reset_password(db: Session, user_id: UUID, new_password: str) -> None:
        """
        重置用户密码

        Raises:
            BadRequestException: 密码为空
            NotFoundException: 用户不存在
        """
        if not new_password:
            raise BadRequestException("新密码不能为空")

        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("用户不存在")

        user.password_hash = get_password_hash(new_password)
        db.commit()

    @staticmethod
    def get_user_workflows(db: Session, user_id: UUID) -> dict:
        """
        获取用户的工作流权限

        Raises:
            NotFoundException: 用户不存在
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("用户不存在")

        workflow_ids = [
            uw.workflow_id for uw in
            db.query(UserWorkflow).filter(UserWorkflow.user_id == user_id).all()
        ]
        return {"workflow_ids": workflow_ids}

    @staticmethod
    def update_user_workflows(db: Session, user_id: UUID, workflow_ids: List[int]) -> dict:
        """
        更新用户的工作流权限

        Raises:
            NotFoundException: 用户或工作流不存在
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise NotFoundException("用户不存在")

        db.query(UserWorkflow).filter(UserWorkflow.user_id == user_id).delete()

        for workflow_id in workflow_ids:
            workflow = db.query(Workflow).filter(Workflow.id == workflow_id).first()
            if not workflow:
                raise BadRequestException(f"工作流 {workflow_id} 不存在")
            db.add(UserWorkflow(user_id=user_id, workflow_id=workflow_id))

        db.commit()
        return {"workflow_ids": workflow_ids}
