from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


class AppException(Exception):
    """应用基础异常"""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class NotFoundException(AppException):
    """资源不存在异常"""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)


class ValidationException(AppException):
    """验证异常"""

    def __init__(self, message: str = "Validation error"):
        super().__init__(message, 422)


class UnauthorizedException(AppException):
    """未授权异常"""

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401)


async def custom_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    if isinstance(exc, AppException):
        logger.warning(f"AppException: {exc.message} - Path: {request.url.path}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message, "path": str(request.url.path)},
        )

    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "path": str(request.url.path)},
    )
