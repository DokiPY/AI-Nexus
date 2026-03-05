"""统一异常处理"""

from fastapi import HTTPException, status


class BusinessException(HTTPException):
    """业务异常基类"""
    
    def __init__(self, message: str, code: int = 400):
        super().__init__(status_code=code, detail=message)


class NotFoundException(BusinessException):
    """资源不存在异常 - 404"""
    
    def __init__(self, message: str = "资源不存在"):
        super().__init__(message=message, code=status.HTTP_404_NOT_FOUND)


class PermissionDeniedException(BusinessException):
    """权限不足异常 - 403"""
    
    def __init__(self, message: str = "权限不足"):
        super().__init__(message=message, code=status.HTTP_403_FORBIDDEN)


class ConflictException(BusinessException):
    """资源冲突异常 - 409"""
    
    def __init__(self, message: str = "资源已存在"):
        super().__init__(message=message, code=status.HTTP_409_CONFLICT)


class UnauthorizedException(BusinessException):
    """未认证异常 - 401"""
    
    def __init__(self, message: str = "未认证或认证已过期"):
        super().__init__(message=message, code=status.HTTP_401_UNAUTHORIZED)


class BadRequestException(BusinessException):
    """请求参数错误异常 - 400"""
    
    def __init__(self, message: str = "请求参数错误"):
        super().__init__(message=message, code=status.HTTP_400_BAD_REQUEST)


class BadGatewayException(BusinessException):
    """上游服务错误异常 - 502"""
    
    def __init__(self, message: str = "上游服务错误"):
        super().__init__(message=message, code=status.HTTP_502_BAD_GATEWAY)
