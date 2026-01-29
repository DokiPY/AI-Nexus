# 数据库相关文件

本目录包含所有数据库相关的文件和文档。

## 文件说明

### 初始化文件
- **create_tables.sql** - 数据库建表脚本（生产环境使用）
- **init_admin.py** - 管理员账户初始化脚本

### 文档
- **DATABASE_DESIGN.md** - 完整的数据库设计说明文档
- **UPGRADE_CHAT_SYSTEM.md** - 聊天系统升级说明（从旧版本升级时参考）

## 快速开始

### 1. 创建数据库
```bash
psql -U postgres -c "CREATE DATABASE ai_agent_platform;"
```

### 2. 执行建表脚本
```bash
psql -U postgres -d ai_agent_platform -f db/create_tables.sql
```

### 3. 创建管理员账户
```bash
python db/init_admin.py
```

## 注意事项

- 生产环境部署前请先备份数据库
- 修改数据库结构后需要更新 `DATABASE_DESIGN.md` 文档
- 所有数据库迁移脚本应保存在此目录
