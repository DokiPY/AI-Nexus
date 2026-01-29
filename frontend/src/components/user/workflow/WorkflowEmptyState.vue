<template>
  <div class="empty">
    <div v-if="!loading && workflows.length === 0" class="empty-shell">
      <section class="empty-hero">
        <div class="empty-mark">
          <div class="empty-mark-inner"></div>
        </div>
        <div class="empty-head">
          <div class="empty-kicker">Workflow Console</div>
          <div class="empty-title">选择一个 Workflow 开始</div>
          <div class="empty-subtitle">
            从左侧列表选择后，即可开始对话并执行任务；也可以直接搜索想要的 Workflow。
          </div>
        </div>

        <div class="empty-actions">
          <el-button type="primary" @click="$emit('open-search')">
            选择 / 搜索 Workflow
          </el-button>
          <el-button v-if="sidebarCollapsed" @click="$emit('toggle-sidebar')">
            展开侧边栏
          </el-button>
        </div>

        <div class="empty-tips">
          <div class="tip">
            <div class="tip-title">更快开始</div>
            <div class="tip-desc">输入一句话即可：例如"帮我筛选本周候选人简历并给出建议"</div>
          </div>
          <div class="tip">
            <div class="tip-title">保持上下文</div>
            <div class="tip-desc">同一个 Workflow 内会持续对话，方便迭代任务</div>
          </div>
        </div>
      </section>

      <aside class="empty-picks">
        <div class="picks-title">快速开始</div>
        <div class="picks-subtitle">点击一个常用 Workflow 立即进入对话</div>

        <div v-if="loading" class="picks-loading">
          <div class="skeleton"></div>
          <div class="skeleton"></div>
          <div class="skeleton"></div>
        </div>

        <div v-else class="picks-list">
          <button
            v-for="wf in workflows.slice(0, 3)"
            :key="wf.id"
            class="pick-item"
            type="button"
            @click="$emit('select-workflow', wf)"
          >
            <div class="pick-avatar">
              {{ (wf?.name?.[0] || 'W').toUpperCase() }}
            </div>
            <div class="pick-meta">
              <div class="pick-name">{{ wf.name }}</div>
              <div class="pick-desc">{{ wf.description }}</div>
            </div>
          </button>

          <div v-if="workflows.length === 0" class="picks-empty">
            暂无可用 Workflow，请先创建或等待同步完成。
          </div>
        </div>
      </aside>
    </div>
    <div v-else class="empty-minimal">
      <div class="mini-spinner"></div>
      <div class="mini-text">
        {{ loading ? '加载中…' : '正在打开默认 Workflow…' }}
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps<{
  loading: boolean
  workflows: any[]
  sidebarCollapsed: boolean
}>()

defineEmits<{
  'open-search': []
  'toggle-sidebar': []
  'select-workflow': [workflow: any]
}>()
</script>

<style scoped>
.empty {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.empty-minimal {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #6b7280;
  font-size: 13px;
}

.mini-spinner {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 2px solid #e5e7eb;
  border-top-color: #3b82f6;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.mini-text {
  line-height: 1.4;
}

.empty-shell {
  width: min(980px, 100%);
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 16px;
  align-items: start;
}

.empty-hero,
.empty-picks {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(17, 24, 39, 0.06);
}

.empty-hero {
  padding: 22px 20px;
}

.empty-picks {
  padding: 18px 16px;
}

.empty-mark {
  width: 44px;
  height: 44px;
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(59, 130, 246, 0.18), rgba(31, 58, 95, 0.12));
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.empty-mark-inner {
  width: 22px;
  height: 22px;
  border-radius: 10px;
  background: linear-gradient(135deg, #1f3a5f, #3b82f6);
}

.empty-kicker {
  font-size: 12px;
  color: #6b7280;
  font-weight: 600;
}

.empty-title {
  margin-top: 6px;
  font-size: 18px;
  font-weight: 800;
  color: #111827;
}

.empty-subtitle {
  margin-top: 8px;
  font-size: 13px;
  color: #6b7280;
  line-height: 1.6;
}

.empty-actions {
  margin-top: 14px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.empty-tips {
  margin-top: 16px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.tip {
  padding: 12px;
  border-radius: 14px;
  background: #f8fafc;
  border: 1px solid #eef2f7;
}

.tip-title {
  font-size: 12px;
  font-weight: 700;
  color: #111827;
}

.tip-desc {
  margin-top: 6px;
  font-size: 12px;
  color: #6b7280;
  line-height: 1.55;
}

.picks-title {
  font-size: 14px;
  font-weight: 800;
  color: #111827;
}

.picks-subtitle {
  margin-top: 6px;
  font-size: 12px;
  color: #6b7280;
  line-height: 1.5;
}

.picks-list {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.pick-item {
  text-align: left;
  width: 100%;
  border: 1px solid #eef2f7;
  background: #ffffff;
  border-radius: 14px;
  padding: 12px;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  cursor: pointer;
  transition: background 0.15s ease, border-color 0.15s ease, transform 0.15s ease;
}

.pick-item:hover {
  background: #f8fafc;
  border-color: #dbeafe;
  transform: translateY(-1px);
}

.pick-avatar {
  width: 34px;
  height: 34px;
  border-radius: 12px;
  background: linear-gradient(135deg, #1f3a5f, #3b82f6);
  color: #ffffff;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 14px;
  flex: 0 0 auto;
}

.pick-meta {
  min-width: 0;
  flex: 1;
}

.pick-name {
  font-size: 13px;
  font-weight: 800;
  color: #111827;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.pick-desc {
  margin-top: 4px;
  font-size: 12px;
  color: #6b7280;
  display: -webkit-box;
  line-clamp: 2;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.picks-loading {
  margin-top: 12px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.skeleton {
  height: 58px;
  border-radius: 14px;
  background: linear-gradient(90deg, #f3f4f6 0%, #e5e7eb 50%, #f3f4f6 100%);
  background-size: 200% 100%;
  animation: shimmer 1.2s ease-in-out infinite;
}

@keyframes shimmer {
  0% { background-position: 0% 0%; }
  100% { background-position: 200% 0%; }
}

.picks-empty {
  margin-top: 10px;
  font-size: 12px;
  color: #9ca3af;
}

@media (max-width: 980px) {
  .empty-shell {
    grid-template-columns: 1fr;
  }
  .empty-tips {
    grid-template-columns: 1fr;
  }
}
</style>
