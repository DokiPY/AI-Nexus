"""健康检查接口测试"""

import pytest


class TestHealthCheck:
    """健康检查测试"""
    
    def test_root_endpoint(self, api_client):
        """测试根路径"""
        response = api_client.get("/")
        
        assert response.status_code == 200, "根路径应返回 200"
        
        data = response.json()
        assert "message" in data, "响应应包含 message 字段"
        assert "status" in data, "响应应包含 status 字段"
        assert data["status"] == "running", "状态应为 running"
    
    def test_health_endpoint(self, api_client):
        """测试健康检查接口"""
        response = api_client.get("/health")
        
        assert response.status_code == 200, "健康检查应返回 200"
        
        data = response.json()
        assert "status" in data, "响应应包含 status 字段"
        assert data["status"] == "healthy", "状态应为 healthy"
