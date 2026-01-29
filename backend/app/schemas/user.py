from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    company_id: int
    role: str = "user"
    is_active: bool = True

class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None
    company_name: str  # 使用公司名称而不是ID
    role: str = "user"
    is_active: bool = True
    password: str

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