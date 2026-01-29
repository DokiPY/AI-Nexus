# 前端部署指南

## 环境变量说明

前端支持多环境配置，通过 `VITE_ENV` 环境变量切换：

```bash
VITE_ENV=local       # 本地开发（默认）
VITE_ENV=test        # 测试环境
VITE_ENV=staging     # 预发布环境
VITE_ENV=production  # 生产环境
```

## 本地开发

### Windows PowerShell
```powershell
cd frontend/frontend
npm install
npm run dev
```

### Linux/Mac
```bash
cd frontend/frontend
npm install
npm run dev
```

## 本地打包测试

### Windows PowerShell
```powershell
# 测试环境
$env:VITE_ENV="test"; npm run build
# 输出到: dist-test/

# 预发布环境
$env:VITE_ENV="staging"; npm run build
# 输出到: dist-staging/

# 生产环境
$env:VITE_ENV="production"; npm run build
# 输出到: dist-production/
```

### Linux/Mac
```bash
# 测试环境
VITE_ENV=test npm run build

# 预发布环境
VITE_ENV=staging npm run build

# 生产环境
VITE_ENV=production npm run build
```

## 环境配置文件

```
frontend/frontend/
├── .env                # 本地开发（默认）
├── .env.test           # 测试环境
├── .env.staging        # 预发布环境
├── .env.production     # 生产环境
└── .env.example        # 配置示例
```

修改对应环境的 `.env` 文件：
```env
VITE_ENV=production
VITE_API_BASE_URL=http://your-server-ip:8000/api/v1
```

---

## 部署方式：云端打包（推荐）

### 前置要求

Ubuntu 服务器需要安装：
- Node.js 18+ 
- Nginx

### 一、服务器环境准备

```bash
# 1. 安装 Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# 2. 验证安装
node -v  # 应该显示 v18.x.x
npm -v

# 3. 安装 Nginx
sudo apt update
sudo apt install nginx -y

# 4. 启动 Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 二、拉取代码并打包

```bash
# 1. 克隆代码（如果还没有）
cd /var/www
sudo git clone <your-git-repo-url> ai-agent-platform
cd ai-agent-platform/frontend

# 2. 修改生产环境配置
sudo nano .env.production
# 修改为你的服务器地址：
# VITE_ENV=production
# VITE_API_BASE_URL=http://your-server-ip:8000/api/v1

# 3. 安装依赖
sudo npm install

# 4. 打包构建（指定生产环境）
VITE_ENV=production sudo npm run build

# 打包完成后，dist-production 文件夹就是静态文件
```

### 三、配置 Nginx

```bash
# 1. 创建 Nginx 配置文件
sudo nano /etc/nginx/sites-available/ai-agent-platform
```

粘贴以下配置：

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 改成你的域名或服务器IP

    # 前端静态文件
    root /var/www/ai-agent-platform/frontend/dist-production;
    index index.html;

    # 处理 Vue Router 的 history 模式
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 代理后端 API（可选，如果前后端在同一服务器）
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gzip 压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/javascript application/json;
}
```

```bash
# 2. 启用配置
sudo ln -s /etc/nginx/sites-available/ai-agent-platform /etc/nginx/sites-enabled/

# 3. 测试配置
sudo nginx -t

# 4. 重启 Nginx
sudo systemctl restart nginx
```

### 四、访问应用

浏览器访问：`http://your-server-ip`

## 更新部署

后续更新只需：

```bash
cd /var/www/ai-agent-platform
sudo git pull
cd frontend
sudo npm install  # 如果有新依赖
VITE_ENV=production sudo npm run build
sudo systemctl restart nginx
```

## 常见问题

### 1. 打包失败：内存不足
```bash
# 增加 Node.js 内存限制
export NODE_OPTIONS="--max-old-space-size=4096"
sudo npm run build
```

### 2. 权限问题
```bash
# 修改文件夹权限
sudo chown -R $USER:$USER /var/www/ai-agent-platform
```

### 3. API 请求跨域
- 方案1：使用 Nginx 代理（推荐，见上面配置）
- 方案2：后端配置 CORS

### 4. 页面刷新 404
- 确保 Nginx 配置了 `try_files $uri $uri/ /index.html;`

## 生产优化建议

### 1. 使用 HTTPS
```bash
# 安装 Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取 SSL 证书
sudo certbot --nginx -d your-domain.com
```

### 2. 配置 PM2 管理后端
```bash
sudo npm install -g pm2
cd /var/www/ai-agent-platform/backend
pm2 start "uvicorn app.main:app --host 0.0.0.0 --port 8000" --name ai-agent-backend
pm2 save
pm2 startup
```

### 3. 设置防火墙
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp  # 如果后端需要外部访问
sudo ufw enable
```

## 目录结构

```
/var/www/ai-agent-platform/
├── backend/              # 后端代码
├── frontend/             # 前端代码
│   ├── dist-production/  # 打包后的静态文件（Nginx 指向这里）
│   ├── src/              # 源代码
│   ├── .env.production   # 生产环境配置
│   └── package.json
└── README.md
```

## 自动化部署（可选）

创建部署脚本 `deploy.sh`：

```bash
#!/bin/bash
cd /var/www/ai-agent-platform
git pull
cd frontend
npm install
VITE_ENV=production npm run build
sudo systemctl restart nginx
echo "部署完成！"
```

使用：
```bash
chmod +x deploy.sh
./deploy.sh
```
