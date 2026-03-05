<template>
  <!-- 表格容器 -->
  <div class="table-container" v-loading="loading" element-loading-background="rgba(255, 255, 255, 0.8)" element-loading-text="加载中...">
    <el-table 
      :data="companies" 
      style="width: 100%"
      stripe
      highlight-current-row
      :row-style="{ height: '64px' }"
    >
      <el-table-column label="公司" min-width="240">
        <template #default="scope">
          <div class="company-info-cell">
            <div class="company-avatar" :style="getAvatarStyle()">
              {{ scope.row.name.charAt(0).toUpperCase() }}
            </div>
            <div class="company-detail">
              <div class="company-name">{{ scope.row.name }}</div>
              <div class="company-domain">{{ scope.row.domain || '-' }}</div>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="user_count" label="用户数" min-width="100">
        <template #default="scope">
          {{ scope.row.user_count || 0 }}人
        </template>
      </el-table-column>
      <el-table-column prop="is_active" label="状态" min-width="100">
        <template #default="scope">
          <span class="status-badge" :class="{ 'status-active': scope.row.is_active }">
            <span class="status-dot"></span>
            {{ scope.row.is_active ? '启用' : '禁用' }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="创建时间" min-width="120">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="240" fixed="right" align="right">
        <template #default="scope">
          <div class="action-buttons">
            <button class="action-link action-edit" @click="$emit('edit', scope.row)">
              编辑
            </button>
            <span class="action-divider"></span>
            <button class="action-link action-normal" @click="$emit('viewUsers', scope.row)">
              查看用户
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
import type { Company } from '@/services'

defineProps<{
  companies: Company[]
  loading: boolean
}>()

defineEmits<{
  edit: [company: Company]
  delete: [company: Company]
  viewUsers: [company: Company]
}>()

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('zh-CN')
}

// 深蓝渐变 + 白字
const getAvatarStyle = () => ({
  background: 'linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)',
  color: '#fff'
})
</script>

<style scoped>
.table-container {
  flex: 1;
  position: relative;
  border-radius: 14px;
  overflow: hidden;
  background: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  display: flex;
  flex-direction: column;
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

.company-info-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.company-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4), 0 1px 2px rgba(0, 0, 0, 0.1);
  letter-spacing: 0.5px;
}

.company-detail {
  display: flex;
  flex-direction: column;
  justify-content: center;
  line-height: 1.4;
}

.company-name {
  font-weight: 600;
  color: #0f172a;
  font-size: 14px;
}

.company-domain {
  color: #64748b;
  font-size: 12px;
}

.table-container :deep(.el-table__header th) {
  background: rgba(248, 250, 252, 0.95);
  color: #475569;
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

/* Hover 行在 fixed 列(右侧操作列)会是另一张表，必须一起覆盖 */
.table-container :deep(.el-table__body tr.hover-row > td.el-table__cell),
.table-container :deep(.el-table__fixed-body-wrapper tr.hover-row > td.el-table__cell),
.table-container :deep(.el-table__fixed-right tr.hover-row > td.el-table__cell),
.table-container :deep(.el-table__fixed-right-patch tr.hover-row > td.el-table__cell) {
  background-color: rgba(59, 130, 246, 0.06) !important;
}

/* 固定列样式优化 */
.table-container :deep(.el-table__fixed-right) {
  border-left: 1px solid rgba(0, 0, 0, 0.06);
  background-color: transparent;
}

.table-container :deep(.el-table__fixed-right-patch) {
  background-color: transparent;
}

.table-container :deep(.el-table__fixed-right)::before {
  box-shadow: none !important;
  background: transparent !important;
  opacity: 0 !important;
  pointer-events: none !important;
}

.table-container :deep(.el-table__fixed-right)::after,
.table-container :deep(.el-table__fixed)::before,
.table-container :deep(.el-table__fixed)::after {
  box-shadow: none !important;
  background: transparent !important;
  opacity: 0 !important;
  pointer-events: none !important;
}
</style>
