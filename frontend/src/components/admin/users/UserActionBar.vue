<template>
  <!-- 操作栏 -->
  <div class="action-bar">
    <div class="left-actions">
      <el-button class="primary-btn" type="primary" @click="$emit('create')" size="default">
        <el-icon class="btn-icon"><Plus /></el-icon>
        新增用户
      </el-button>
    </div>
    <div class="right-actions">
      <el-input
        class="search-input"
        :model-value="searchQuery"
        @update:model-value="$emit('update:searchQuery', $event)"
        placeholder="搜索用户..."
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
import { Plus, Search, Refresh } from '@element-plus/icons-vue'

defineProps<{
  searchQuery: string
  loading: boolean
}>()

defineEmits<{
  create: []
  refresh: []
  'update:searchQuery': [value: string]
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
  padding: 0 18px;
  border-radius: 8px;
  font-weight: 500;
  font-size: 14px;
  background-color: #0284c7;
  border: none;
  box-shadow: 0 1px 3px rgba(2, 132, 199, 0.2);
  transition: all 0.2s ease;
  letter-spacing: 0.3px;
}

.primary-btn:hover {
  background-color: #0369a1;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(2, 132, 199, 0.3);
}

.primary-btn:active {
  transform: translateY(0);
  box-shadow: 0 1px 2px rgba(2, 132, 199, 0.2);
}

.btn-icon {
  margin-right: 6px;
  font-size: 16px;
}

.search-input :deep(.el-input__wrapper) {
  border-radius: 8px;
  box-shadow: none;
  background: rgba(248, 250, 252, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.06);
  transition: border-color 0.2s ease, background 0.2s ease;
}

.search-input :deep(.el-input__wrapper.is-focus) {
  border-color: rgba(2, 132, 199, 0.4);
  background: rgba(255, 255, 255, 1);
  box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.1);
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
  transition: all 0.2s ease;
}

.icon-btn:hover {
  border-color: rgba(2, 132, 199, 0.4);
  color: #0284c7;
  background: rgba(255, 255, 255, 1);
}
</style>