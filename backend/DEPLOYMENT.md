# 后端部署指南

## 环境变量说明

后端支持多环境配置，通过 `ENV` 环境变量切换：

```bash
ENV=local       # 本地开发（默认）
ENV=test        # 测试环境
ENV=staging     # 预发布环境
ENV=production  # 生产环境
```

## 本地开发

```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 启动服务（默认使用 .env）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 生产部署

### 方式1：直接运行

```bash
# 设置环境变量并启动
ENV=production uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 方式2：使用 Gunicorn（推荐）

```bash
# 安装 Gunicorn
pip install gunicorn

# 启动（4个worker）
ENV=production gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --access-logfile - \
  --error-logfile -
```

### 方式3：使用 Systemd 服务

创建 `/etc/systemd/system/ai-agent-backend.service`：

```ini
[Unit]
Description=AI Agent Platform Backend
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/ai-agent-platform/backend
Environment="ENV=production"
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
ExecStart=/usr/local/bin/gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务：
```bash
sudo systemctl daemon-reload
sudo systemctl start ai-agent-backend
sudo systemctl enable ai-agent-backend
sudo systemctl status ai-agent-backend
```

## CORS 配置

在 `app/core/config.py` 中已配置允许的前端域名：

```python
ALLOWED_ORIGINS: List[str] = [
    "http://localhost:5173",      # 本地开发
    "https://localhost:5173",     # 本地开发（HTTPS）
    "http://localhost:4173",      # 本地预览
    "http://127.0.0.1:5173",      # 本地开发
    "http://38.150.3.103"         # 测试服务器
]
```

### 添加生产域名

修改 `app/core/config.py`，在 `ALLOWED_ORIGINS` 中添加：

```python
ALLOWED_ORIGINS: List[str] = [
    # ... 现有配置
    "https://your-domain.com",           # 你的生产域名
    "https://pro2.cuscompass.com",       # CloudFront 域名
]
```

## 环境配置文件

```
backend/
├── .env                # 本地开发（默认）
├── .env.test           # 测试环境
├── .env.staging        # 预发布环境
├── .env.production     # 生产环境
└── .env.example        # 配置示例
```

## 配置项说明

| 配置项 | 说明 | 示例 |
|--------|------|------|
| ENV | 环境标识 | local/test/staging/production |
| DB_HOST | 数据库地址 | 127.0.0.1 |
| DB_PORT | 数据库端口 | 5432 |
| DB_USER | 数据库用户 | postgres |
| DB_PASSWORD | 数据库密码 | your_password |
| DB_NAME | 数据库名称 | ai_agent_platform |
| SECRET_KEY | JWT密钥 | 随机字符串 |
| ALGORITHM | JWT算法 | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token过期时间 | 480（8小时） |

## 安全建议

1. **生产环境必须修改**：
   - `SECRET_KEY` - 使用强随机密钥
   - `DB_PASSWORD` - 使用强密码
   
2. **生成安全密钥**：
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **不要提交敏感配置到 Git**：
   - `.env.production` 应该只在服务器上存在
   - 使用 AWS Secrets Manager 或环境变量管理敏感信息

## Nginx 反向代理配置

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /var/www/ai-agent-platform/frontend/frontend/dist-production;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 健康检查

```bash
# 检查服务状态
curl http://localhost:8000/

# 检查 API 文档
curl http://localhost:8000/docs
```

## 日志查看

```bash
# Systemd 服务日志
sudo journalctl -u ai-agent-backend -f

# Gunicorn 日志
tail -f /var/log/ai-agent-backend.log
```

## 常见问题

### 1. 数据库连接失败
检查 `.env` 文件中的数据库配置是否正确

### 2. CORS 错误
确保前端域名已添加到 `ALLOWED_ORIGINS`

### 3. Token 过期
调整 `ACCESS_TOKEN_EXPIRE_MINUTES` 配置

### 4. 端口被占用
```bash
# 查看端口占用
sudo lsof -i :8000

# 杀死进程
sudo kill -9 <PID>
```
