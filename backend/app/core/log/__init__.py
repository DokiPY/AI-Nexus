"""日志模块

提供 request_id 上下文变量，用于在整个异步调用链中传递请求追踪ID。
"""

from contextvars import ContextVar

# 全局 request_id 上下文变量，异步安全
request_id_ctx: ContextVar[str] = ContextVar("request_id", default="N/A")
