"""登录认证API路由"""

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Cookie
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from typing import Optional

from app.database.connection import get_db
from app.schemas.auth import LoginRequest, Token
from app.schemas.response import success_response
from app.models.user import User
from app.core.config.settings import settings
from app.core.errors.exceptions import UnauthorizedException, PermissionDeniedException
from app.services.login.auth_service import AuthService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")


@router.post("/token", response_model=Token, summary="OAuth2 Token")
async def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """
    OAuth2标准token接口，用于API鉴权
    
    注意：此接口保持 OAuth2 标准格式，不使用统一响应格式
    """
    user = AuthService.authenticate_user(db, form_data.username, form_data.password)
    access_token = AuthService.create_token(user.username)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/login", summary="用户登录")
async def login(
    request: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):
    """前端用户登录接口 - 使用HttpOnly Cookie"""
    result = AuthService.login(db, request.username, request.password)
    
    # 设置HttpOnly Cookie
    response.set_cookie(
        key="access_token",
        value=result["access_token"],
        httponly=True,  # 防止XSS攻击
        secure=settings.ENV == "production",  # 生产环境强制HTTPS
        samesite="lax",  # 防止CSRF攻击
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # 秒
        path="/"
    )
    
    # 返回用户信息（直接返回user_info，不再嵌套）
    return success_response(
        data=result["user_info"],
        message="登录成功"
    )


async def get_current_user(
    db: Session = Depends(get_db),
    access_token: Optional[str] = Cookie(None)
) -> User:
    """
    获取当前登录用户 - 从Cookie读取token
    
    Args:
        db: 数据库会话
        access_token: 从Cookie中获取的JWT令牌
        
    Returns:
        当前用户对象
        
    Raises:
        UnauthorizedException: 令牌无效或用户不存在
        PermissionDeniedException: 账号被禁用
    """
    if not access_token:
        raise UnauthorizedException("登录已过期，请重新登录")
    
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise UnauthorizedException("登录已过期，请重新登录")
    except JWTError:
        raise UnauthorizedException("登录已过期，请重新登录")
    
    # 先查找用户(不限制is_active)
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise UnauthorizedException("登录已过期，请重新登录")
    
    # 检查用户是否被禁用
    if not user.is_active:
        raise PermissionDeniedException("账号已被禁用，请联系管理员")
    
    return user


@router.get("/me", summary="获取当前用户信息")
async def get_user_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前登录用户的详细信息"""
    user_info = AuthService.get_user_info_with_company(db, current_user)
    
    # 添加额外字段
    user_info["is_active"] = current_user.is_active
    user_info["created_at"] = current_user.created_at.isoformat() if current_user.created_at else None
    
    return success_response(data=user_info)


@router.post("/logout", summary="用户登出")
async def logout(response: Response):
    """清除Cookie实现登出"""
    response.delete_cookie(key="access_token", path="/")
    return success_response(message="登出成功")
