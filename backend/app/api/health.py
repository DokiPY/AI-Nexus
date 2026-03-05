"""健康检查和系统信息接口"""

from fastapi import APIRouter

from app.core.config.settings import settings

router = APIRouter(tags=["健康检查"])


@router.get("/")
async def root():
    """
    根路径健康检查
    
    返回系统基本信息和运行状态
    """
    return {
        "message": f"{settings.PROJECT_NAME} API v{settings.VERSION}",
        "status": "running",
        "environment": settings.ENV
    }


@router.get("/health")
async def health_check():
    """
    健康检查接口
    
    用于负载均衡器、容器编排系统等检查服务状态
    """
    return {
        "status": "healthy",
        "version": settings.VERSION
    }
