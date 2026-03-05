<template>
  <div class="action-bar">
    <div class="left-actions">
      <button
        :class="['create-btn', createButtonVariant === 'soft' ? 'create-btn--soft' : 'create-btn--primary']"
        @click="$emit('create')"
      >
        <svg class="create-btn-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" />
        </svg>
        {{ createButtonText }}
      </button>
    </div>
    <div class="right-actions">
      <el-input
        class="search-input"
        :model-value="searchQuery"
        @update:model-value="$emit('update:searchQuery', $event)"
        :placeholder="searchPlaceholder"
        style="width: 280px"
        clearable
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
      <slot name="right-extra" />
      <el-tooltip content="刷新" placement="top">
        <el-button
          class="icon-btn"
          @click="$emit('refresh')"
          :icon="Refresh"
          :loading="loading"
          circle
        />
      </el-tooltip>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Search, Refresh } from '@element-plus/icons-vue'

defineProps<{
  searchQuery: string
  loading: boolean
  createButtonText: string
  searchPlaceholder: string
  /**
   * primary: 强主按钮（默认，适用于“新建/新增”的高强调动作）
   * soft: 轻量主按钮（更融入卡片/表格风格，适用于不想太“跳”的页面）
   */
  createButtonVariant?: 'primary' | 'soft'
}>()

defineEmits<{
  'update:searchQuery': [value: string]
  create: []
  refresh: []
}>()
</script>

<style scoped>
.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: -24px -24px 20px -24px;
  padding: 14px 24px;
  flex-shrink: 0;
  background: rgba(248, 250, 252, 0.8);
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 16px 16px 0 0;
}

.left-actions {
  display: flex;
  gap: 12px;
}

.right-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

/* 新增按钮基础 */
.create-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 36px;
  padding: 0 16px;
  border-radius: 8px;
  font-weight: 600;
  font-size: 13px;
  letter-spacing: 0.2px;
  cursor: pointer;
  border: none;
  outline: none;
  transition: all 0.2s ease;
  white-space: nowrap;
}

.create-btn-icon {
  width: 15px;
  height: 15px;
  flex-shrink: 0;
}

/* primary 变体 */
.create-btn--primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
}

.create-btn--primary:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  box-shadow: 0 6px 16px rgba(37, 99, 235, 0.35);
  transform: translateY(-1px);
}

.create-btn--primary:active {
  box-shadow: 0 1px 4px rgba(37, 99, 235, 0.2);
  transform: translateY(0);
}

/* soft 变体 */
.create-btn--soft {
  background: #eff6ff;
  color: #2563eb;
  border: 1.5px solid #bfdbfe;
  box-shadow: none;
}

.create-btn--soft:hover {
  background: #dbeafe;
  color: #1d4ed8;
  border-color: #93c5fd;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.1);
  transform: translateY(-1px);
}

.create-btn--soft:active {
  box-shadow: none;
  transform: translateY(0);
}

/* 搜索框样式保持一致 */
.search-input :deep(.el-input__wrapper) {
  border-radius: 10px;
  box-shadow: none;
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.08);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  height: 40px;
}

.search-input :deep(.el-input__wrapper.is-focus) {
  border-color: rgba(59, 130, 246, 0.4);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.08);
  background: #ffffff;
}

.right-actions .el-button.is-circle {
  width: 40px;
  height: 40px;
  padding: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
}

.icon-btn {
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: #ffffff;
  color: #64748b;
  transition: all 0.2s;
}

.icon-btn:hover {
  border-color: rgba(59, 130, 246, 0.35);
  color: #3b82f6;
  background: #fff;
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
}
</style>
