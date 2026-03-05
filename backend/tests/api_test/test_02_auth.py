"""认证接口测试"""

import pytest
from tests.api_test.test_config import ADMIN_USERNAME, ADMIN_PASSWORD


class TestAuthentication:
    """认证功能测试"""
    
    def test_login_success(self, api_client):
        """测试登录成功"""
        response = api_client.post(
            "/api/v1/auth/login",
            json={"username": ADMIN_USERNAME, "password": ADMIN_PASSWORD}
        )
        
        assert response.status_code == 200, "登录成功应返回 200"
        
        data = response.json()
        assert data["success"] is True, "success 应为 true"
        assert data["code"] == 200, "code 应为 200"
        assert data["message"] == "登录成功", "message 应为'登录成功'"
        assert "data" in data, "响应应包含 data 字段"
        assert "id" in data["data"], "data 应包含用户 id"
        assert "username" in data["data"], "data 应包含 username"
        assert data["data"]["username"] == ADMIN_USERNAME, f"用户名应为 {ADMIN_USERNAME}"
        assert "request_id" in data, "响应应包含 request_id"
        
        # 检查响应头
        assert "X-Request-ID" in response.headers, "响应头应包含 X-Request-ID"
        assert "X-Process-Time" in response.headers, "响应头应包含 X-Process-Time"
    
    def test_login_wrong_password(self, api_client):
        """测试错误密码"""
        response = api_client.post(
            "/api/v1/auth/login",
            json={"username": ADMIN_USERNAME, "password": "wrongpassword"}
        )
        
        assert response.status_code == 401, "错误密码应返回 401"
        
        data = response.json()
        assert data["success"] is False, "success 应为 false"
        assert data["code"] == 401, "code 应为 401"
        assert "账号或密码错误" in data["message"], "错误信息应包含'账号或密码错误'"
        assert data["data"] is None, "data 应为 null"
        assert "request_id" in data, "错误响应也应包含 request_id"
    
    def test_login_user_not_found(self, api_client):
        """测试用户不存在"""
        response = api_client.post(
            "/api/v1/auth/login",
            json={"username": "nonexistent_user", "password": ADMIN_PASSWORD}
        )
        
        assert response.status_code == 401, "用户不存在应返回 401"
        
        data = response.json()
        assert data["success"] is False, "success 应为 false"
        assert data["code"] == 401, "code 应为 401"
    
    def test_login_missing_fields(self, api_client):
        """测试缺少必填字段"""
        response = api_client.post(
            "/api/v1/auth/login",
            json={"username": ADMIN_USERNAME}  # 缺少 password
        )
        
        assert response.status_code == 422, "缺少字段应返回 422"
        
        data = response.json()
        assert data["success"] is False, "success 应为 false"
        assert data["code"] == 422, "code 应为 422"
        assert "参数验证失败" in data["message"], "错误信息应包含'参数验证失败'"
    
    def test_get_current_user(self, authenticated_client):
        """测试获取当前用户信息"""
        response = authenticated_client.get("/api/v1/auth/me")
        
        assert response.status_code == 200, "获取用户信息应返回 200"
        
        data = response.json()
        assert data["success"] is True, "success 应为 true"
        assert data["code"] == 200, "code 应为 200"
        assert "data" in data, "响应应包含 data"
        assert "id" in data["data"], "data 应包含 id"
        assert "username" in data["data"], "data 应包含 username"
        assert "email" in data["data"], "data 应包含 email"
        assert "role" in data["data"], "data 应包含 role"
        assert "company" in data["data"], "data 应包含 company"
    
    def test_get_current_user_unauthorized(self, api_client):
        """测试未登录获取用户信息"""
        # 创建新的客户端（未登录）
        new_client = api_client.__class__()
        response = new_client.get("/api/v1/auth/me")
        
        assert response.status_code == 401, "未登录应返回 401"
        
        data = response.json()
        assert data["success"] is False, "success 应为 false"
        assert data["code"] == 401, "code 应为 401"
    
    def test_logout(self, authenticated_client):
        """测试登出"""
        response = authenticated_client.post("/api/v1/auth/logout")
        
        assert response.status_code == 200, "登出应返回 200"
        
        data = response.json()
        assert data["success"] is True, "success 应为 true"
        assert data["code"] == 200, "code 应为 200"
        assert "登出成功" in data["message"], "message 应包含'登出成功'"
