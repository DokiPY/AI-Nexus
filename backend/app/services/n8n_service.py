import httpx
from typing import Dict, Any
import html

class N8NService:
    @staticmethod
    async def call_workflow(webhook_url: str, user_message: str, user_info: Dict[str, Any]) -> str:
        """调用N8N工作流"""
        try:
            payload = {
                "message": user_message,
                "user": {
                    "id": str(user_info["id"]),
                    "username": user_info["username"],
                    "email": user_info["email"],
                    "company_id": user_info["company_id"]
                }
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    webhook_url,
                    json=payload,
                    timeout=120.0  # AI模型响应较慢，设置为120秒
                )
                
                if response.status_code == 200:
                    response_text = response.text
                    # 解码HTML实体（&quot; &amp; &#39; 等）
                    response_text = html.unescape(response_text)
                    try:
                        import json
                        result = json.loads(response_text)
                        # N8N返回格式：[{"output": "AI回复内容"}]
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
                else:
                    return f"N8N工作流调用失败，状态码：{response.status_code}"
                    
        except httpx.TimeoutException:
            return "N8N工作流调用超时，请稍后重试"
        except Exception as e:
            return f"N8N工作流调用异常：{str(e)}"