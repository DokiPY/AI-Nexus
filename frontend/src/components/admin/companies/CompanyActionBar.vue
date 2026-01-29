<template>
  <div class="action-bar">
    <div class="left">
      <el-input
        :model-value="searchQuery"
        @update:model-value="$emit('update:searchQuery', $event)"
        placeholder="搜索公司名称..."
        style="width: 300px"
        clearable
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>
    <div class="right">
      <el-button :icon="Refresh" :loading="loading" @click="$emit('refresh')" circle />
      <el-button type="primary" :icon="Plus" @click="$emit('create')" round>
        新增公司
      </el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Search, Refresh, Plus } from '@element-plus/icons-vue'

defineProps<{
  searchQuery: string
  loading: boolean
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
}

.right {
  display: flex;
  gap: 12px;
}
</style>
