"""N8N 工作流调用服务"""

import httpx
import json
import html
import logging
from typing import Dict, Any, AsyncGenerator

logger = logging.getLogger(__name__)


class N8NService:
    @staticmethod
    async def call_workflow(webhook_url: str, user_message: str, user_info: Dict[str, Any]) -> str:
        """调用N8N工作流（非流式，兼容旧接口）"""
        try:
            payload = N8NService._build_payload(user_message, user_info)
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    webhook_url,
                    json=payload,
                    timeout=120.0
                )
                
                if response.status_code == 200:
                    return N8NService._parse_response(response.text)
                else:
                    return f"N8N工作流调用失败，状态码：{response.status_code}"
                    
        except httpx.TimeoutException:
            return "N8N工作流调用超时，请稍后重试"
        except Exception as e:
            return f"N8N工作流调用异常：{str(e)}"

    @staticmethod
    async def call_workflow_stream(
        webhook_url: str, user_message: str, user_info: Dict[str, Any]
    ) -> AsyncGenerator[str, None]:
        """调用N8N工作流（流式），逐块 yield 文本内容"""
        payload = N8NService._build_payload(user_message, user_info)
        decoder = json.JSONDecoder()

        try:
            # 禁用 Accept-Encoding 压缩，防止 httpx 缓冲整个响应来解压
            headers = {"Accept-Encoding": "identity"}
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    "POST",
                    webhook_url,
                    json=payload,
                    headers=headers,
                    timeout=120.0
                ) as response:
                    if response.status_code != 200:
                        yield f"N8N工作流调用失败，状态码：{response.status_code}"
                        return

                    buffer = ""
                    # 使用 aiter_bytes 避免 aiter_text 的内部缓冲
                    async for raw_chunk in response.aiter_bytes():
                        buffer += raw_chunk.decode("utf-8", errors="replace")
                        # N8N 流式返回的是多个 JSON 对象拼接，逐个解析
                        while buffer:
                            buffer = buffer.lstrip()
                            if not buffer:
                                break
                            try:
                                obj, end_idx = decoder.raw_decode(buffer)
                                buffer = buffer[end_idx:]

                                # N8N 流式返回的是 {"type":"item","content":"..."} 格式
                                # 非流式 Respond to Webhook 可能返回 list 或 dict
                                if isinstance(obj, list):
                                    # 非流式返回了数组，提取 output
                                    for item in obj:
                                        if isinstance(item, dict):
                                            output = item.get("output", "")
                                            if output:
                                                yield output
                                elif isinstance(obj, dict):
                                    if obj.get("type") == "item":
                                        content = obj.get("content", "")
                                        if content:
                                            yield content
                                    elif "output" in obj:
                                        yield obj["output"]
                            except json.JSONDecodeError:
                                # 不完整的 JSON，等待更多数据
                                break

        except httpx.TimeoutException:
            yield "N8N工作流调用超时，请稍后重试"
        except Exception as e:
            logger.error(f"N8N流式调用异常: {str(e)}")
            yield f"N8N工作流调用异常：{str(e)}"

    @staticmethod
    def _build_payload(user_message: str, user_info: Dict[str, Any]) -> dict:
        """构建N8N请求体"""
        return {
            "message": user_message,
            "user": {
                "id": str(user_info["id"]),
                "username": user_info["username"],
                "email": user_info["email"],
                "company_id": user_info["company_id"]
            }
        }

    @staticmethod
    def _parse_response(response_text: str) -> str:
        """解析N8N非流式响应"""
        response_text = html.unescape(response_text)
        try:
            result = json.loads(response_text)
            if isinstance(result, list) and len(result) > 0:
                output = result[0].get("output")
                if output:
                    return output
                return "N8N工作流执行成功，但未返回内容"
            elif isinstance(result, dict) and "output" in result:
                return result["output"]
            return f"N8N工作流返回格式异常: {type(result).__name__}"
        except Exception as json_error:
            return f"N8N返回内容解析失败: {str(json_error)}\n原始返回: {response_text[:200]}"
