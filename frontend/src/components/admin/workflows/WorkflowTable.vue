<template>
  <div class="table-container" v-loading="loading" element-loading-background="rgba(255, 255, 255, 0.8)" element-loading-text="加载中...">
    <el-table 
      :data="workflows" 
      style="width: 100%"
      stripe
      highlight-current-row
      :row-style="{ height: '64px' }"
    >
      <el-table-column label="工作流" min-width="200">
        <template #default="scope">
          <div class="workflow-info-cell">
            <div class="workflow-avatar" :style="getAvatarStyle()">
              {{ scope.row.name.charAt(0).toUpperCase() }}
            </div>
            <div class="workflow-detail">
              <el-tooltip 
                :content="scope.row.description || '暂无描述'" 
                placement="top"
                :disabled="!scope.row.description"
                effect="light"
                popper-class="workflow-tooltip"
              >
                <div class="workflow-name">{{ scope.row.name }}</div>
              </el-tooltip>
            </div>
          </div>
        </template>
      </el-table-column>
      <el-table-column prop="category" label="分类" min-width="120">
        <template #default="scope">
          <span class="status-badge" :class="getCategoryClass(scope.row.category)">
            <span class="status-dot"></span>
            {{ scope.row.category }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="http_method" label="请求方式" min-width="120">
        <template #default="scope">
          <span class="status-badge" :class="getMethodClass(scope.row.http_method)">
            <span class="status-dot"></span>
            {{ scope.row.http_method || 'POST' }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="n8n_webhook_url" label="N8N Webhook URL" min-width="250" show-overflow-tooltip />
      <el-table-column prop="created_at" label="创建时间" min-width="120">
        <template #default="scope">
          {{ formatDate(scope.row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180" :fixed="isCompact ? undefined : 'right'" align="right">
        <template #default="scope">
          <div class="action-buttons">
            <button class="action-link action-edit" @click="$emit('edit', scope.row)">
              编辑
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

interface Workflow {
  id: number
  name: string
  description?: string
  category: string
  http_method: string
  n8n_webhook_url: string
  created_at: string
}

interface WorkflowTableProps {
  workflows: Workflow[]
  loading: boolean
  currentPage?: number
  pageSize?: number
}

const props = withDefaults(defineProps<WorkflowTableProps>(), {
  currentPage: 1,
  pageSize: 10
})

const isCompact = ref(false)
let mediaQuery: MediaQueryList | null = null
const handleMediaChange = (e: MediaQueryListEvent | MediaQueryList) => {
  isCompact.value = 'matches' in e ? e.matches : (e as MediaQueryList).matches
}

onMounted(() => {
  mediaQuery = window.matchMedia('(max-width: 1200px)')
  handleMediaChange(mediaQuery)
  mediaQuery.addEventListener?.('change', handleMediaChange as any)
  mediaQuery.addListener?.(handleMediaChange as any)
})

onUnmounted(() => {
  if (!mediaQuery) return
  mediaQuery.removeEventListener?.('change', handleMediaChange as any)
  mediaQuery.removeListener?.(handleMediaChange as any)
})

defineEmits<{
  edit: [workflow: Workflow]
  delete: [workflow: Workflow]
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

// 根据请求方式返回对应的样式类
const getMethodClass = (method: string) => {
  const classes: Record<string, string> = {
    'POST': 'method-post',
    'GET': 'method-get',
    'PUT': 'method-put',
    'DELETE': 'method-delete'
  }
  return classes[method] || 'method-post'
}

// 根据分类返回对应的样式类
const getCategoryClass = (category: string) => {
  const classes: Record<string, string> = {
    '办公助手': 'category-office',
    '数据分析': 'category-data',
    '客户服务': 'category-service',
    '开发工具': 'category-dev'
  }
  return classes[category] || 'category-office'
}
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

/* 分类 - 绿色（和启用状态一样） */
.status-badge.status-active {
  background-color: #ecfdf5;
  color: #059669;
  border-color: #a7f3d0;
}

.status-badge.status-active .status-dot {
  background-color: #10b981;
}

/* 分类样式 - 不同分类不同颜色 */
/* 办公助手 - 蓝色 */
.status-badge.category-office {
  background-color: #eff6ff;
  color: #2563eb;
  border-color: #bfdbfe;
}

.status-badge.category-office .status-dot {
  background-color: #3b82f6;
}

/* 数据分析 - 紫色 */
.status-badge.category-data {
  background-color: #faf5ff;
  color: #9333ea;
  border-color: #e9d5ff;
}

.status-badge.category-data .status-dot {
  background-color: #a855f7;
}

/* 客户服务 - 青色 */
.status-badge.category-service {
  background-color: #ecfeff;
  color: #0891b2;
  border-color: #a5f3fc;
}

.status-badge.category-service .status-dot {
  background-color: #06b6d4;
}

/* 开发工具 - 绿色 */
.status-badge.category-dev {
  background-color: #ecfdf5;
  color: #059669;
  border-color: #a7f3d0;
}

.status-badge.category-dev .status-dot {
  background-color: #10b981;
}

/* POST - 绿色 */
.status-badge.method-post {
  background-color: #ecfdf5;
  color: #059669;
  border-color: #a7f3d0;
}

.status-badge.method-post .status-dot {
  background-color: #10b981;
}

/* GET - 蓝色 */
.status-badge.method-get {
  background-color: #eff6ff;
  color: #2563eb;
  border-color: #bfdbfe;
}

.status-badge.method-get .status-dot {
  background-color: #3b82f6;
}

/* PUT - 橙色 */
.status-badge.method-put {
  background-color: #fff7ed;
  color: #ea580c;
  border-color: #fed7aa;
}

.status-badge.method-put .status-dot {
  background-color: #f97316;
}

/* DELETE - 红色 */
.status-badge.method-delete {
  background-color: #fef2f2;
  color: #dc2626;
  border-color: #fecaca;
}

.status-badge.method-delete .status-dot {
  background-color: #ef4444;
}

.table-container :deep(.el-table) {
  --el-table-border-color: rgba(0, 0, 0, 0.06);
}

.workflow-info-cell {
  display: flex;
  align-items: center;
  gap: 12px;
}

.workflow-avatar {
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

.workflow-avatar:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

/* 精致的光泽效果 */
.workflow-avatar::before {
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

.workflow-detail {
  display: flex;
  flex-direction: column;
  justify-content: center;
  line-height: 1.4;
  flex: 1;
  min-width: 0;
}

.workflow-name {
  font-weight: 600;
  color: #0f172a;
  font-size: 14px;
  cursor: help;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  transition: color 0.2s ease;
}

.workflow-name:hover {
  color: #3b82f6;
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

<style>
/* Tooltip 样式 - 不使用 scoped，因为 tooltip 是挂载到 body 的 */
.workflow-tooltip {
  max-width: 400px;
  padding: 12px 16px !important;
  border-radius: 8px !important;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
  border: 1px solid #e5e7eb !important;
  font-size: 13px !important;
  line-height: 1.6 !important;
  color: #374151 !important;
  background: #ffffff !important;
}

.workflow-tooltip .el-popper__arrow::before {
  border: 1px solid #e5e7eb !important;
  background: #ffffff !important;
}
</style>