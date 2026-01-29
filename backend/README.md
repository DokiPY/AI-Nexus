# AI Agent Platform - Backend

基于 FastAPI 的 AI Agent 编排平台后端服务。

## 项目背景

这是一个企业级 AI Agent 编排平台，主要功能包括：

- **多租户架构**：支持不同公司的员工独立使用
- **权限管理**：管理员分配员工工作流权限
- **工作流编排**：集成 N8N，提供多种 AI Agent 工作流
- **会话管理**：支持多会话聊天，类似 ChatGPT
- **软删除机制**：聊天记录可恢复，符合审计要求
- **企业认证**：基于 JWT 的用户认证体系

## 技术栈

- **框架**：FastAPI + Uvicorn
- **数据库**：PostgreSQL + SQLAlchemy ORM
- **认证**：JWT + OAuth2
- **密码加密**：bcrypt
- **配置管理**：Pydantic Settings
- **N8N 集成**：通过 Webhook 调用工作流

## 目录结构

```
backend/
├── .env                    # 环境变量配置
├── requirements.txt        # Python依赖包
├── README.md              # 项目说明
├── db/                    # 数据库相关文件
│   ├── README.md          # 数据库文档索引
│   ├── create_tables.sql  # 建表脚本
│   ├── init_admin.py      # 管理员初始化
│   ├── DATABASE_DESIGN.md # 数据库设计文档
│   └── UPGRADE_CHAT_SYSTEM.md # 升级说明
└── app/                   # 主应用目录
    ├── main.py            # FastAPI应用实例
    ├── api/               # API路由模块
    │   ├── api_router.py  # 路由汇总
    │   ├── deps.py        # 依赖注入
    │   ├── login/         # 登录认证
    │   ├── workflows/     # 工作流管理
    │   ├── chat/          # 聊天API
    │   └── admin/         # 管理员API
    │       ├── users/     # 用户管理
    │       └── companies/ # 公司管理
    ├── core/              # 核心配置
    │   ├── config.py      # 应用配置
    │   ├── jwt.py         # JWT工具
    │   └── security.py    # 密码加密
    ├── database/          # 数据库相关
    │   └── connection.py  # 数据库连接
    ├── models/            # SQLAlchemy ORM模型
    │   ├── user.py        # 用户、公司模型
    │   └── workflow.py    # 工作流、会话、聊天记录
    ├── schemas/           # Pydantic数据模型
    │   ├── auth.py        # 认证模型
    │   ├── user.py        # 用户模型
    │   ├── company.py     # 公司模型
    │   └── workflow.py    # 工作流模型
    └── services/          # 业务逻辑层
        ├── n8n_service.py # N8N集成服务
        ├── login/         # 登录服务
        └── admin/         # 管理员服务
```

## 数据库设计

### 核心表结构
- `companies` - 公司信息
- `users` - 用户信息（UUID主键）
- `workflows` - 工作流定义
- `company_workflows` - 公司工作流授权（预留）
- `user_workflows` - 用户工作流授权
- `chat_sessions` - 聊天会话（支持多会话）
- `chat_logs` - 聊天消息（支持软删除）

详细设计请查看：[db/DATABASE_DESIGN.md](db/DATABASE_DESIGN.md)

## 快速开始

### 1. 安装依赖
```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量

后端支持多环境配置，通过 `ENV` 环境变量切换：

```bash
ENV=local       # 本地开发（默认）
ENV=test        # 测试环境
ENV=staging     # 预发布环境
ENV=production  # 生产环境
```

编辑对应的 `.env` 文件：
```env
# 环境标识
ENV=local

# 数据库配置
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=your_password
DB_NAME=ai_agent_platform

# JWT配置
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480
```

### 3. 初始化数据库
```bash
# 创建数据库
psql -U postgres -c "CREATE DATABASE ai_agent_platform;"

# 执行建表脚本
psql -U postgres -d ai_agent_platform -f db/create_tables.sql

# 创建管理员账户
python db/init_admin.py
```

### 4. 启动服务

#### 本地开发（Windows PowerShell）
```powershell
# 默认使用 .env 文件
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 指定环境运行（Windows PowerShell）
```powershell
# 测试环境
$env:ENV="test"; uvicorn app.main:app --host 0.0.0.0 --port 8000

# 预发布环境
$env:ENV="staging"; uvicorn app.main:app --host 0.0.0.0 --port 8000

# 生产环境
$env:ENV="production"; uvicorn app.main:app --host 0.0.0.0 --port 8000
```

#### Linux/Mac 运行
```bash
# 本地开发
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 测试环境
ENV=test uvicorn app.main:app --host 0.0.0.0 --port 8000

# 生产环境
ENV=production uvicorn app.main:app --host 0.0.0.0 --port 8000
```

服务将在 `http://localhost:8000` 启动。

## API文档

启动服务后访问：
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 功能模块

### ✅ 已完成

**认证系统**
- [x] 用户登录/登出
- [x] JWT Token 管理
- [x] 权限验证（管理员/普通用户）

**用户管理**
- [x] 用户列表查询
- [x] 用户创建/编辑/删除
- [x] 用户工作流权限分配

**公司管理**
- [x] 公司列表查询
- [x] 公司创建/编辑/删除

**工作流管理**
- [x] 工作流列表查询（按权限过滤）
- [x] 工作流分类管理
- [x] 工作流创建/编辑/删除（管理员）
- [x] N8N Webhook 集成

**聊天系统**
- [x] 会话管理（自动创建）
- [x] 聊天历史查询
- [x] 发送消息并调用 N8N
- [x] 清空聊天记录（软删除）
- [x] 响应时间记录

### 🚧 未来扩展

- [ ] 公司级工作流购买管理
- [ ] 多会话切换UI
- [ ] 会话分享功能
- [ ] 消息全文搜索
- [ ] Token 消耗统计
- [ ] 数据分析面板

## 核心功能说明

### 权限控制
- **管理员**：可以管理所有用户、公司、工作流
- **普通用户**：只能访问被授权的工作流

### 会话管理
- 每个用户的每个 workflow 自动创建会话
- 用第一条消息作为会话标题
- 支持软删除，数据可恢复

### N8N 集成
- 通过 Webhook 调用 N8N 工作流
- 自动解析 HTML 实体编码
- 记录响应时间和错误信息

## 开发规范

- 遵循 FastAPI 最佳实践
- 使用 Pydantic 进行数据验证
- 业务逻辑封装在 services 层
- API 路由保持简洁，复杂逻辑下沉到服务层
- 数据库操作使用 SQLAlchemy ORM
- 敏感操作记录审计日志

## 部署说明

详细部署指南请查看：[DEPLOYMENT.md](DEPLOYMENT.md)

## 环境配置文件

```
backend/
├── .env                # 本地开发（默认）
├── .env.test           # 测试环境
├── .env.staging        # 预发布环境
├── .env.production     # 生产环境
└── .env.example        # 配置示例
```

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交代码
4. 发起 Pull Request

## 许可证

MIT License
