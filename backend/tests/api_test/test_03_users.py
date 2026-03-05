"""用户管理接口测试"""

import pytest
from tests.api_test.test_config import (
    USER_SEARCH_KEYWORD,
    INVALID_EMAIL,
    NON_EXISTENT_USER_ID,
    DEFAULT_PAGE,
    DEFAULT_PAGE_SIZE
)


class TestUserManagement:
    """用户管理测试"""
    
    def test_get_users_list(self, authenticated_client):
        """测试获取用户列表"""
        response = authenticated_client.get(
            f"/api/v1/admin/users?page={DEFAULT_PAGE}&page_size={DEFAULT_PAGE_SIZE}"
        )
        
        assert response.status_code == 200, "获取用户列表应返回 200"
        
        data = response.json()
        assert data["success"] is True, "success 应为 true"
        assert data["code"] == 200, "code 应为 200"
        assert "data" in data, "响应应包含 data"
        assert "total" in data["data"], "data 应包含 total"
        assert "page" in data["data"], "data 应包含 page"
        assert "page_size" in data["data"], "data 应包含 page_size"
        assert "users" in data["data"], "data 应包含 users 列表"
        assert isinstance(data["data"]["users"], list), "users 应为列表"
    
    def test_get_users_with_search(self, authenticated_client):
        """测试搜索用户"""
        response = authenticated_client.get(
            f"/api/v1/admin/users?search={USER_SEARCH_KEYWORD}"
        )
        
        assert response.status_code == 200, "搜索用户应返回 200"
        
        data = response.json()
        assert data["success"] is True, "success 应为 true"
    
    def test_create_user_success(self, authenticated_client, test_user_data):
        """测试创建用户成功"""
        # test_user_data 已经从配置文件生成，包含 company_name
        response = authenticated_client.post(
            "/api/v1/admin/users",
            json=test_user_data
        )
        
        assert response.status_code == 201, "创建用户应返回 201"
        
        data = response.json()
        assert data["success"] is True, "success 应为 true"
        assert data["code"] == 201, "code 应为 201"
        assert "用户创建成功" in data["message"], "message 应包含'用户创建成功'"
        assert "data" in data, "响应应包含 data"
        assert "id" in data["data"], "data 应包含新用户的 id"
        assert "username" in data["data"], "data 应包含 username"
    
    def test_create_user_duplicate_username(self, authenticated_client, test_user_data):
        """测试创建重复用户名"""
        # 第一次创建
        response1 = authenticated_client.post(
            "/api/v1/admin/users",
            json=test_user_data
        )
        assert response1.status_code == 201, "第一次创建应该成功"
        
        # 第二次创建（相同用户名）
        response2 = authenticated_client.post(
            "/api/v1/admin/users",
            json=test_user_data
        )
        
        assert response2.status_code == 409, f"重复用户名应返回 409，实际返回 {response2.status_code}"
        
        data = response2.json()
        assert data["success"] is False, "success 应为 false"
        assert data["code"] == 409, "code 应为 409"
        assert "用户名已存在" in data["message"], "错误信息应包含'用户名已存在'"
    
    def test_create_user_invalid_email(self, authenticated_client):
        """测试创建用户时使用无效邮箱"""
        from tests.api_test.test_config import get_unique_username, TEST_COMPANY_NAME, get_timestamp
        
        # 使用明确无效的邮箱格式（没有@符号）
        invalid_email = f"invalid_email_{get_timestamp()}"  # 没有 @ 符号，明确无效
        
        # 创建一个新的测试数据，使用唯一用户名和无效邮箱
        invalid_user_data = {
            "username": get_unique_username(),  # 使用唯一用户名避免冲突
            "email": invalid_email,  # 使用无效邮箱格式
            "password": "Test123456",
            "role": "user",
            "company_name": TEST_COMPANY_NAME,
            "is_active": True
        }
        
        response = authenticated_client.post(
            "/api/v1/admin/users",
            json=invalid_user_data
        )
        
        assert response.status_code == 422, f"无效邮箱应返回 422，实际返回 {response.status_code}，响应: {response.json()}"
        
        data = response.json()
        assert data["success"] is False, "success 应为 false"
        assert data["code"] == 422, "code 应为 422"
    
    def test_get_user_by_id(self, authenticated_client):
        """测试获取用户详情"""
        # 先获取用户列表，取第一个用户的 ID
        list_response = authenticated_client.get("/api/v1/admin/users?page=1&page_size=1")
        list_data = list_response.json()
        
        if list_data["data"]["total"] > 0:
            user_id = list_data["data"]["users"][0]["id"]
            
            response = authenticated_client.get(f"/api/v1/admin/users/{user_id}")
            
            assert response.status_code == 200, "获取用户详情应返回 200"
            
            data = response.json()
            assert data["success"] is True, "success 应为 true"
            assert data["code"] == 200, "code 应为 200"
            assert "data" in data, "响应应包含 data"
            assert data["data"]["id"] == user_id, "返回的用户 ID 应匹配"
    
    def test_get_user_not_found(self, authenticated_client):
        """测试获取不存在的用户"""
        response = authenticated_client.get(
            f"/api/v1/admin/users/{NON_EXISTENT_USER_ID}"
        )
        
        assert response.status_code == 404, "用户不存在应返回 404"
        
        data = response.json()
        assert data["success"] is False, "success 应为 false"
        assert data["code"] == 404, "code 应为 404"
        assert "用户不存在" in data["message"], "错误信息应包含'用户不存在'"
    
    def test_update_user(self, authenticated_client, test_user_data):
        """测试更新用户"""
        from tests.api_test.test_config import get_update_user_data
        
        # 先创建一个用户
        create_response = authenticated_client.post(
            "/api/v1/admin/users",
            json=test_user_data
        )
        assert create_response.status_code == 201, "创建用户应该成功"
        
        user_id = create_response.json()["data"]["id"]
        
        # 更新用户（使用配置文件中的更新数据）
        update_data = get_update_user_data()
        response = authenticated_client.put(
            f"/api/v1/admin/users/{user_id}",
            json=update_data
        )
        
        assert response.status_code in [200, 403], "更新用户应返回 200 或 403"
        
        if response.status_code == 200:
            data = response.json()
            assert data["success"] is True, "success 应为 true"
            assert data["code"] == 200, "code 应为 200"
    
    def test_delete_user_not_found(self, authenticated_client):
        """测试删除不存在的用户"""
        response = authenticated_client.delete(
            f"/api/v1/admin/users/{NON_EXISTENT_USER_ID}"
        )
        
        assert response.status_code == 404, "删除不存在的用户应返回 404"
        
        data = response.json()
        assert data["success"] is False, "success 应为 false"
        assert data["code"] == 404, "code 应为 404"
        assert "用户不存在" in data["message"], "错误信息应包含'用户不存在'"
