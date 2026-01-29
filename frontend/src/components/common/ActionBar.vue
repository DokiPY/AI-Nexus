<template>
  <div class="action-bar">
    <div class="left-actions">
      <el-button
        type="primary"
        :class="['create-btn', createButtonVariant === 'soft' ? 'create-btn--soft' : 'create-btn--primary']"
        :icon="Plus"
        @click="$emit('create')"
      >
        {{ createButtonText }}
      </el-button>
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
import { Search, Refresh, Plus } from '@element-plus/icons-vue'

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
  margin-bottom: 20px;
  flex-shrink: 0;
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

/* 新增按钮（默认 primary） */
.create-btn {
  height: 40px;
  padding: 0 24px;
  border-radius: 10px;
  font-weight: 500;
  font-size: 14px;
  transition: all 0.2s ease;
}

.create-btn--primary {
  border: none;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2), 0 2px 4px -1px rgba(37, 99, 235, 0.1);
}

.create-btn--primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.25), 0 4px 6px -2px rgba(37, 99, 235, 0.15);
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
}

.create-btn--primary:active {
  transform: translateY(0);
  box-shadow: none;
}

/* 轻量主按钮：更贴合表格/卡片的浅蓝体系 */
.create-btn--soft {
  color: #2563eb;
  border: none;
  background: linear-gradient(135deg, rgba(239, 246, 255, 0.95) 0%, rgba(219, 234, 254, 0.95) 100%);
  box-shadow: 0 1px 2px rgba(2, 6, 23, 0.06);
}

.create-btn--soft:hover {
  transform: translateY(-1px);
  color: #1d4ed8;
  background: linear-gradient(135deg, rgba(219, 234, 254, 1) 0%, rgba(191, 219, 254, 1) 100%);
  box-shadow: 0 6px 14px rgba(37, 99, 235, 0.12);
}

.create-btn--soft:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(2, 6, 23, 0.06);
}

/* 搜索框样式保持一致 */
.search-input :deep(.el-input__wrapper) {
  border-radius: 10px;
  box-shadow: none;
  background: rgba(248, 250, 252, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.06);
  transition: border-color 0.2s ease, background 0.2s ease;
  height: 40px;
}

.search-input :deep(.el-input__wrapper.is-focus) {
  border-color: rgba(59, 130, 246, 0.35);
  background: rgba(255, 255, 255, 0.95);
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
  border: 1px solid rgba(0, 0, 0, 0.06);
  background: rgba(255, 255, 255, 0.9);
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
