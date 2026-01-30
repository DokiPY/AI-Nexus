<template>
  <!-- 表格容器 -->
  <div class="table-container" v-loading="loading" element-loading-background="rgba(255, 255, 255, 0.8)" element-loading-text="加载中...">
    <el-table 
      :data="users" 
      style="width: 100%"
      stripe
      highlight-current-row
      :row-style="{ height: '64px' }"
    >
    <el-table-column label="用户" min-width="240">
      <template #default="scope">
        <div class="user-info-cell">
          <div class="user-avatar" :style="getAvatarStyle()">
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

// 使用统一的蓝色，与品牌色和UI保持一致
const getAvatarStyle = () => {
  return {
    background: 'linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%)',
    color: '#0284c7'
  }
}
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
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.table-container :deep(.el-loading-mask) {
  border-radius: 14px;
}

.table-container :deep(.el-loading-spinner) {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  margin: 0;
}

.table-container :deep(.el-loading-spinner .circular) {
  width: 42px;
  height: 42px;
}

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

/* 编辑 - 品牌色 */
.action-edit {
  color: #3b82f6;
}

.action-edit:hover {
  background-color: #eff6ff;
  color: #2563eb;
}

/* 常规操作 - 灰色，hover变品牌色 */
.action-normal {
  color: #64748b;
}

.action-normal:hover {
  background-color: #f1f5f9;
  color: #3b82f6;
}

/* 删除 - 红色 */
.action-delete {
  color: #ef4444;
}

.action-delete:hover {
  background-color: #fef2f2;
  color: #dc2626;
}

.action-divider {
  width: 1px;
  height: 12px;
  background-color: #cbd5e1;
  margin: 0 2px;
  opacity: 0.5;
}

.role-cell {
  display: flex;
  align-items: center;
}

.role-tag {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 2px 10px;
  border-radius: 999px; /* Pill shape */
  font-size: 12px;
  font-weight: 500;
  border: 1px solid transparent;
  min-width: 64px;
}

/* 管理员 - 浅蓝背景，深蓝字 */
.role-tag-admin {
  background-color: #eff6ff;
  color: #3b82f6;
  border-color: #dbeafe;
}

/* 普通用户 - 浅灰背景，深灰字 */
.role-tag-user {
  background-color: #f8fafc;
  color: #64748b;
  border-color: #e2e8f0;
}

.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  font-weight: 500;
  padding: 2px 10px;
  border-radius: 999px;
  border: 1px solid transparent;
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

/* 启用状态 - 绿色 */
.status-badge.status-active {
  background-color: #ecfdf5;
  color: #059669;
  border-color: #a7f3d0;
}

.status-badge.status-active .status-dot {
  background-color: #10b981;
}

/* 禁用状态 - 橙色 */
.status-badge:not(.status-active) {
  background-color: #fff7ed;
  color: #ea580c;
  border-color: #fed7aa;
}

.status-badge:not(.status-active) .status-dot {
  background-color: #f97316;
}

.table-container :deep(.el-table) {
  --el-table-border-color: rgba(0, 0, 0, 0.06);
}

.user-info-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-avatar {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 15px;
  flex-shrink: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  text-shadow: none;
  position: relative;
  overflow: hidden;
  transition: all 0.2s ease;
}

.user-avatar:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

/* 精致的光泽效果 */
.user-avatar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.5) 0%, rgba(255, 255, 255, 0.1) 40%, rgba(0, 0, 0, 0.03) 100%);
  border-radius: 12px;
  pointer-events: none;
}

.user-detail {
  display: flex;
  flex-direction: column;
  justify-content: center;
  line-height: 1.4;
}

.user-name {
  font-weight: 600;
  color: #0f172a; /* Slate 900 - Darker */
  font-size: 14px;
}

.user-email {
  color: #64748b;
  font-size: 12px;
}

.table-container :deep(.el-table__header th) {
  background: rgba(248, 250, 252, 0.95);
  color: #475569; /* Slate 600 - Darker than before */
  font-weight: 600;
  font-size: 12px;
  padding: 12px 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #e2e8f0;
}

.table-container :deep(.el-table__body td) {
  padding: 12px 0;
  color: #334155;
  font-size: 13px;
}

.table-container :deep(.el-table__row:hover td) {
  background: rgba(59, 130, 246, 0.04);
}

.table-container :deep(.el-table__row) {
  transition: background-color 0.2s ease;
}

/* Hover 行在 fixed 列(右侧操作列)会是另一张表，必须一起覆盖，否则会出现“浅蓝不均匀” */
.table-container :deep(.el-table__body tr.hover-row > td.el-table__cell),
.table-container :deep(.el-table__fixed-body-wrapper tr.hover-row > td.el-table__cell),
.table-container :deep(.el-table__fixed-right tr.hover-row > td.el-table__cell),
.table-container :deep(.el-table__fixed-right-patch tr.hover-row > td.el-table__cell) {
  background-color: rgba(59, 130, 246, 0.06) !important;
}

/* 小屏/横向滚动时，fixed-right 会有阴影叠加在背景上，导致 hover 看起来“少一截/重叠”。
   这里改成更干净的分割线，避免阴影对 hover 颜色造成影响。 */
.table-container :deep(.el-table__fixed-right) {
  border-left: 1px solid rgba(0, 0, 0, 0.06);
  background-color: transparent;
}

.table-container :deep(.el-table__fixed-right-patch) {
  background-color: transparent;
}

.table-container :deep(.el-table__fixed-right)::before {
  /* Element Plus 的固定列阴影遮罩 */
  box-shadow: none !important;
  background: transparent !important;
  opacity: 0 !important;
  pointer-events: none !important;
}

/* 有些版本阴影在 ::after 或 fixed 容器上（横向滚动时），这里一并禁用，避免 hover 颜色被叠层压暗 */
.table-container :deep(.el-table__fixed-right)::after,
.table-container :deep(.el-table__fixed)::before,
.table-container :deep(.el-table__fixed)::after {
  box-shadow: none !important;
  background: transparent !important;
  opacity: 0 !important;
  pointer-events: none !important;
}
</style>
