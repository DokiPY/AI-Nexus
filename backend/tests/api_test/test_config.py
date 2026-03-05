"""
测试配置文件
集中管理所有测试参数，方便修改和维护
"""

# ============================================================================
# 基础配置
# ============================================================================

# API 基础 URL
BASE_URL = "http://localhost:8000"

# 请求超时时间（秒）
REQUEST_TIMEOUT = 30


# ============================================================================
# 测试账号配置
# ============================================================================

# 管理员账号（用于登录和管理员权限测试）
ADMIN_USERNAME = "lucky"
ADMIN_PASSWORD = "123456"

# 测试用的公司名称（用于创建用户时指定公司）
TEST_COMPANY_NAME = "Demo Company"

# 测试用的公司 ID（用于某些需要公司 ID 的测试）
TEST_COMPANY_ID = 1


# ============================================================================
# 用户管理测试配置
# ============================================================================

# 创建用户测试数据
CREATE_USER_DATA = {
    "username": "testuser_{timestamp}",  # {timestamp} 会被替换为时间戳
    "email": "testuser_{timestamp}@example.com",
    "password": "Test123456",
    "role": "user",
    "company_name": TEST_COMPANY_NAME,
    "is_active": True
}

# 更新用户测试数据
UPDATE_USER_DATA = {
    "email": "updated_{timestamp}@example.com",
    "role": "admin",
    "is_active": False
}

# 用户搜索关键词
USER_SEARCH_KEYWORD = "lucky"

# 无效的邮箱格式（用于测试参数验证）
INVALID_EMAIL = "not-an-email"  # 明确的无效邮箱格式,没有 @ 符号

# 不存在的用户 ID（UUID 格式）
NON_EXISTENT_USER_ID = "00000000-0000-0000-0000-000000000000"


# ============================================================================
# 公司管理测试配置
# ============================================================================

# 创建公司测试数据
CREATE_COMPANY_DATA = {
    "name": "测试公司_{timestamp}",
    "description": "这是一个测试公司",
    "is_active": True
}

# 不存在的公司 ID（整数格式）
NON_EXISTENT_COMPANY_ID = 999999


# ============================================================================
# 工作流管理测试配置
# ============================================================================

# 创建工作流测试数据
CREATE_WORKFLOW_DATA = {
    "name": "测试工作流_{timestamp}",
    "description": "这是一个测试工作流",
    "category": "测试",
    "webhook_url": "https://n8n.example.com/webhook/test",
    "is_active": True
}

# 不存在的工作流 ID（UUID 格式）
NON_EXISTENT_WORKFLOW_ID = "00000000-0000-0000-0000-000000000000"


# ============================================================================
# 分页配置
# ============================================================================

# 默认页码
DEFAULT_PAGE = 1

# 默认每页数量
DEFAULT_PAGE_SIZE = 10


# ============================================================================
# 辅助函数
# ============================================================================

import time

def get_timestamp():
    """获取当前时间戳（用于生成唯一的测试数据）"""
    return str(int(time.time() * 1000))


def get_unique_username():
    """生成唯一的用户名"""
    return CREATE_USER_DATA["username"].replace("{timestamp}", get_timestamp())


def get_unique_email():
    """生成唯一的邮箱"""
    return CREATE_USER_DATA["email"].replace("{timestamp}", get_timestamp())


def get_unique_company_name():
    """生成唯一的公司名称"""
    return CREATE_COMPANY_DATA["name"].replace("{timestamp}", get_timestamp())


def get_unique_workflow_name():
    """生成唯一的工作流名称"""
    return CREATE_WORKFLOW_DATA["name"].replace("{timestamp}", get_timestamp())


def get_create_user_data():
    """获取创建用户的测试数据（自动替换时间戳）"""
    timestamp = get_timestamp()
    return {
        "username": CREATE_USER_DATA["username"].replace("{timestamp}", timestamp),
        "email": CREATE_USER_DATA["email"].replace("{timestamp}", timestamp),
        "password": CREATE_USER_DATA["password"],
        "role": CREATE_USER_DATA["role"],
        "company_name": CREATE_USER_DATA["company_name"],
        "is_active": CREATE_USER_DATA["is_active"]
    }


def get_update_user_data():
    """获取更新用户的测试数据（自动替换时间戳）"""
    timestamp = get_timestamp()
    return {
        "email": UPDATE_USER_DATA["email"].replace("{timestamp}", timestamp),
        "role": UPDATE_USER_DATA["role"],
        "is_active": UPDATE_USER_DATA["is_active"]
    }


def get_create_company_data():
    """获取创建公司的测试数据（自动替换时间戳）"""
    timestamp = get_timestamp()
    return {
        "name": CREATE_COMPANY_DATA["name"].replace("{timestamp}", timestamp),
        "description": CREATE_COMPANY_DATA["description"],
        "is_active": CREATE_COMPANY_DATA["is_active"]
    }


def get_create_workflow_data():
    """获取创建工作流的测试数据（自动替换时间戳）"""
    timestamp = get_timestamp()
    return {
        "name": CREATE_WORKFLOW_DATA["name"].replace("{timestamp}", timestamp),
        "description": CREATE_WORKFLOW_DATA["description"],
        "category": CREATE_WORKFLOW_DATA["category"],
        "webhook_url": CREATE_WORKFLOW_DATA["webhook_url"],
        "is_active": CREATE_WORKFLOW_DATA["is_active"]
    }
