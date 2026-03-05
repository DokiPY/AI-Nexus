"""应用中间件"""

import uuid
import time
import logging
from starlette.types import ASGIApp, Receive, Scope, Send

from app.core.log import request_id_ctx

logger = logging.getLogger(__name__)


class RequestIDMiddleware:
    """
    Request ID 追踪中间件（纯 ASGI 实现）
    
    使用纯 ASGI 而非 BaseHTTPMiddleware，避免缓冲 StreamingResponse。
    
    功能：
    1. 为每个请求生成或接收唯一的 request_id
    2. 将 request_id 存储在 contextvars 中
    3. 在响应头中返回 request_id 和处理时间
    4. 记录请求日志
    """

    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        # 从请求头获取或生成 request_id
        headers = dict(scope.get("headers", []))
        request_id = (
            headers.get(b"x-request-id", b"").decode() or str(uuid.uuid4())
        )

        # 设置到 contextvars
        token = request_id_ctx.set(request_id)

        method = scope.get("method", "")
        path = scope.get("path", "")
        start_time = time.time()

        logger.info(f"{method} {path}", extra={"request_id": request_id})

        async def send_wrapper(message):
            if message["type"] == "http.response.start":
                # 注入响应头
                process_time = time.time() - start_time
                headers = list(message.get("headers", []))
                headers.append((b"x-request-id", request_id.encode()))
                headers.append((b"x-process-time", f"{process_time:.3f}s".encode()))
                message["headers"] = headers
            elif message["type"] == "http.response.body":
                # 在最后一个 body chunk 时记录完成日志
                if not message.get("more_body", False):
                    process_time = time.time() - start_time
                    status = getattr(send_wrapper, "_status", 0)
                    logger.info(
                        f"Completed {method} {path} - "
                        f"Status: {status} - Time: {process_time:.3f}s",
                        extra={"request_id": request_id}
                    )
            # 记录状态码
            if message["type"] == "http.response.start":
                send_wrapper._status = message.get("status", 0)
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            request_id_ctx.reset(token)
