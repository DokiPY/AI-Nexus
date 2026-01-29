# AI Agent Platform - Frontend

## 项目简介

这是一个基于 **Vue 3 + TypeScript + Vite** 的企业级 AI 工作流管理平台前端项目。

### 核心功能
- 🔐 **用户认证系统** - 支持管理员和普通用户角色
- 👥 **用户管理** - 用户、公司、权限管理
- 🤖 **AI 工作流** - 工作流配置、分类、权限分配
- 💬 **智能对话** - 与 AI 工作流实时交互
- 📊 **数据统计** - 使用趋势、用户活跃度分析

### 技术栈
- **框架**: Vue 3 (Composition API + `<script setup>`)
- **语言**: TypeScript
- **构建工具**: Vite
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **UI 组件**: Element Plus
- **HTTP 客户端**: 自研 HttpClient (基于 Fetch API)
- **样式**: Scoped CSS + CSS Variables

---

## 项目结构

```
frontend/                   # 前端项目根目录
├── src/
│   ├── assets/                    # 静态资源
│   │   ├── images/               # 图片资源
│   │   ├── icons/                # 图标资源
│   │   └── styles/               # 全局样式
│   │
│   ├── components/                # 组件库（统一导出）
│   │   ├── index.ts              # ✨ 统一导出入口
│   │   ├── common/               # 公共组件
│   │   ├── login/                # 登录相关组件
│   │   ├── admin/                # 管理端组件
│   │   └── user/                 # 用户端组件
│   │
│   ├── composables/               # 组合式函数（统一导出）
│   │   ├── index.ts              # ✨ 统一导出入口
│   │   ├── common/               # 公共 Composables
│   │   ├── admin/                # 管理端业务逻辑
│   │   └── user/                 # 用户端业务逻辑
│   │
│   ├── router/                    # 路由配置
│   │   ├── index.ts              # 路由定义
│   │   └── guards.ts             # 路由守卫
│   │
│   ├── services/                  # API 服务层（统一导出）
│   │   ├── index.ts              # ✨ 统一导出入口
│   │   ├── http.ts               # ✨ HTTP 客户端
│   │   ├── login/                # 登录 API
│   │   ├── admin/                # 管理端 API
│   │   └── user/                 # 用户端 API
│   │
│   ├── stores/                    # Pinia 状态管理
│   │   ├── index.ts              # Store 统一导出
│   │   ├── login/                # 登录状态
│   │   └── admin/                # 管理端状态
│   │
│   ├── utils/                     # 工具函数
│   │   ├── auth.ts               # 认证工具
│   │   ├── debounce.ts           # 防抖
│   │   └── throttle.ts           # 节流
│   │
│   ├── views/                     # 页面视图
│   │   ├── login/                # 登录页
│   │   ├── admin/                # 管理端页面
│   │   └── user/                 # 用户端页面
│   │
│   ├── App.vue                    # 根组件
│   └── main.ts                    # 应用入口
│
├── .env                       # 本地开发配置
├── .env.test                  # 测试环境配置
├── .env.staging               # 预发布环境配置
├── .env.production            # 生产环境配置
├── .env.example               # 配置示例
├── .gitignore                 # Git 忽略文件
├── index.html                 # HTML 入口
├── package.json               # 项目配置
├── tsconfig.json              # TypeScript 配置
├── vite.config.ts             # Vite 配置
└── README.md                  # 项目说明
```

---

## 架构设计规范

### 1. 统一导出模式

所有模块都通过 `index.ts` 统一导出，使用 `@/` 别名导入：

```typescript
// ✅ 推荐：统一导入
import { UserApi, CompanyApi } from '@/services'
import { useUserManagement } from '@/composables'
import { AppHeader, UserTable } from '@/components'

// ❌ 避免：相对路径导入
import UserApi from '../../../services/admin/users/api'
```

### 2. HTTP 客户端设计

**核心文件**: `services/http.ts`

```typescript
// 统一的 HTTP 客户端
import { http } from '@/services'

// 自动处理：
// - Token 管理
// - 错误处理
// - 401/403 自动跳转
// - URL 参数构建

export class UserApi {
  static getUsers() {
    return http.get('/admin/users')
  }
  
  static createUser(data) {
    return http.post('/admin/users', data)
  }
}
```

### 3. 组件设计原则

- **单一职责**: 每个组件只负责一个功能
- **Props 类型化**: 使用 TypeScript 定义 Props
- **事件命名**: 使用 kebab-case (`@update:value`)
- **样式隔离**: 使用 `scoped` CSS

```vue
<script setup lang="ts">
interface Props {
  title: string
  count: number
}

defineProps<Props>()

defineEmits<{
  'update:count': [value: number]
}>()
</script>
```

### 4. Composables 设计

- **命名规范**: `use` 开头
- **返回对象**: 返回响应式数据和方法
- **职责分离**: 业务逻辑与组件分离

```typescript
export function useUserManagement() {
  const users = ref<User[]>([])
  const loading = ref(false)
  
  const loadUsers = async () => {
    loading.value = true
    try {
      users.value = await UserApi.getUsers()
    } finally {
      loading.value = false
    }
  }
  
  return {
    users,
    loading,
    loadUsers
  }
}
```

### 5. 路由设计

- **懒加载**: 所有路由组件使用动态导入
- **守卫分离**: 权限逻辑在 `guards.ts` 中
- **Meta 标记**: 使用 `meta` 定义权限要求

```typescript
const routes = [
  {
    path: '/admin',
    component: () => import('@/views/admin/AdminDashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  }
]
```

### 6. 类型定义

- **接口优先**: 使用 `interface` 定义数据结构
- **类型导出**: 每个模块的 `types.ts` 导出类型
- **类型复用**: 通过 `@/services` 统一导入

```typescript
// services/admin/users/types.ts
export interface User {
  id: string
  username: string
  role: 'admin' | 'user'
}

// 使用
import type { User } from '@/services'
```

---

## 开发规范

### 命名规范

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件文件 | PascalCase | `UserTable.vue` |
| 组件名称 | PascalCase | `<UserTable />` |
| Composables | camelCase + use前缀 | `useUserManagement` |
| 常量 | UPPER_SNAKE_CASE | `API_BASE_URL` |
| 变量/函数 | camelCase | `loadUsers` |
| 类型/接口 | PascalCase | `User`, `UserListResponse` |
| CSS 类名 | kebab-case | `.user-table` |

### 文件组织

```
module/
├── api.ts          # API 调用
├── types.ts        # 类型定义
└── index.ts        # 统一导出（可选）
```

### Git 提交规范

```
feat: 新功能
fix: 修复 bug
refactor: 重构代码
style: 样式调整
docs: 文档更新
chore: 构建/工具链更新
```

---

## 环境配置

### 环境变量

项目支持多环境配置：

```bash
VITE_ENV=local       # 本地开发（默认）
VITE_ENV=test        # 测试环境
VITE_ENV=staging     # 预发布环境
VITE_ENV=production  # 生产环境
```

编辑对应的 `.env` 文件：

```env
# .env (本地开发)
VITE_ENV=local
VITE_API_BASE_URL=http://localhost:8000/api/v1

# .env.production (生产环境)
VITE_ENV=production
VITE_API_BASE_URL=https://api.yourdomain.com/api/v1
```

### 路径别名

`vite.config.ts` 和 `tsconfig.app.json` 已配置：

```typescript
// 使用 @/ 代替相对路径
import { UserApi } from '@/services'
import { useUserManagement } from '@/composables'
```

---

## 核心特性

### 1. 统一 HTTP 客户端
- ✅ 自动 Token 管理
- ✅ 统一错误处理
- ✅ 401/403 自动跳转登录
- ✅ URL 参数自动构建
- ✅ TypeScript 类型支持

### 2. 模块化架构
- ✅ 按业务模块划分
- ✅ 统一导出入口
- ✅ 清晰的依赖关系
- ✅ 易于维护和扩展

### 3. 类型安全
- ✅ 全面的 TypeScript 覆盖
- ✅ 编译时错误检查
- ✅ IDE 智能提示
- ✅ 重构友好

### 4. 性能优化
- ✅ 路由懒加载
- ✅ 组件按需导入
- ✅ Keep-alive 缓存
- ✅ 防抖/节流处理

---

## 开发命令

```bash
# 进入项目目录
cd frontend

# 安装依赖
npm install

# 开发模式（默认使用 .env）
npm run dev

# 指定环境开发（Windows PowerShell）
$env:VITE_ENV="test"; npm run dev

# 指定环境开发（Linux/Mac）
VITE_ENV=test npm run dev

# 构建生产版本（Windows PowerShell）
$env:VITE_ENV="production"; npm run build

# 构建生产版本（Linux/Mac）
VITE_ENV=production npm run build

# 预览生产构建
npm run preview
```

---

## 项目亮点

1. **教科书级别的架构设计** - 完全符合 Vue 3 生产环境规范
2. **统一的代码风格** - 所有模块遵循相同的设计模式
3. **优秀的可维护性** - 清晰的模块划分和统一导出
4. **完善的类型系统** - TypeScript 全覆盖
5. **高性能** - 懒加载、缓存、优化的渲染策略

---

## 技术文档

- [Vue 3 官方文档](https://cn.vuejs.org/)
- [TypeScript 官方文档](https://www.typescriptlang.org/)
- [Vite 官方文档](https://cn.vitejs.dev/)
- [Pinia 官方文档](https://pinia.vuejs.org/zh/)
- [Element Plus 官方文档](https://element-plus.org/zh-CN/)
