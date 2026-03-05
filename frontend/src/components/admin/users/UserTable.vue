<template>
  <!-- 表格容器 -->
  <div class="table-container" v-loading="loading" element-loading-background="rgba(255, 255, 255, 0.8)" element-loading-text="加载中...">
    <el-table 
      :data="users" 
      style="width: 100%"
      highlight-current-row
      :row-style="{ height: '72px' }"
    >
    <el-table-column label="用户" min-width="240">
      <template #default="scope">
        <div class="user-info-cell">
          <div class="user-avatar" :style="getAvatarStyle(scope.row.username)">
            {{ scope.row.username.charAt(0).toUpperCase() }}
          </div>
          <div class="user-detail">
            <div class="user-name">{{ scope.row.username }}</div>
            <div class="user-email">{{ scope.row.email || '-' }}</div>
          </div>
        </div>
      </template>
    </el-table-column>
    <el-table-column prop="role" label="角色" min-width="110">
      <template #default="scope">
        <div class="role-cell">
          <span class="role-tag" :class="scope.row.role === 'admin' ? 'role-tag-admin' : 'role-tag-user'">
            {{ scope.row.role === 'admin' ? '管理员' : '普通用户' }}
          </span>
        </div>
      </template>
    </el-table-column>
    <el-table-column prop="company_name" label="公司" min-width="120" />
    <el-table-column prop="is_active" label="状态" min-width="100">
      <template #default="scope">
        <span class="status-badge" :class="{ 'status-active': scope.row.is_active }">
          <span class="status-dot"></span>
          {{ scope.row.is_active ? '启用' : '禁用' }}
        </span>
      </template>
    </el-table-column>
    <el-table-column prop="workflow_count" label="工作流权限" min-width="120">
      <template #default="scope">
        {{ scope.row.workflow_count || 0 }}个
      </template>
    </el-table-column>
    <el-table-column prop="created_at" label="创建时间" min-width="120">
      <template #default="scope">
        {{ formatDate(scope.row.created_at) }}
      </template>
    </el-table-column>
    <el-table-column label="操作" width="280" :fixed="isCompact ? undefined : 'right'" align="right">
      <template #default="scope">
        <div class="action-buttons">
          <button class="action-link action-edit" @click="$emit('edit', scope.row)">
            编辑
          </button>
          <span class="action-divider"></span>
          <button class="action-link action-normal" @click="$emit('manageWorkflows', scope.row)">
            权限
          </button>
          <span class="action-divider"></span>
          <button class="action-link action-normal" @click="$emit('resetPassword', scope.row)">
            重置密码
          </button>
          <span class="action-divider"></span>
          <button class="action-link action-delete" @click="$emit('delete', scope.row)">
            删除
          </button>
        </div>
      </template>
    </el-table-column>
  </el-table>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import type { User } from '../../../services'

interface UserTableProps {
  users: User[]
  loading: boolean
  currentPage?: number
  pageSize?: number
}

// Props are defined but not directly used in script - they're accessed in template
withDefaults(defineProps<UserTableProps>(), {
  currentPage: 1,
  pageSize: 10
})

// 小屏直接取消 fixed 右侧操作列，避免 Element Plus 的滚动阴影层造成 hover 叠色/断层
const isCompact = ref(false)
let mediaQuery: MediaQueryList | null = null
const handleMediaChange = (e: MediaQueryListEvent | MediaQueryList) => {
  isCompact.value = 'matches' in e ? e.matches : (e as MediaQueryList).matches
}

onMounted(() => {
  // 这里的阈值可按你设计稿微调（例如 1200/1024）
  mediaQuery = window.matchMedia('(max-width: 1200px)')
  handleMediaChange(mediaQuery)
  mediaQuery.addEventListener?.('change', handleMediaChange as any)
  // Safari 兼容
  mediaQuery.addListener?.(handleMediaChange as any)
})

onUnmounted(() => {
  if (!mediaQuery) return
  mediaQuery.removeEventListener?.('change', handleMediaChange as any)
  mediaQuery.removeListener?.(handleMediaChange as any)
})

defineEmits<{
  edit: [user: User]
  delete: [user: User]
  manageWorkflows: [user: User]
  resetPassword: [user: User]
}>()

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const getAvatarStyle = (_username: string) => ({
  background: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
  color: '#fff'
})
</script>

<style scoped>
.table-container {
  flex: 1;
  margin-bottom: 20px;
  position: relative;
  border-radius: 14px;
  overflow: hidden;
  min-height: 400px;
  background: #ffffff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06), 0 1px 3px rgba(0, 0, 0, 0.04);
}

.table-container :deep(.el-loading-mask) { border-radius: 14px; }
.table-container :deep(.el-loading-spinner) {
  position: absolute; top: 50%; left: 50%;
  transform: translate(-50%, -50%); margin: 0;
}
.table-container :deep(.el-loading-spinner .circular) { width: 42px; height: 42px; }

/* 列头 */
.table-container :deep(.el-table__header th.el-table__cell) {
  background: rgba(248, 250, 252, 0.95);
  color: #475569;
  font-weight: 600;
  font-size: 12px;
  padding: 13px 0;
  letter-spacing: 0.4px;
  border-bottom: 1px solid #e2e8f0;
}

/* 行 */
.table-container :deep(.el-table__body td.el-table__cell) {
  padding: 12px 0;
  color: #334155;
  font-size: 13px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.04);
}

.table-container :deep(.el-table) {
  --el-table-border-color: rgba(0, 0, 0, 0.06);
}

/* hover */
.table-container :deep(.el-table__body tr.hover-row > td.el-table__cell),
.table-container :deep(.el-table__fixed-body-wrapper tr.hover-row > td.el-table__cell),
.table-container :deep(.el-table__fixed-right tr.hover-row > td.el-table__cell),
.table-container :deep(.el-table__fixed-right-patch tr.hover-row > td.el-table__cell) {
  background-color: rgba(59, 130, 246, 0.05) !important;
}

/* fixed 列阴影清除 */
.table-container :deep(.el-table__fixed-right) {
  border-left: 1px solid rgba(0, 0, 0, 0.06);
  background-color: transparent;
}
.table-container :deep(.el-table__fixed-right-patch) { background-color: transparent; }
.table-container :deep(.el-table__fixed-right)::before,
.table-container :deep(.el-table__fixed-right)::after,
.table-container :deep(.el-table__fixed)::before,
.table-container :deep(.el-table__fixed)::after {
  box-shadow: none !important;
  background: transparent !important;
  opacity: 0 !important;
  pointer-events: none !important;
}

/* 用户列 */
.user-info-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
  background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
  color: #fff;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4), 0 1px 2px rgba(0, 0, 0, 0.1);
  letter-spacing: 0.5px;
}

.user-detail {
  display: flex;
  flex-direction: column;
  justify-content: center;
  line-height: 1.4;
}

.user-name {
  font-weight: 600;
  color: #0f172a;
  font-size: 14px;
}

.user-email {
  color: #64748b;
  font-size: 12px;
}

/* 角色 badge */
.role-cell { display: flex; align-items: center; }

.role-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 12px;
  font-weight: 500;
  border: 1px solid transparent;
  min-width: 64px;
}

/* 管理员 - 紫色 */
.role-tag-admin {
  background-color: #f5f3ff;
  color: #7c3aed;
  border-color: #ddd6fe;
  box-shadow: 0 1px 3px rgba(124, 58, 237, 0.12);
}

/* 普通用户 - 蓝灰 */
.role-tag-user {
  background-color: #f0f9ff;
  color: #0369a1;
  border-color: #bae6fd;
  box-shadow: 0 1px 3px rgba(3, 105, 161, 0.1);
}

/* 状态 badge */
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
  padding: 3px 10px;
  border-radius: 999px;
  border: 1px solid transparent;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* 启用 - 绿色 */
.status-badge.status-active {
  background-color: #ecfdf5;
  color: #059669;
  border-color: #a7f3d0;
  box-shadow: 0 1px 3px rgba(5, 150, 105, 0.12);
}
.status-badge.status-active .status-dot { background-color: #10b981; }

/* 禁用 - 红色 */
.status-badge:not(.status-active) {
  background-color: #fef2f2;
  color: #dc2626;
  border-color: #fecaca;
  box-shadow: 0 1px 3px rgba(220, 38, 38, 0.1);
}
.status-badge:not(.status-active) .status-dot { background-color: #ef4444; }

/* 操作按钮 */
.action-buttons {
  display: inline-flex;
  align-items: center;
  justify-content: flex-end;
  gap: 4px;
}

.action-link {
  background: none;
  border: none;
  padding: 4px 8px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s ease;
  font-weight: 500;
  border-radius: 4px;
  line-height: 1.5;
}

.action-edit { color: #3b82f6; }
.action-edit:hover { background-color: #eff6ff; color: #2563eb; }

.action-normal { color: #64748b; }
.action-normal:hover { background-color: #f1f5f9; color: #3b82f6; }

.action-delete { color: #ef4444; }
.action-delete:hover { background-color: #fef2f2; color: #dc2626; }

.action-divider {
  width: 1px;
  height: 12px;
  background-color: #cbd5e1;
  margin: 0 2px;
  opacity: 0.5;
}
</style>