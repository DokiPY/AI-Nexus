"""JWT 令牌管理模块

提供 JWT 令牌的创建和验证功能。
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from app.core.config.settings import settings

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """创建 JWT 访问令牌
    
    Args:
        data: 要编码到令牌中的数据（通常包含用户标识）
        expires_delta: 令牌过期时间增量，如果为 None 则使用配置的默认值
        
    Returns:
        str: 编码后的 JWT 令牌
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """验证 JWT 令牌并提取用户名
    
    Args:
        token: JWT 令牌字符串
        
    Returns:
        Optional[str]: 如果令牌有效返回用户名，否则返回 None
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: Optional[str] = payload.get("sub")
        return username
    except JWTError:
        return None