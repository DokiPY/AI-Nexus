"""FastAPI 应用入口"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config.settings import settings
from app.core.log.middleware import RequestIDMiddleware
from app.core.log.logging_config import setup_logging
from app.core.errors.handlers import register_exception_handlers
from app.api.api_router import api_router
from app.api.health import router as health_router

# 配置日志
setup_logging(
    log_level="INFO" if not settings.DEBUG else "DEBUG",
    log_to_file=settings.ENV == "production",  # 生产环境写文件
    log_to_stdout=True  # 始终输出到标准输出（容器友好）
)

# 创建 FastAPI 应用
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG
)

# 添加中间件
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS_LIST,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Request-ID", "X-Process-Time"],
    max_age=3600,
)

# 注册异常处理器
register_exception_handlers(app)

# 注册路由
app.include_router(health_router)  # 健康检查路由
app.include_router(api_router, prefix="/api/v1")  # 业务 API 路由


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

