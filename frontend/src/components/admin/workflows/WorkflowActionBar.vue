<template>
  <div class="action-bar">
    <div class="left-actions">
      <el-button class="primary-btn" type="primary" @click="$emit('create')" size="default" round>
        <el-icon><Plus /></el-icon>
        新建工作流
      </el-button>
    </div>
    <div class="right-actions">
      <el-input
        class="search-input"
        :model-value="searchQuery"
        @update:model-value="$emit('update:searchQuery', $event)"
        placeholder="搜索工作流..."
        style="width: 280px"
        clearable
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
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

interface ActionBarProps {
  searchQuery: string
  loading: boolean
}

defineProps<ActionBarProps>()

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

.primary-btn {
  height: 36px;
  font-weight: 600;
  box-shadow: 0 6px 16px rgba(59, 130, 246, 0.18);
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  box-shadow: none;
  background: rgba(248, 250, 252, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.06);
  transition: border-color 0.2s ease, background 0.2s ease;
}

.search-input :deep(.el-input__wrapper.is-focus) {
  border-color: rgba(59, 130, 246, 0.35);
  background: rgba(255, 255, 255, 0.95);
}

.right-actions .el-button.is-circle {
  width: 32px;
  height: 32px;
  padding: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.icon-btn {
  border: 1px solid rgba(0, 0, 0, 0.06);
  background: rgba(255, 255, 255, 0.9);
}

.icon-btn:hover {
  border-color: rgba(59, 130, 246, 0.35);
  color: #3b82f6;
}
</style>
