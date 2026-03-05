# ============================================
# AI-Nexus Frontend Dockerfile (多阶段构建)
# 构建参数: VITE_ENV (test/staging/production)
# ============================================

# --- Stage 1: 构建 ---
FROM node:20-alpine AS builder

WORKDIR /app

# 先复制依赖文件，利用 Docker 缓存
COPY package.json package-lock.json ./
RUN npm ci

# 复制源码和环境配置
COPY . .

# 通过构建参数指定环境，默认 production
ARG VITE_ENV=production
ENV VITE_ENV=${VITE_ENV}

# 执行构建（输出到 dist-{VITE_ENV}）
RUN npx vue-tsc -b && npx vite build

# --- Stage 2: Nginx 静态服务 ---
FROM nginx:alpine

ARG VITE_ENV=production

# 复制构建产物
COPY --from=builder /app/dist-${VITE_ENV} /usr/share/nginx/html

# 自定义 nginx 配置（SPA history 模式 + API 反向代理）
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
