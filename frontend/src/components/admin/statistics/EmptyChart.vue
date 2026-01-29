<template>
  <div class="empty-state">
    <el-icon class="empty-icon"><component :is="icon" /></el-icon>
    <p class="empty-text">{{ title }}</p>
    <p class="empty-hint">{{ description }}</p>
  </div>
</template>

<script setup lang="ts">
import { DataLine } from '@element-plus/icons-vue'
import type { Component } from 'vue'

withDefaults(defineProps<{
  title?: string
  description?: string
  icon?: Component
}>(), {
  title: '暂无数据',
  description: '当有数据时，这里将显示图表',
  icon: DataLine as any
})
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #94a3b8;
}

.empty-icon {
  font-size: 64px;
  color: #cbd5e1;
  margin-bottom: 16px;
}

.empty-text {
  font-size: 16px;
  font-weight: 500;
  color: #64748b;
  margin: 0 0 8px 0;
}

.empty-hint {
  font-size: 13px;
  color: #94a3b8;
  margin: 0;
  max-width: 300px;
  text-align: center;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .empty-state {
    height: 250px;
  }
}
</style>
