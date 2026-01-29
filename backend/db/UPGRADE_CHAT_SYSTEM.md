# 聊天记录系统升级说明

## 升级内容

### 1. 新增会话管理功能
- 每个用户的每个 workflow 可以有多个会话
- 自动创建会话，用第一条消息作为标题
- 支持会话级别的软删除

### 2. 优化数据库设计
- 新增 `chat_sessions` 表管理会话
- 优化 `chat_logs` 表，添加元数据字段
- 添加软删除支持（`is_deleted` 字段）
- 添加性能索引

### 3. 新增功能
- 清空聊天记录（软删除）
- 记录 AI 响应时间
- 支持 token 消耗统计（预留字段）
- 支持错误信息记录（预留字段）

## 升级步骤

### 1. 备份数据库
```bash
# PostgreSQL
pg_dump -U your_user -d your_database > backup_$(date +%Y%m%d).sql
```

### 2. 执行数据库迁移
```bash
psql -U your_user -d your_database -f migrate_chat_sessions.sql
```

### 3. 验证数据迁移
```sql
-- 检查记录数是否一致
SELECT COUNT(*) FROM chat_logs_backup;
SELECT COUNT(*) FROM chat_logs;

-- 检查会话是否正确创建
SELECT user_id, workflow_id, COUNT(*) as session_count 
FROM chat_sessions 
GROUP BY user_id, workflow_id;
```

### 4. 重启后端服务
```bash
# 停止服务
# 重启服务
```

### 5. 测试功能
- [ ] 发送消息正常
- [ ] 获取历史记录正常
- [ ] 清空聊天记录正常
- [ ] 刷新页面后清空的记录不再显示

### 6. 删除备份表（可选）
```sql
-- 确认一切正常后执行
DROP TABLE chat_logs_backup;
```

## 新增 API

### DELETE /chat/workflows/{workflow_id}
清空指定 workflow 的当前会话聊天记录（软删除）

**响应：**
```json
{
  "message": "聊天记录已清空"
}
```

## 数据库变更

### 新增表：chat_sessions
```sql
CREATE TABLE chat_sessions (
    id SERIAL PRIMARY KEY,
    user_id UUID NOT NULL,
    workflow_id INTEGER NOT NULL,
    title VARCHAR(255),
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 修改表：chat_logs
新增字段：
- `session_id` - 关联会话
- `response_time_ms` - 响应时间（毫秒）
- `token_count` - token 消耗
- `error_message` - 错误信息
- `is_deleted` - 软删除标记

## 注意事项

1. **数据迁移**：旧数据会自动迁移到新表结构，每个用户的每个 workflow 创建一个默认会话
2. **软删除**：清空操作不会真正删除数据，只是标记为已删除
3. **性能优化**：添加了多个索引，查询性能会有提升
4. **向后兼容**：API 接口保持兼容，前端无需大改

## 未来扩展

1. **多会话管理**：可以在前端添加会话列表，让用户切换不同会话
2. **会话标题编辑**：允许用户修改会话标题
3. **数据归档**：定期将已删除的数据归档到冷存储
4. **数据分析**：利用 response_time_ms 和 token_count 进行性能分析
