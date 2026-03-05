"""工作流接口测试"""

import pytest


class TestWorkflowManagement:
    """工作流管理测试"""
    
    def test_get_user_workflows(self, authenticated_client):
        """测试获取用户可用工作流"""
        response = authenticated_client.get("/api/v1/user/workflows")
        
        assert response.status_code == 200, "获取工作流列表应返回 200"
        
        data = response.json()
        assert data["success"] is True, "success 应为 true"
        assert data["code"] == 200, "code 应为 200"
        assert "data" in data, "响应应包含 data"
        
        # 实际 API 返回的是包含 workflows 数组的对象
        assert "workflows" in data["data"], "data 应包含 workflows"
        assert "total_workflows" in data["data"], "data 应包含 total_workflows"
        assert "available_count" in data["data"], "data 应包含 available_count"
        assert isinstance(data["data"]["workflows"], list), "workflows 应为列表"
    
    def test_get_workflow_categories(self, authenticated_client):
        """测试获取工作流分类"""
        response = authenticated_client.get("/api/v1/user/workflows/categories")
        
        assert response.status_code == 200, "获取分类应返回 200"
        
        data = response.json()
        assert data["success"] is True, "success 应为 true"
        
        # 实际 API 返回的是包含 categories 数组的对象
        assert "data" in data, "响应应包含 data"
        assert "categories" in data["data"], "data 应包含 categories"
        assert isinstance(data["data"]["categories"], list), "categories 应为列表"
    
    def test_get_admin_workflows(self, authenticated_client):
        """测试管理员获取所有工作流"""
        response = authenticated_client.get("/api/v1/admin/workflows?page=1&page_size=10")
        
        assert response.status_code == 200, "获取工作流列表应返回 200"
        
        data = response.json()
        assert data["success"] is True, "success 应为 true"
        assert "data" in data, "响应应包含 data"
