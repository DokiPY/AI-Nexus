# UserFormDialog 对应的服务层

from sqlalchemy.orm import Session
from fastapi import HTTPException
from uuid import UUID

from app.models.user import User
from app.models.company import Company
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


class UserFormDialogService:
    """UserFormDialog 服务 - 对应前端 UserFormDialog.vue"""
    
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> dict:
        """创建新用户"""
        # 检查用户名是否已存在
        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(status_code=400, detail="用户名已存在")
        
        # 检查邮箱是否已存在
        if user_data.email and db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(status_code=400, detail="邮箱已存在")
        
        # 根据公司名称查找公司ID
        company = db.query(Company).filter(Company.name == user_data.company_name).first()
        if not company:
            raise HTTPException(status_code=400, detail=f"公司 '{user_data.company_name}' 不存在")
        
        # 创建用户
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
        
        return {
            "id": str(db_user.id),
            "username": db_user.username,
            "email": db_user.email,
            "role": db_user.role,
            "company_id": db_user.company_id,
            "company_name": company.name,
            "is_active": db_user.is_active,
            "created_at": db_user.created_at.isoformat() if db_user.created_at else None
        }
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: UUID) -> dict:
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
            "company_id": user.company_id,
            "company_name": company.name if company else "未知",
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
    
    @staticmethod
    def update_user(db: Session, user_id: UUID, user_data: dict) -> dict:
        """更新用户信息"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        # 处理公司名称
        if 'company_name' in user_data:
            company = db.query(Company).filter(Company.name == user_data['company_name']).first()
            if not company:
                raise HTTPException(status_code=400, detail=f"公司 '{user_data['company_name']}' 不存在")
            user.company_id = company.id
        
        # 更新其他允许的字段
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
            "company_id": user.company_id,
            "company_name": company.name if company else "未知",
            "is_active": user.is_active,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
    
    @staticmethod
    def reset_password(db: Session, user_id: UUID, new_password: str) -> dict:
        """重置用户密码"""
        if not new_password:
            raise HTTPException(status_code=400, detail="新密码不能为空")
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="用户不存在")
        
        user.password_hash = get_password_hash(new_password)
        db.commit()
        
        return {"message": "密码重置成功"}
