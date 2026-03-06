# AI-Nexus 云端部署指南 (Ubuntu)

## 架构概览

```
用户浏览器
    ↓ HTTPS
Cloudflare CDN (SSL 终端 / DNS)
    ↓ HTTPS
nginx-proxy 容器 (80/443)
    ├── / → ai-nexus-frontend 容器 (80)
    └── /api/v1/ → ai-nexus-backend 容器 (8000)
                        ↓
                  PostgreSQL 容器 (5432)
```

所有容器通过 Docker 内网通信，只有 nginx-proxy 对外暴露 80/443 端口。

## 目录结构

```
~/devops/AI-Nexus/
├── docker-compose.yml          # 前后端服务
├── .env.production             # 生产环境变量（需手动填写真实值）
├── .env.staging                # 预发布环境变量
├── backend/                    # 后端代码 + Dockerfile
├── frontend/                   # 前端代码 + Dockerfile + nginx.conf
└── nginx-proxy/                # 反向代理（独立 compose）
    ├── docker-compose.yml
    ├── conf.d/
    │   └── ai-nexus.conf       # 域名路由配置
    └── certbot-webroot/        # Let's Encrypt 验证目录
```

---

## Step 1: 服务器环境准备

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装 Docker
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# 重新登录使 docker 组生效

# 安装 certbot（用于 SSL 证书）
sudo apt install -y certbot

# 验证
docker --version
docker compose version
```

## Step 2: 部署 PostgreSQL

```bash
# 创建数据卷
docker volume create pgdata

# 启动 PostgreSQL
docker run -d \
  --name ai-nexus-postgres \
  -e POSTGRES_USER=your-db-user \
  -e POSTGRES_PASSWORD=your-db-password \
  -e POSTGRES_DB=ai_agent_platform \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  --restart unless-stopped \
  postgres:16-alpine
```

初始化数据库表：

```bash
# 将 SQL 文件复制进容器并执行
docker cp backend/db/create_tables.sql ai-nexus-postgres:/tmp/
docker exec -i ai-nexus-postgres psql -U your-db-user -d ai_agent_platform -f /tmp/create_tables.sql
```

初始化管理员账号：

```bash
# 在后端容器启动后执行（见 Step 5）
docker exec -i ai-nexus-backend python db/init_admin.py
```

## Step 3: 创建 Docker 网络

```bash
# 创建外部网络，nginx-proxy 和应用容器共享
docker network create nginx-proxy

# 将 PostgreSQL 加入网络（使后端容器可通过容器名访问）
docker network connect nginx-proxy ai-nexus-postgres
```

## Step 4: 配置环境变量

编辑服务器上的 `.env.production`，填入真实值：

```bash
vi ~/devops/AI-Nexus/.env.production
```

```dotenv
# 环境标识
ENV=production
VITE_ENV=production

# 数据库配置
DB_HOST=ai-nexus-postgres       # PostgreSQL 容器名
DB_PORT=5432
DB_USER=your-db-user            # 替换为真实用户名
DB_PASSWORD=your-db-password    # 替换为真实密码
DB_NAME=ai_agent_platform

# JWT 密钥（用 python 生成：python3 -c "import secrets; print(secrets.token_hex(32))"）
SECRET_KEY=your-production-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=480

# CORS
ALLOWED_ORIGINS=https://nexus.berivena.com,http://nexus.berivena.com

# 应用配置
DEBUG=false
```

> **注意**: `.env.production` 包含敏感信息，不要提交到 Git。确保 `.gitignore` 中已忽略。

## Step 5: 启动前后端服务

```bash
cd ~/devops/AI-Nexus

# 构建并启动（首次或代码更新后加 --build）
docker compose --env-file .env.production up -d --build

# 查看状态
docker ps

# 查看后端日志
docker logs ai-nexus-backend --tail 50

# 查看前端日志
docker logs ai-nexus-frontend --tail 20
```

将 PostgreSQL 也加入应用内网（如果还没加）：

```bash
docker network connect ai-nexus_ai-nexus ai-nexus-postgres
```

## Step 6: 申请 SSL 证书

先临时启动一个 HTTP-only 的 nginx 来完成证书验证：

```bash
cd ~/devops/AI-Nexus/nginx-proxy

# 确保 certbot-webroot 目录存在
mkdir -p certbot-webroot

# 先用临时 HTTP 配置启动 nginx-proxy（确保 80 端口可访问）
docker compose up -d
```

申请证书：

```bash
sudo certbot certonly --webroot \
  -w ~/devops/AI-Nexus/nginx-proxy/certbot-webroot \
  -d nexus.berivena.com \
  --email your-email@example.com \
  --agree-tos --no-eff-email
```

证书会保存在 `/etc/letsencrypt/live/nexus.berivena.com/`。

## Step 7: 启动 nginx-proxy（HTTPS）

```bash
cd ~/devops/AI-Nexus/nginx-proxy

# 重启以加载 HTTPS 配置（docker-compose.yml 已挂载 /etc/letsencrypt）
docker compose down
docker compose up -d

# 验证 nginx 配置
docker exec nginx-proxy nginx -t

# 验证 HTTPS
curl -I https://nexus.berivena.com/
```

## Step 8: Cloudflare 配置

1. DNS 记录：`nexus.berivena.com` → A 记录指向服务器公网 IP，开启代理（橙色云朵）
2. SSL/TLS → 加密模式选择 **完全（严格）**
3. 确保没有开启 "Always Use HTTPS" 以外的页面规则冲突

---

## 日常运维

### 更新代码部署

```bash
cd ~/devops/AI-Nexus

# 拉取最新代码
git pull

# 重新构建并启动
docker compose --env-file .env.production up -d --build

# 如果只改了后端
docker compose --env-file .env.production up -d --build backend

# 如果只改了前端
docker compose --env-file .env.production up -d --build frontend
```

### 查看日志

```bash
# 后端日志
docker logs ai-nexus-backend --tail 100 -f

# 前端 nginx 日志
docker logs ai-nexus-frontend --tail 50

# 反向代理日志
docker logs nginx-proxy --tail 50
```

### 重启服务

```bash
# 重启所有
docker compose --env-file .env.production restart

# 重启单个
docker restart ai-nexus-backend
docker restart ai-nexus-frontend
docker restart nginx-proxy
```

### SSL 证书续期

Certbot 会自动续期。手动续期：

```bash
sudo certbot renew

# 续期后重载 nginx
docker exec nginx-proxy nginx -s reload
```

### 清理 Docker 资源

```bash
# 清理无用镜像
docker image prune -f

# 清理所有未使用资源（谨慎）
docker system prune -f
```

---

## 网络拓扑

```
┌─────────────────────────────────────────────────┐
│  Docker Host (Ubuntu)                           │
│                                                 │
│  ┌─── nginx-proxy network (external) ────────┐  │
│  │                                           │  │
│  │  nginx-proxy (:80/:443 对外)              │  │
│  │       │                                   │  │
│  │  ai-nexus-frontend (:80 内部)             │  │
│  │  ai-nexus-backend  (:8000 内部)           │  │
│  │  ai-nexus-postgres (:5432)                │  │
│  │                                           │  │
│  └───────────────────────────────────────────┘  │
│                                                 │
│  ┌─── ai-nexus network (内部) ───────────────┐  │
│  │  ai-nexus-frontend                        │  │
│  │  ai-nexus-backend                         │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

## 常见问题

### 1. 后端 500 错误 - 数据库连接失败

```
connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed
```

原因：`DB_HOST` 为空或 PostgreSQL 不在同一 Docker 网络。

解决：
```bash
# 确认环境变量
docker exec ai-nexus-backend env | grep DB_

# 确认网络连通
docker network connect nginx-proxy ai-nexus-postgres
```

### 2. Cloudflare 521 错误

原因：Cloudflare 无法连接到源站。

解决：
- 确认 nginx-proxy 容器在运行且 443 端口监听
- 确认 Cloudflare SSL 模式为"完全（严格）"
- 确认证书文件存在：`docker exec nginx-proxy ls /etc/letsencrypt/live/nexus.berivena.com/`

### 3. 启动时环境变量警告

```
WARN: The "DB_HOST" variable is not set
```

原因：没有指定 `--env-file`。

解决：
```bash
docker compose --env-file .env.production up -d --build
```

### 4. 大文件 proxy buffer 警告

```
an upstream response is buffered to a temporary file
```

已在 `ai-nexus.conf` 中配置了更大的 `proxy_buffers`，重启 nginx-proxy 即可。
