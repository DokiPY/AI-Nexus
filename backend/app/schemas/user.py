from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    company_id: int
    role: str = "user"
    is_active: bool = True

class UserCreate(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    company_name: str  # 使用公司名称而不是ID
    role: str = "user"
    is_active: bool = True
    password: str
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """验证邮箱格式"""
        if v is not None and v.strip() == '':
            raise ValueError('邮箱不能为空字符串')
        return v

class UserUpdate(BaseModel):
    """用户更新请求"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    company_name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class ResetPassword(BaseModel):
    """重置密码请求"""
    new_password: str

class UpdateWorkflows(BaseModel):
    """更新用户工作流权限请求"""
    workflow_ids: list[int] = []

class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    
    class Config:
        from_attributes = True

class CompanyResponse(BaseModel):
    id: int
    name: str
    domain: Optional[str]
    is_active: bool
    
    class Config:
        from_attributes = True