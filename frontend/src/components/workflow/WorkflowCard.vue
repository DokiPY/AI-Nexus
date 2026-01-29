<!-- 创建工作流卡片组件，包含图标、状态、标题、描述和操作按钮 -->
<template>
  <div 
    class="workflow-card fade-in-up"
    :style="{ animationDelay: `${animationDelay}ms` }"
    @click="handleClick"
  >
    <div class="card-glow"></div>
    
    <div class="card-header">
      <div class="agent-icon" :style="{ background: workflow.color }">
        {{ workflow.icon }}
      </div>
      <div class="status-badge" :class="statusClass">
        <span class="dot"></span> 
        {{ statusText }}
      </div>
    </div>

    <div class="card-body">
      <h3>{{ workflow.name }}</h3>
      <p>{{ workflow.description }}</p>
    </div>

    <div class="card-footer">
      <div class="tags">
        <span class="tag">{{ workflow.category }}</span>
      </div>
      <button class="action-btn">
        进入对话 <span class="arrow">→</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Workflow {
  id: number | string
  name: string
  description: string
  icon: string
  color?: string
  category: string
  // 兼容后端/前端两种字段形态，避免 `WorkflowGrid.vue` 传入时报模板类型错误
  status?: 'active' | 'maintenance' | 'available' | 'no_permission'
  is_active?: boolean
  has_permission?: boolean
}

interface Props {
  workflow: Workflow
  animationDelay?: number
}

const props = withDefaults(defineProps<Props>(), {
  animationDelay: 0
})

const emit = defineEmits<{
  click: [workflow: Workflow]
}>()

const handleClick = () => {
  emit('click', props.workflow)
}

const statusInfo = computed(() => {
  const wf = props.workflow
  const hasPermission = wf.has_permission !== false && wf.status !== 'no_permission'
  if (!hasPermission) return { cls: 'no_permission', text: '无权限' } as const

  const isRunning =
    wf.is_active === true ||
    wf.status === 'active' ||
    wf.status === 'available'

  return isRunning
    ? ({ cls: 'active', text: '运行中' } as const)
    : ({ cls: 'maintenance', text: '维护中' } as const)
})

const statusClass = computed(() => statusInfo.value.cls)
const statusText = computed(() => statusInfo.value.text)
</script>

<style scoped>
.workflow-card {
  background: rgba(255, 255, 255, 0.9);
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 20px;
  padding: 24px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex; flex-direction: column;
  backdrop-filter: blur(10px);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
}

.workflow-card:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.95);
  border-color: rgba(59, 130, 246, 0.2);
  box-shadow: 0 20px 40px -5px rgba(59, 130, 246, 0.1);
}
.workflow-card:hover .action-btn { color: #3b82f6; }
.workflow-card:hover .arrow { transform: translateX(5px); }
.workflow-card:hover .card-glow { opacity: 1; }

.card-glow {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  background: radial-gradient(circle at top right, rgba(59, 130, 246, 0.05), transparent 60%);
  opacity: 0; transition: opacity 0.4s; pointer-events: none;
}

.card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; }
.agent-icon {
  width: 56px; height: 56px; border-radius: 16px; display: flex; align-items: center; justify-content: center; font-size: 1.8rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.status-badge {
  font-size: 0.75rem; padding: 4px 10px; border-radius: 12px; display: flex; align-items: center; gap: 6px; font-weight: 500;
}
.status-badge.active { background: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.2); }
.status-badge.maintenance { background: rgba(245, 158, 11, 0.1); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.2); }
.status-badge.no_permission { background: rgba(239, 68, 68, 0.1); color: #ef4444; border: 1px solid rgba(239, 68, 68, 0.2); }
.dot { width: 6px; height: 6px; border-radius: 50%; background: currentColor; }
.status-badge.active .dot { box-shadow: 0 0 5px #34d399; }

.card-body h3 { font-size: 1.25rem; margin-bottom: 10px; font-weight: 600; color: #1e293b; }
.card-body p { color: #64748b; font-size: 0.95rem; line-height: 1.5; margin-bottom: 24px; flex-grow: 1; }

.card-footer {
  display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(0, 0, 0, 0.06); padding-top: 16px; margin-top: auto;
}
.tag { font-size: 0.8rem; color: #475569; background: rgba(248, 250, 252, 0.8); padding: 4px 8px; border-radius: 6px; border: 1px solid rgba(0, 0, 0, 0.04); }

.action-btn {
  background: none; border: none; color: #64748b; font-size: 0.9rem; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 6px; transition: color 0.3s;
}
.arrow { transition: transform 0.3s; }

.fade-in-up { opacity: 0; animation: fadeInUp 0.6s ease-out forwards; transform: translateY(20px); }

@keyframes fadeInUp { to { opacity: 1; transform: translateY(0); } }
</style>