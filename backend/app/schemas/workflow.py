from pydantic import BaseModel, HttpUrl
from typing import Optional

class WorkflowResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    icon: Optional[str]
    n8n_webhook_url: str
    is_active: bool
    
    class Config:
        from_attributes = True

class WorkflowCreate(BaseModel):
    name: str
    description: Optional[str] = None
    n8n_webhook_url: str
    icon: Optional[str] = None
    category: str = "办公助手"
    http_method: str = "POST"
    stream_enabled: bool = True

class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    n8n_webhook_url: Optional[str] = None
    icon: Optional[str] = None
    category: Optional[str] = None
    http_method: Optional[str] = None
    stream_enabled: Optional[bool] = None