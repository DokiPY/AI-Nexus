# ============================================
# AI-Nexus Backend Dockerfile
# 构建参数: ENV (local/test/staging/production)
# ============================================
FROM python:3.11-slim

WORKDIR /app

# 系统依赖（psycopg2-binary 需要 libpq）
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 先复制依赖文件，利用 Docker 缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY app/ ./app/
COPY db/ ./db/

# 不把 .env 文件打进镜像，所有配置通过运行时环境变量注入
# 本地开发如需 .env 文件，可通过 docker-compose 的 env_file 挂载

# 默认环境标识
ENV ENV=local

EXPOSE 8000

# 生产环境不开 reload，workers 可按需调整
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
