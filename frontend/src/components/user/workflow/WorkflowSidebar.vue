<template>
  <aside :class="['sidebar', { collapsed: collapsed }]">
    <div :class="['sidebar-panel', { pulse: pulse }]">
      <div class="sidebar-top">
        <h3 class="sidebar-title">
          <span class="sidebar-title-text">My Workflow</span>
        </h3>
        <button
          class="collapse-btn"
          type="button"
          :title="collapsed ? '展开侧边栏' : '收起侧边栏'"
          @click="$emit('toggle-collapse')"
        >
          <span class="collapse-icon">
            {{ collapsed ? '»' : '«' }}
          </span>
        </button>
      </div>

      <div v-if="!collapsed" class="search-box">
        <el-input
          ref="searchInputRef"
          :model-value="searchQuery"
          @update:model-value="$emit('update:searchQuery', $event)"
          size="small"
          clearable
          placeholder="搜索 Workflow..."
        />
      </div>

      <div v-if="!collapsed" class="category-tabs">
        <button 
          v-for="cat in categories" 
          :key="cat"
          :class="{ active: currentCategory === cat }"
          @click="$emit('update:currentCategory', cat)"
        >
          {{ cat }}
        </button>
      </div>

      <div class="workflow-list">
        <div
          v-for="wf in workflows"
          :key="wf.id"
          :class="['workflow-item', { active: wf.id === activeWorkflowId }]"
          :title="wf.name"
          @click="$emit('select-workflow', wf)"
        >
          <div class="wf-avatar">
            {{ (wf?.name?.[0] || 'W').toUpperCase() }}
          </div>
          <div class="wf-meta">
            <div class="wf-name" :title="wf.name">{{ wf.name }}</div>
            <div class="wf-desc" :title="wf.description">{{ wf.description }}</div>
          </div>
        </div>

        <div v-if="workflows.length === 0 && !loading && !collapsed" class="empty-state">
          暂无可用的 Workflow
        </div>
        <div
          v-else-if="workflows.length === 0 && !loading && collapsed"
          class="empty-state-collapsed"
          title="暂无可用的 Workflow"
        >
          —
        </div>

        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>
          加载中...
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref } from 'vue'

defineProps<{
  collapsed: boolean
  pulse: boolean
  searchQuery: string
  currentCategory: string
  categories: string[]
  workflows: any[]
  activeWorkflowId?: number
  loading: boolean
}>()

defineEmits<{
  'toggle-collapse': []
  'update:searchQuery': [value: string]
  'update:currentCategory': [value: string]
  'select-workflow': [workflow: any]
}>()

const searchInputRef = ref<any>(null)

defineExpose({
  focusSearch: () => searchInputRef.value?.focus?.()
})
</script>

<style scoped>
.sidebar {
  width: 320px;
  min-width: 320px;
  background: transparent;
  padding: 0 12px 12px;
  display: flex;
  flex-direction: column;
  transition: width 0.2s ease, min-width 0.2s ease, padding 0.2s ease;
}

.sidebar.collapsed {
  /* 折叠态下要保证头像区域的可用宽度，否则 40px 头像会被内容区挤压 */
  width: 88px;
  min-width: 88px;
  padding: 0 8px 12px;
}

.sidebar-panel {
  margin-top: 12px;
  height: calc(100% - 12px);
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  box-shadow: 0 8px 24px rgba(17, 24, 39, 0.06);
  padding: 14px 12px;
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.sidebar.collapsed .sidebar-panel {
  padding: 10px 8px;
}

.sidebar-panel.pulse {
  animation: sidebarPulse 0.9s ease-in-out;
}

@keyframes sidebarPulse {
  0% {
    box-shadow: 0 8px 24px rgba(17, 24, 39, 0.06);
    border-color: #e5e7eb;
  }
  45% {
    box-shadow: 0 12px 34px rgba(59, 130, 246, 0.22);
    border-color: rgba(59, 130, 246, 0.55);
  }
  100% {
    box-shadow: 0 8px 24px rgba(17, 24, 39, 0.06);
    border-color: #e5e7eb;
  }
}

.sidebar-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 12px;
}

.sidebar.collapsed .sidebar-top {
  justify-content: center;
}

.sidebar.collapsed .sidebar-title {
  display: none;
}

.sidebar-title {
  font-size: 16px;
  font-weight: 600;
  margin: 0;
  color: #374151;
  min-width: 0;
}

.sidebar-title-text {
  display: inline-block;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.collapse-btn {
  width: 34px;
  height: 34px;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
  background: #ffffff;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s ease, border-color 0.15s ease;
}

.collapse-btn:hover {
  background: #f3f4f6;
  border-color: #d1d5db;
}

.collapse-icon {
  font-size: 18px;
  color: #374151;
}

.search-box {
  margin-bottom: 12px;
  width: 100%;
  min-width: 0;
}

.search-box :deep(.el-input) {
  width: 100%;
}

.search-box :deep(.el-input__wrapper) {
  border-radius: 10px;
}

.category-tabs {
  display: flex;
  gap: 6px;
  margin-bottom: 16px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.category-tabs button {
  padding: 6px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 999px;
  background: white;
  color: #6b7280;
  font-size: 12px;
  cursor: pointer;
  white-space: nowrap;
  transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease;
}

.category-tabs button:hover {
  background: #f3f4f6;
}

.category-tabs button.active {
  background: #1f3a5f;
  color: white;
  border-color: #1f3a5f;
}

.workflow-list {
  flex: 1;
  overflow-y: auto;
  padding-right: 2px;
}

.workflow-item {
  padding: 12px;
  border-radius: 12px;
  cursor: pointer;
  margin-bottom: 8px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 12px;
  border: 1px solid transparent;
  position: relative;
}

.workflow-item:hover {
  background: #f8fafc;
}

.workflow-item.active {
  background: #eff6ff;
  border-color: rgba(59, 130, 246, 0.15);
}

.workflow-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 12px;
  bottom: 12px;
  width: 3px;
  background-color: #3b82f6;
  border-radius: 0 3px 3px 0;
  opacity: 0; /* 默认不显示，根据需要开启 */
}

.wf-avatar {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: #ffffff;
  color: #3b82f6;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  flex: 0 0 auto;
  box-shadow: 0 2px 6px rgba(59, 130, 246, 0.08);
  border: 1px solid #eef2f6;
  transition: all 0.2s;
}

.workflow-item:hover .wf-avatar {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.12);
  border-color: #dbeafe;
}

.workflow-item.active .wf-avatar {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
  border-color: transparent;
}

.wf-meta {
  min-width: 0;
  flex: 1;
}

.sidebar.collapsed .wf-meta {
  display: none;
}

.sidebar.collapsed .workflow-item {
  justify-content: center;
  align-items: center;
  padding: 8px 6px;
  gap: 0;
  border-radius: 12px;
}

.sidebar.collapsed .workflow-list {
  padding-right: 0;
}

.sidebar.collapsed .wf-avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  font-size: 14px;
}

.sidebar.collapsed .workflow-item.active .wf-avatar {
  box-shadow:
    0 0 0 3px rgba(59, 130, 246, 0.25),
    0 6px 16px rgba(17, 24, 39, 0.12);
}

.wf-name {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.3;
}

.workflow-item.active .wf-name {
  color: #1e40af;
}

.wf-desc {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 3px;
  display: -webkit-box;
  line-clamp: 1;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
}

.workflow-item:hover .wf-desc {
  color: #64748b;
}

.workflow-item.active .wf-desc {
  color: #60a5fa;
}

.empty-state,
.loading-state {
  text-align: center;
  padding: 40px 20px;
  color: #9ca3af;
  font-size: 14px;
}

.empty-state-collapsed {
  text-align: center;
  padding: 24px 0;
  color: #9ca3af;
  font-size: 18px;
  line-height: 1;
  user-select: none;
}

.spinner {
  width: 24px;
  height: 24px;
  border: 3px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  margin: 0 auto 12px;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
