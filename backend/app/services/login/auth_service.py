# 登录认证服务层

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta, datetime

from app.models.user import User
from app.models.company import Company
from app.core.security import verify_password
from app.core.jwt import create_access_token
from app.core.config import settings


class AuthService:
    """登录认证服务"""
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
        """
        验证用户身份
        
        Args:
            db: 数据库会话
            username: 用户名
            password: 密码
            
        Returns:
            验证成功的用户对象
            
        Raises:
            HTTPException: 用户不存在、密码错误或账号未激活
        """
        # 查找用户(不限制is_active)
        user = db.query(User).filter(User.username == username).first()
        
        # 用户不存在
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="账号或密码错误"
            )
        
        # 密码错误
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="账号或密码错误"
            )
        
        # 账号被禁用
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="账号已被禁用，请联系管理员"
            )
        
        return user
    
    @staticmethod
    def create_token(username: str) -> str:
        """
        创建访问令牌
        
        Args:
            username: 用户名
            
        Returns:
            JWT访问令牌
        """
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username},
            expires_delta=access_token_expires
        )
        return access_token
    
    @staticmethod
    def update_last_login(db: Session, user: User) -> None:
        """
        更新用户最后登录时间
        
        Args:
            db: 数据库会话
            user: 用户对象
        """
        user.last_login_at = datetime.utcnow()
        db.commit()
    
    @staticmethod
    def get_user_info_with_company(db: Session, user: User) -> dict:
        """
        获取用户信息（包含公司信息）
        
        Args:
            db: 数据库会话
            user: 用户对象
            
        Returns:
            包含用户和公司信息的字典
        """
        company = db.query(Company).filter(Company.id == user.company_id).first()
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "company": {
                "id": company.id if company else None,
                "name": company.name if company else "未知"
            }
        }
    
    @staticmethod
    def login(db: Session, username: str, password: str) -> dict:
        """
        用户登录（完整流程）
        
        Args:
            db: 数据库会话
            username: 用户名
            password: 密码
            
        Returns:
            包含访问令牌和用户信息的字典
            
        Raises:
            HTTPException: 认证失败
        """
        # 验证用户
        user = AuthService.authenticate_user(db, username, password)
        
        # 创建token
        access_token = AuthService.create_token(user.username)
        
        # 更新最后登录时间
        AuthService.update_last_login(db, user)
        
        # 获取用户信息
        user_info = AuthService.get_user_info_with_company(db, user)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_info": user_info
        }