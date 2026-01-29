# 数据库设计说明

## 概述

AI Agent Platform 使用 PostgreSQL 数据库，采用多租户架构，支持公司级和用户级的工作流权限管理，以及完整的会话聊天系统。

## 数据库架构

### 1. 多租户架构

```
companies (公司)
    ↓
users (用户)
    ↓
user_workflows (用户权限)
```

### 2. 工作流权限体系

```
workflows (工作流)
    ↓
company_workflows (公司授权) → 【预留功能，暂未使用】
    ↓
user_workflows (用户授权) → 当前直接授权给用户
```

**注意：** 当前版本直接通过 `user_workflows` 授权，跳过了 `company_workflows` 层级。`company_workflows` 表为未来"公司购买套餐"功能预留。

### 3. 会话聊天系统

```
users + workflows
    ↓
chat_sessions (会话) → 支持多会话
    ↓
chat_logs (消息记录) → 支持软删除
```

## 表结构详解

### 核心业务表

#### 1. companies - 公司表
多租户的核心，每个公司独立管理用户和权限。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| name | VARCHAR(255) | 公司名称 |
| domain | VARCHAR(255) | 公司域名（唯一） |
| is_active | BOOLEAN | 是否启用 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

#### 2. users - 用户表
使用 UUID 作为主键，支持跨系统集成。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | UUID | 主键（自动生成） |
| username | VARCHAR(100) | 用户名（唯一） |
| email | VARCHAR(255) | 邮箱（唯一） |
| password_hash | VARCHAR(255) | 密码哈希 |
| company_id | INTEGER | 所属公司 |
| role | VARCHAR(50) | 角色（admin/user） |
| is_active | BOOLEAN | 是否启用 |
| last_login_at | TIMESTAMP | 最后登录时间 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

**索引：**
- `idx_users_company_id` - 按公司查询
- `idx_users_email` - 邮箱登录

#### 3. workflows - 工作流表
存储 N8N 工作流的元数据。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| name | VARCHAR(255) | 工作流名称 |
| description | TEXT | 描述 |
| n8n_webhook_url | TEXT | N8N Webhook URL |
| http_method | VARCHAR(10) | HTTP方法（POST/GET） |
| icon | VARCHAR(255) | 图标 |
| category | VARCHAR(100) | 分类（办公助手/数据分析等） |
| is_active | BOOLEAN | 是否启用 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

#### 4. company_workflows - 公司工作流授权表
**【预留功能 - 当前版本未使用】**

为未来"公司购买套餐"功能预留，当前版本直接通过 `user_workflows` 授权。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| company_id | INTEGER | 公司ID |
| workflow_id | INTEGER | 工作流ID |

**约束：**
- UNIQUE(company_id, workflow_id) - 防止重复授权

**未来用途：**
- 公司级别的工作流购买管理
- 支持不同公司购买不同的工作流套餐
- 管理员只能给用户授权公司已购买的工作流

#### 5. user_workflows - 用户工作流授权表
用户级权限控制，细粒度管理员工可使用的工作流。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| user_id | UUID | 用户ID |
| workflow_id | INTEGER | 工作流ID |

**约束：**
- UNIQUE(user_id, workflow_id) - 防止重复授权

### 聊天系统表

#### 6. chat_sessions - 会话表
支持多会话管理，类似 ChatGPT 的对话列表。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| user_id | UUID | 用户ID |
| workflow_id | INTEGER | 工作流ID |
| title | VARCHAR(255) | 会话标题 |
| is_deleted | BOOLEAN | 软删除标记 |
| created_at | TIMESTAMP | 创建时间 |
| updated_at | TIMESTAMP | 更新时间 |

**索引：**
- `idx_chat_sessions_user_id`
- `idx_chat_sessions_workflow_id`
- `idx_chat_sessions_is_deleted`

**特性：**
- 自动创建会话，用第一条消息作为标题
- 支持软删除，数据可恢复
- 每次打开 workflow 获取最新会话

#### 7. chat_logs - 聊天记录表
存储所有聊天消息，包含元数据用于分析。

| 字段 | 类型 | 说明 |
|------|------|------|
| id | SERIAL | 主键 |
| session_id | INTEGER | 会话ID |
| user_id | UUID | 用户ID |
| workflow_id | INTEGER | 工作流ID |
| role | VARCHAR(50) | 角色（user/ai） |
| message | TEXT | 消息内容 |
| response_time_ms | INTEGER | AI响应时间（毫秒） |
| token_count | INTEGER | Token消耗 |
| error_message | TEXT | 错误信息 |
| is_deleted | BOOLEAN | 软删除标记 |
| created_at | TIMESTAMP | 创建时间 |

**索引：**
- `idx_chat_logs_session_id`
- `idx_chat_logs_user_id`
- `idx_chat_logs_workflow_id`
- `idx_chat_logs_is_deleted`
- `idx_chat_logs_session_created` - 复合索引（会话+时间）
- `idx_chat_logs_user_workflow` - 复合索引（用户+工作流+删除标记）

**特性：**
- 软删除：清空聊天不会真正删除数据
- 元数据：记录响应时间、Token消耗等
- 性能优化：多个索引提升查询速度

## 数据关系图

```
┌─────────────┐
│  companies  │
└──────┬──────┘
       │ 1:N
       ↓
┌─────────────┐      ┌──────────────┐
│    users    │──────│  workflows   │
└──────┬──────┘  N:M └──────┬───────┘
       │                    │
       │ 1:N                │ 1:N
       ↓                    ↓
┌─────────────────┐  ┌──────────────────┐
│ chat_sessions   │  │ company_workflows│
└────────┬────────┘  └──────────────────┘
         │ 1:N            (预留)
         ↓
┌─────────────────┐
│   chat_logs     │
└─────────────────┘
```

## 权限控制逻辑

### 当前版本的权限检查

**用户访问工作流的条件：**

1. **用户级权限**（当前使用）：用户必须被授权使用
   ```sql
   SELECT * FROM user_workflows 
   WHERE user_id = ? AND workflow_id = ?
   ```

2. **管理员例外**：role='admin' 的用户跳过权限检查

### 查询用户可见的工作流（当前实现）

```sql
SELECT w.* 
FROM workflows w
JOIN user_workflows uw ON w.id = uw.workflow_id
WHERE uw.user_id = ?
  AND w.is_active = TRUE
```

### 未来版本的权限检查（预留）

如果启用 `company_workflows` 表，权限检查将变为两层：

1. **公司级权限**：公司必须购买该工作流
   ```sql
   SELECT * FROM company_workflows 
   WHERE company_id = ? AND workflow_id = ?
   ```

2. **用户级权限**：用户必须被授权使用
   ```sql
   SELECT * FROM user_workflows 
   WHERE user_id = ? AND workflow_id = ?
   ```

3. **管理员例外**：role='admin' 的用户跳过权限检查

### 查询用户可见的工作流（未来版本）

```sql
SELECT w.* 
FROM workflows w
JOIN company_workflows cw ON w.id = cw.workflow_id
JOIN user_workflows uw ON w.id = uw.workflow_id
WHERE cw.company_id = ? 
  AND uw.user_id = ?
  AND w.is_active = TRUE
```

## 软删除机制

### 清空聊天记录

```sql
-- 标记会话为已删除
UPDATE chat_sessions 
SET is_deleted = TRUE 
WHERE id = ?;

-- 标记消息为已删除
UPDATE chat_logs 
SET is_deleted = TRUE 
WHERE session_id = ?;
```

### 查询时过滤已删除记录

```sql
SELECT * FROM chat_logs 
WHERE session_id = ? 
  AND is_deleted = FALSE
ORDER BY created_at ASC;
```

## 性能优化建议

### 1. 定期归档
将90天前已删除的数据归档到冷存储：

```sql
-- 归档会话
INSERT INTO chat_sessions_archive 
SELECT * FROM chat_sessions 
WHERE is_deleted = TRUE 
  AND updated_at < NOW() - INTERVAL '90 days';

-- 归档消息
INSERT INTO chat_logs_archive 
SELECT * FROM chat_logs 
WHERE is_deleted = TRUE 
  AND created_at < NOW() - INTERVAL '90 days';

-- 删除已归档数据
DELETE FROM chat_sessions 
WHERE is_deleted = TRUE 
  AND updated_at < NOW() - INTERVAL '90 days';

DELETE FROM chat_logs 
WHERE is_deleted = TRUE 
  AND created_at < NOW() - INTERVAL '90 days';
```

### 2. 分区表（可选）
对于大量数据，可以按时间分区：

```sql
CREATE TABLE chat_logs_2024_01 PARTITION OF chat_logs
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

### 3. 定期 VACUUM

```sql
VACUUM ANALYZE chat_logs;
VACUUM ANALYZE chat_sessions;
```

## 数据备份策略

### 每日备份
```bash
pg_dump -U postgres -d ai_agent_platform > backup_$(date +%Y%m%d).sql
```

### 恢复数据
```bash
psql -U postgres -d ai_agent_platform < backup_20240101.sql
```

## 安全建议

1. **密码加密**：使用 bcrypt 加密存储
2. **级联删除**：使用 ON DELETE CASCADE 保证数据一致性
3. **索引优化**：定期分析慢查询，添加必要索引
4. **访问控制**：数据库用户使用最小权限原则
5. **审计日志**：记录敏感操作（删除、权限变更等）

## 扩展性考虑

### 未来可能的扩展

1. **启用公司级权限**：实现"公司购买套餐"功能
2. **多会话切换**：前端添加会话列表UI
3. **会话分享**：支持会话分享给其他用户
4. **消息搜索**：添加全文搜索索引
5. **数据分析**：利用 response_time_ms 和 token_count 做性能分析
6. **消息附件**：支持上传文件到消息
7. **消息反馈**：用户对 AI 回复点赞/点踩
