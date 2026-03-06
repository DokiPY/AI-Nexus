"""配置管理模块

使用 Pydantic Settings 管理应用配置，支持从 .env 文件和环境变量读取配置。
支持多环境：local, test, staging, production
"""

import os
from pydantic_settings import BaseSettings
from typing import List, Optional
from pathlib import Path

# 获取项目根目录（backend/）
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

# 获取环境变量，默认为 local
ENV = os.getenv('ENV', 'local')

class Settings(BaseSettings):
    """应用配置类"""
    
    # 环境标识
    ENV: str = ENV
    
    # 数据库配置
    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "123456"
    DB_NAME: str = "ai_agent_platform"
    
    @property
    def DATABASE_URL(self) -> str:
        """动态生成数据库连接 URL（安全处理密码中的特殊字符）"""
        from urllib.parse import quote_plus
        return f"postgresql://{quote_plus(self.DB_USER)}:{quote_plus(self.DB_PASSWORD)}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # JWT配置
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    
    # 应用配置
    PROJECT_NAME: str = "AI Agent Platform"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # CORS配置 - 支持多个前端域名（从环境变量读取，逗号分隔）
    ALLOWED_ORIGINS: str = "http://localhost:5173,https://localhost:5173,http://localhost:4173,http://127.0.0.1:5173"
    
    @property
    def ALLOWED_ORIGINS_LIST(self) -> List[str]:
        """将 CORS 字符串转换为列表"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(',')]
    
    # AWS配置（可选）
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    S3_UPLOAD_BUCKET_NAME: Optional[str] = None
    S3_SPLIT_BUCKET_NAME: Optional[str] = None
    
    # Redis配置（可选）
    REDIS_URL: Optional[str] = None
    
    class Config:
        """Pydantic 配置"""
        env_file = str(BASE_DIR / ".env")
        env_file_encoding = "utf-8"
        case_sensitive = True

# 环境 → .env 文件映射
_ENV_FILE_MAP = {
    "local": ".env",
    "test": ".env.test",
    "staging": ".env.staging",
    "production": ".env.production",
}

def get_settings() -> Settings:
    """根据 ENV 环境变量加载对应配置
    
    优先级：系统环境变量 > .env 文件 > 默认值
    容器部署时不需要 .env 文件，全部通过环境变量注入即可
    """
    env_filename = _ENV_FILE_MAP.get(ENV)
    if env_filename is None:
        raise ValueError(f"未知的环境配置: {ENV}，支持的环境: {', '.join(_ENV_FILE_MAP.keys())}")
    
    env_file_path = BASE_DIR / env_filename
    
    if env_file_path.is_file():
        print(f"🔥 当前环境: {ENV}, 加载配置: {env_filename}")
        return Settings(_env_file=str(env_file_path))
    else:
        # 容器环境下没有 .env 文件，完全依赖环境变量
        print(f"🔥 当前环境: {ENV}, 未找到 {env_filename}，使用环境变量")
        return Settings(_env_file=None)

# 创建配置实例
settings = get_settings()