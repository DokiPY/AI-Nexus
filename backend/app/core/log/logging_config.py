"""日志配置"""

import logging
import logging.handlers
import os
from pathlib import Path

from app.core.log import request_id_ctx


class RequestIDFilter(logging.Filter):
    """
    日志过滤器，确保所有日志都有 request_id 字段
    优先从 contextvars 获取 request_id，保证 httpx 等第三方库日志也能携带
    """
    
    def filter(self, record):
        if not hasattr(record, 'request_id') or record.request_id == 'N/A':
            record.request_id = request_id_ctx.get()
        return True


def setup_logging(log_level: str = "INFO", log_to_file: bool = False, log_to_stdout: bool = True):
    """
    配置应用日志
    
    Args:
        log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: 是否输出到文件（开发环境/传统部署）
        log_to_stdout: 是否输出到标准输出（容器化部署推荐）
    """
    # 创建日志目录
    if log_to_file:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
    
    # 配置根日志记录器
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # 清除现有的处理器和过滤器
    logger.handlers.clear()
    logger.filters.clear()
    
    # 添加 RequestIDFilter 到根日志记录器
    logger.addFilter(RequestIDFilter())
    
    # 日志格式
    log_format = '%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s'
    formatter = logging.Formatter(log_format)
    
    # 标准输出处理器（容器化部署推荐）
    if log_to_stdout:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.addFilter(RequestIDFilter())
        logger.addHandler(console_handler)
    
    # 文件处理器（可选，用于传统部署或开发环境）
    if log_to_file:
        file_handler = logging.handlers.RotatingFileHandler(
            'logs/app.log',
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=10,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        file_handler.addFilter(RequestIDFilter())
        logger.addHandler(file_handler)
        
        # 错误日志单独文件
        error_handler = logging.handlers.RotatingFileHandler(
            'logs/error.log',
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=10,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        error_handler.addFilter(RequestIDFilter())
        logger.addHandler(error_handler)
    
    # 设置第三方库的日志级别（避免过多日志）
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    logging.getLogger("passlib").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.INFO)
    
    logger.info(f"Logging configured - Level: {log_level}, File: {log_to_file}, Stdout: {log_to_stdout}")
