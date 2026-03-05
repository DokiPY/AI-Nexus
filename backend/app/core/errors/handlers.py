"""全局异常处理器"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config.settings import settings
from app.schemas.response import error_response


async def http_exception_handler(request: Request, exc: HTTPException):
    """
    统一处理 HTTPException
    
    捕获所有 HTTPException 及其子类（包括自定义异常）
    返回统一的错误响应格式
    """
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response(
            message=exc.detail,
            code=exc.status_code,
            request_id=request_id
        )
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    统一处理参数验证错误
    
    捕获 Pydantic 参数验证失败的异常
    返回详细的验证错误信息
    """
    request_id = getattr(request.state, "request_id", None)
    
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"][1:]),
            "message": error["msg"]
        })
    
    return JSONResponse(
        status_code=422,
        content=error_response(
            message="参数验证失败",
            code=422,
            data={"errors": errors},
            request_id=request_id
        )
    )


async def global_exception_handler(request: Request, exc: Exception):
    """
    统一处理未捕获异常
    
    捕获所有未被其他处理器捕获的异常
    开发环境打印详细错误，生产环境返回通用错误信息
    """
    request_id = getattr(request.state, "request_id", None)
    
    # 开发环境打印详细错误
    if settings.DEBUG:
        import traceback
        print(f"未捕获异常: {exc}")
        traceback.print_exc()
    
    return JSONResponse(
        status_code=500,
        content=error_response(
            message="服务器内部错误",
            code=500,
            request_id=request_id
        )
    )


def register_exception_handlers(app):
    """
    注册所有异常处理器到 FastAPI 应用
    
    Args:
        app: FastAPI 应用实例
    """
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, global_exception_handler)
