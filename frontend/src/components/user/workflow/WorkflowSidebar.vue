<template>
  <aside :class="['sidebar', { collapsed: collapsed }]">
    <div :class="['sidebar-panel', { pulse: pulse }]">
      <div class="sidebar-top">
        <div v-if="!collapsed" class="brand-area">
          <div class="brand-row">
            <span class="brand-name">AI Agents</span>
            <span class="brand-badge"><span class="badge-dot"></span>在线</span>
          </div>
        </div>
        <button class="collapse-btn" type="button"
          :title="collapsed ? '展开侧边栏' : '收起侧边栏'"
          @click="$emit('toggle-collapse')">
          <span class="collapse-icon">{{ collapsed ? '»' : '«' }}</span>
        </button>
      </div>

      <div v-if="!collapsed" class="search-bar">
        <div class="search-inner">
          <svg class="search-icon" viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
          </svg>
          <input ref="searchInputRef" type="text" class="search-input"
            :value="searchQuery" placeholder="搜索助手..."
            @input="$emit('update:searchQuery', ($event.target as HTMLInputElement).value)" />
          <button v-if="searchQuery" class="search-clear" @click="$emit('update:searchQuery', '')">✕</button>
        </div>
      </div>

      <div v-if="!collapsed" class="filter-pills">
        <button v-for="cat in categories" :key="cat"
          :class="['pill', { active: currentCategory === cat }]"
          @click="$emit('update:currentCategory', cat)">
          {{ cat === '全部' ? '全部' : cat }}
        </button>
      </div>

      <div class="workflow-list">
        <el-tooltip v-for="wf in workflows" :key="wf.id"
          :content="wf.description || '暂无描述'" placement="right" effect="light"
          :show-after="400" :disabled="collapsed" popper-class="agent-tooltip">
          <div :class="['workflow-item', { active: wf.id === activeWorkflowId }]"
            @click="$emit('select-workflow', wf)">
            <div class="wf-avatar">{{ (wf?.name?.[0] || 'A').toUpperCase() }}</div>
            <div class="wf-meta">
              <div class="wf-name">{{ wf.name }}</div>
              <div class="wf-desc">{{ wf.description || '暂无描述' }}</div>
            </div>
          </div>
        </el-tooltip>

        <div v-if="workflows.length === 0 && !loading && !collapsed" class="empty-state">
          暂无可用的智能助手
        </div>
        <div v-else-if="workflows.length === 0 && !loading && collapsed"
          class="empty-state-collapsed" title="暂无可用的智能助手">—</div>
        <div v-if="loading" class="loading-state">
          <div class="spinner"></div>加载中...
        </div>
      </div>

      <div class="sidebar-footer">
        <WeatherWidget :mini="collapsed" />
      </div>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import WeatherWidget from '../../common/WeatherWidget.vue'

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
/* === Layout === */
.sidebar {
  width: 320px;
  min-width: 320px;
  background: transparent;
  padding: 0 12px 12px;
  display: flex;
  flex-direction: column;
  transition: width 0.2s ease, min-width 0.2s ease, padding 0.2s ease;
}
.sidebar.collapsed { width: 88px; min-width: 88px; padding: 0 8px 12px; }

.sidebar-panel {
  margin-top: 12px;
  height: calc(100% - 12px);
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  box-shadow: 0 8px 24px rgba(17, 24, 39, 0.06);
  padding: 18px 16px;
  display: flex;
  flex-direction: column;
  min-height: 0;
}
.sidebar.collapsed .sidebar-panel { padding: 10px 8px; }
.sidebar-panel.pulse { animation: sidebarPulse 0.9s ease-in-out; }

@keyframes sidebarPulse {
  0% { box-shadow: 0 8px 24px rgba(17,24,39,0.06); border-color: #e5e7eb; }
  45% { box-shadow: 0 12px 34px rgba(59,130,246,0.22); border-color: rgba(59,130,246,0.55); }
  100% { box-shadow: 0 8px 24px rgba(17,24,39,0.06); border-color: #e5e7eb; }
}

/* === Top: Brand + Collapse === */
.sidebar-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 18px;
}
.sidebar.collapsed .sidebar-top { justify-content: center; margin-bottom: 12px; }

.brand-area { flex: 1; min-width: 0; }
.brand-row {
  display: flex;
  align-items: center;
  gap: 10px;
}
.brand-name {
  font-size: 18px;
  font-weight: 800;
  background: linear-gradient(135deg, #3b82f6, #1d4ed8);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.3px;
  line-height: 1;
}
.brand-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 11px;
  color: #10b981;
  font-weight: 500;
  background: #ecfdf5;
  padding: 2px 8px;
  border-radius: 999px;
}
.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #10b981;
  animation: dotPulse 2s ease-in-out infinite;
}
@keyframes dotPulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}

.collapse-btn {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
  background: #ffffff;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s ease, border-color 0.15s ease;
  flex-shrink: 0;
  margin-top: -2px;
}
.collapse-btn:hover { background: #f3f4f6; border-color: #d1d5db; }
.collapse-icon { font-size: 16px; color: #6b7280; }
</style>

<style scoped>
/* === Search Bar === */
.search-bar {
  margin-bottom: 12px;
}
.search-inner {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 7px 12px;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.search-inner:focus-within {
  border-color: #93c5fd;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
  background: #ffffff;
}
.search-icon {
  color: #94a3b8;
  flex-shrink: 0;
  transition: color 0.2s;
}
.search-inner:focus-within .search-icon { color: #3b82f6; }
.search-input {
  flex: 1;
  border: none;
  outline: none;
  background: transparent;
  font-size: 13px;
  color: #334155;
  line-height: 1.4;
  min-width: 0;
}
.search-input::placeholder { color: #cbd5e1; }
.search-clear {
  border: none;
  background: none;
  color: #94a3b8;
  cursor: pointer;
  font-size: 12px;
  padding: 0 2px;
  line-height: 1;
  transition: color 0.15s;
}
.search-clear:hover { color: #64748b; }

/* === Filter Pills === */
.filter-pills {
  display: flex;
  gap: 6px;
  margin-bottom: 20px;
  overflow-x: auto;
  padding-bottom: 4px;
  scrollbar-width: thin;
  scrollbar-color: #d1d5db transparent;
}
.filter-pills::-webkit-scrollbar { height: 3px; }
.filter-pills::-webkit-scrollbar-track { background: transparent; }
.filter-pills::-webkit-scrollbar-thumb {
  background: #d1d5db;
  border-radius: 3px;
}
.filter-pills::-webkit-scrollbar-thumb:hover { background: #9ca3af; }

.pill {
  padding: 5px 14px;
  border: none;
  border-radius: 999px;
  background: #f1f5f9;
  color: #64748b;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.2s ease;
  line-height: 1.4;
}
.pill:hover {
  background: #e2e8f0;
  color: #475569;
}
.pill.active {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: #ffffff;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

/* === Workflow List === */
.workflow-list { flex: 1; overflow-y: auto; padding-right: 2px; }

.workflow-item {
  padding: 10px 12px;
  border-radius: 12px;
  cursor: pointer;
  margin-bottom: 4px;
  transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  align-items: center;
  gap: 12px;
  border: 1px solid transparent;
  position: relative;
}
.workflow-item:hover { background: #f8fafc; }
.workflow-item.active { background: #eff6ff; border-color: rgba(59,130,246,0.15); }
.workflow-item.active::before {
  content: '';
  position: absolute;
  left: 0; top: 10px; bottom: 10px;
  width: 3px;
  background-color: #3b82f6;
  border-radius: 0 3px 3px 0;
}

.wf-avatar {
  width: 38px;
  height: 38px;
  border-radius: 10px;
  background: #ffffff;
  color: #3b82f6;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 15px;
  flex: 0 0 auto;
  box-shadow: 0 2px 6px rgba(59,130,246,0.08);
  border: 1px solid #eef2f6;
  transition: all 0.2s;
}
.workflow-item:hover .wf-avatar {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(59,130,246,0.12);
  border-color: #dbeafe;
}
.workflow-item.active .wf-avatar {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: #ffffff;
  box-shadow: 0 4px 12px rgba(37,99,235,0.2);
  border-color: transparent;
}

.wf-meta { min-width: 0; flex: 1; }
.sidebar.collapsed .wf-meta { display: none; }
.sidebar.collapsed .workflow-item {
  justify-content: center;
  padding: 8px 6px;
  gap: 0;
}
.sidebar.collapsed .workflow-list { padding-right: 0; }
.sidebar.collapsed .wf-avatar { width: 36px; height: 36px; border-radius: 10px; font-size: 14px; }
.sidebar.collapsed .workflow-item.active .wf-avatar {
  box-shadow: 0 0 0 3px rgba(59,130,246,0.25), 0 6px 16px rgba(17,24,39,0.12);
}

.wf-name {
  font-size: 13.5px;
  font-weight: 600;
  color: #334155;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  line-height: 1.3;
}
.workflow-item.active .wf-name { color: #1e40af; }

.wf-desc {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 2px;
  display: -webkit-box;
  line-clamp: 1;
  -webkit-line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
}
.workflow-item:hover .wf-desc { color: #64748b; }
.workflow-item.active .wf-desc { color: #60a5fa; }

/* === Empty & Loading === */
.empty-state, .loading-state {
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
@keyframes spin { to { transform: rotate(360deg); } }

/* === Footer === */
.sidebar-footer {
  flex-shrink: 0;
  margin: 8px -16px -18px;
  padding: 18px 18px 20px;
  background: linear-gradient(180deg, transparent 0%, #f0f7ff 100%);
  border-radius: 0 0 14px 14px;
}
.sidebar.collapsed .sidebar-footer {
  margin: 8px -8px -10px;
  padding: 14px 8px 16px;
}
</style>

<style>
.agent-tooltip {
  max-width: 280px;
  padding: 10px 14px !important;
  border-radius: 10px !important;
  box-shadow: 0 8px 24px rgba(0,0,0,0.12) !important;
  border: 1px solid #e5e7eb !important;
  font-size: 13px !important;
  line-height: 1.5 !important;
  color: #374151 !important;
  background: #ffffff !important;
}
.agent-tooltip .el-popper__arrow::before {
  border: 1px solid #e5e7eb !important;
  background: #ffffff !important;
}
</style>
