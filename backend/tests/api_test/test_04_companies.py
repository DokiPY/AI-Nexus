"""公司管理接口测试"""

import pytest
from tests.api_test.test_config import (
    NON_EXISTENT_COMPANY_ID,
    DEFAULT_PAGE,
    DEFAULT_PAGE_SIZE
)


class TestCompanyManagement:
    """公司管理测试"""
    
    def test_get_companies_list(self, authenticated_client):
        """测试获取公司列表"""
        response = authenticated_client.get(
            f"/api/v1/admin/companies?page={DEFAULT_PAGE}&page_size={DEFAULT_PAGE_SIZE}"
        )
        
        assert response.status_code == 200, "获取公司列表应返回 200"
        
        data = response.json()
        assert data["success"] is True, "success 应为 true"
        assert data["code"] == 200, "code 应为 200"
        assert "data" in data, "响应应包含 data"
        assert "total" in data["data"], "data 应包含 total"
        assert "page" in data["data"], "data 应包含 page"
        assert "page_size" in data["data"], "data 应包含 page_size"
        assert "companies" in data["data"], "data 应包含 companies 列表"
        assert isinstance(data["data"]["companies"], list), "companies 应为列表"
    
    def test_create_company_success(self, authenticated_client, test_company_data):
        """测试创建公司成功"""
        # test_company_data 已经从配置文件生成
        response = authenticated_client.post(
            "/api/v1/admin/companies",
            json=test_company_data
        )
        
        assert response.status_code == 201, "创建公司应返回 201"
        
        data = response.json()
        assert data["success"] is True, "success 应为 true"
        assert data["code"] == 201, "code 应为 201"
        assert "公司创建成功" in data["message"], "message 应包含'公司创建成功'"
        assert "data" in data, "响应应包含 data"
        assert "id" in data["data"], "data 应包含新公司的 id"
        assert "name" in data["data"], "data 应包含 name"
    
    def test_get_company_by_id(self, authenticated_client):
        """测试获取公司详情"""
        # 先获取公司列表，取第一个公司的 ID
        list_response = authenticated_client.get(
            f"/api/v1/admin/companies?page={DEFAULT_PAGE}&page_size=1"
        )
        list_data = list_response.json()
        
        if list_data["data"]["total"] > 0:
            company_id = list_data["data"]["companies"][0]["id"]
            
            response = authenticated_client.get(f"/api/v1/admin/companies/{company_id}")
            
            assert response.status_code == 200, "获取公司详情应返回 200"
            
            data = response.json()
            assert data["success"] is True, "success 应为 true"
            assert data["code"] == 200, "code 应为 200"
            assert "data" in data, "响应应包含 data"
            assert data["data"]["id"] == company_id, "返回的公司 ID 应匹配"
    
    def test_get_company_not_found(self, authenticated_client):
        """测试获取不存在的公司"""
        response = authenticated_client.get(
            f"/api/v1/admin/companies/{NON_EXISTENT_COMPANY_ID}"
        )
        
        assert response.status_code == 404, "公司不存在应返回 404"
        
        data = response.json()
        assert data["success"] is False, "success 应为 false"
        assert data["code"] == 404, "code 应为 404"
        assert "公司不存在" in data["message"], "错误信息应包含'公司不存在'"
