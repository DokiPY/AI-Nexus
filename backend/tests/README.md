# 自动化测试指南

## 测试环境准备

### 1. 确保后端服务正在运行

```bash
# 在另一个终端窗口中启动后端服务
cd AI-Nexus/backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 激活 Python 虚拟环境

```bash
# Windows
cd AI-Nexus/backend
app\venv\Scripts\activate

# Linux/Mac
cd AI-Nexus/backend
source app/venv/bin/activate
```

### 3. 安装测试依赖

```bash
pip install -r requirements-test.txt
```

## 运行测试

### 方式 1：使用测试运行器（推荐）

```bash
# 在 backend 目录下运行
python tests/run_tests.py
```

这会：
- 运行所有测试
- 生成 HTML 报告：`tests/report.html`
- 生成 Markdown 报告：`tests/TEST_REPORT.md`
- 生成 JSON 报告：`tests/report.json`

### 方式 2：直接使用 pytest

```bash
# 运行所有测试
pytest tests/ -v

# 运行特定测试文件
pytest tests/api_test/test_02_auth.py -v

# 运行特定测试用例
pytest tests/api_test/test_02_auth.py::TestAuthentication::test_login_success -v
```

## 测试目录结构

```
tests/
├── conftest.py              # pytest fixtures（API 客户端、登录等）
├── api_test/                # API 接口测试用例
│   ├── test_config.py       # 测试配置（URL、账号、测试数据）
│   ├── test_01_health.py    # 健康检查接口
│   ├── test_02_auth.py      # 认证功能
│   ├── test_03_users.py     # 用户管理
│   ├── test_04_companies.py # 公司管理
│   └── test_05_workflows.py # 工作流管理
├── utils/                   # 测试工具
│   └── generate_html_report.py  # HTML 报告生成器
└── output/                  # 测试报告输出
    ├── report.json          # pytest JSON 报告
    └── CLIENT_REPORT.html   # 客户友好 HTML 报告
```

## 测试文件说明

| 文件 | 说明 | 测试数量 |
|------|------|---------|
| `api_test/test_01_health.py` | 健康检查接口 | 2 |
| `api_test/test_02_auth.py` | 认证功能（登录、登出、获取用户信息） | 7 |
| `api_test/test_03_users.py` | 用户管理（CRUD + 权限） | 9 |
| `api_test/test_04_companies.py` | 公司管理（CRUD） | 4 |
| `api_test/test_05_workflows.py` | 工作流管理（查询） | 3 |

**总计**: 25 个测试用例

## 测试内容

### 验证项目

每个测试都会严格验证：

1. **HTTP 状态码**：确保返回正确的状态码（200/201/400/401/403/404/409）
2. **统一响应格式**：验证 `{success, code, message, data, request_id}` 格式
3. **响应头**：验证 `X-Request-ID` 和 `X-Process-Time` 存在
4. **业务逻辑**：验证数据的正确性
5. **错误处理**：验证各种异常情况的处理

### 测试分类

- **正常流程测试**：验证接口在正常情况下的行为
- **异常流程测试**：验证错误处理（如资源不存在、权限不足、参数错误等）
- **边界测试**：验证边界条件（如空值、重复数据等）

## 查看测试报告

### HTML 报告

```bash
# Windows
start tests/report.html

# Linux
xdg-open tests/report.html

# Mac
open tests/report.html
```

### Markdown 报告

```bash
# 使用任何文本编辑器或 Markdown 查看器
cat tests/TEST_REPORT.md
```

## 测试配置

测试配置在 `conftest.py` 中：

- **BASE_URL**: `http://localhost:8000/api/v1`
- **测试账号**: `admin` / `admin123`
- **自动清理**: 测试创建的数据会自动清理

## 常见问题

### Q1: 测试失败怎么办？

1. 检查后端服务是否正在运行
2. 检查数据库连接是否正常
3. 查看失败测试的错误信息
4. 检查测试数据是否正确

### Q2: 如何跳过某些测试？

```python
import pytest

@pytest.mark.skip(reason="暂时跳过")
def test_something():
    pass
```

### Q3: 如何只运行失败的测试？

```bash
pytest --lf  # last-failed
```

### Q4: 如何查看详细的错误信息？

```bash
pytest tests/ -v --tb=long
```

## 持续集成

可以将测试集成到 CI/CD 流程中：

```yaml
# .github/workflows/test.yml
name: API Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      - name: Run tests
        run: python tests/run_tests.py
```

## 测试最佳实践

1. **测试隔离**：每个测试独立运行，不依赖其他测试
2. **数据清理**：测试后清理创建的数据
3. **明确断言**：使用清晰的断言消息
4. **覆盖边界**：测试正常和异常情况
5. **保持简洁**：每个测试只验证一个功能点

## 下一步

- [ ] 添加更多测试用例（统计接口、聊天接口）
- [ ] 添加性能测试
- [ ] 添加压力测试
- [ ] 集成到 CI/CD
- [ ] 添加测试覆盖率报告
