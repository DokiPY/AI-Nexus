"""pytest 配置和共享 fixtures"""

import pytest
import requests
from typing import Dict, Optional
from tests.api_test.test_config import (
    BASE_URL,
    REQUEST_TIMEOUT,
    ADMIN_USERNAME,
    ADMIN_PASSWORD,
    get_create_user_data,
    get_create_company_data
)


class APIClient:
    """API 测试客户端"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        self.cookies = None
        self.admin_token = None
        self.timeout = REQUEST_TIMEOUT
        
    def request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """发送 HTTP 请求"""
        url = f"{self.base_url}{endpoint}"
        # 如果没有指定 timeout，使用默认值
        if 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout
        response = self.session.request(method, url, **kwargs)
        return response
    
    def get(self, endpoint: str, **kwargs) -> requests.Response:
        """GET 请求"""
        return self.request("GET", endpoint, **kwargs)
    
    def post(self, endpoint: str, **kwargs) -> requests.Response:
        """POST 请求"""
        return self.request("POST", endpoint, **kwargs)
    
    def put(self, endpoint: str, **kwargs) -> requests.Response:
        """PUT 请求"""
        return self.request("PUT", endpoint, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> requests.Response:
        """DELETE 请求"""
        return self.request("DELETE", endpoint, **kwargs)
    
    def login(self, username: str = ADMIN_USERNAME, password: str = ADMIN_PASSWORD) -> Dict:
        """用户登录（默认使用配置文件中的管理员账号）"""
        response = self.post(
            "/api/v1/auth/login",
            json={"username": username, "password": password}
        )
        if response.status_code == 200:
            # 保存 cookies 到 session，这样后续请求会自动带上
            self.session.cookies.update(response.cookies)
            self.cookies = response.cookies
        return response.json()


@pytest.fixture(scope="function")
def api_client():
    """创建 API 客户端"""
    client = APIClient()
    return client


@pytest.fixture(scope="function")
def authenticated_client():
    """已登录的客户端（使用配置文件中的管理员账号）"""
    client = APIClient()
    login_result = client.login()
    # 确保登录成功
    assert login_result.get("success") == True, f"登录失败: {login_result}"
    return client


@pytest.fixture(scope="function")
def test_user_data():
    """测试用户数据（从配置文件生成）"""
    return get_create_user_data()


@pytest.fixture(scope="function")
def test_company_data():
    """测试公司数据（从配置文件生成）"""
    return get_create_company_data()
