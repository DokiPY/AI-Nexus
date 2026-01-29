<!-- 工作流网格组件，包含卡片列表、骨架屏和空状态 -->
<template>
  <div>
    <!-- 工作流卡片网格 -->
    <div class="workflow-grid" v-if="!loading">
      <WorkflowCard
        v-for="(workflow, index) in workflows"
        :key="workflow.id"
        :workflow="workflow"
        :animation-delay="index * 50 + 300"
        @click="$emit('workflowClick', workflow)"
      />
    </div>

    <!-- Loading 骨架屏 -->
    <div class="workflow-grid" v-else>
      <div class="skeleton-card" v-for="n in 6" :key="n"></div>
    </div>

    <!-- 空状态 -->
    <div v-if="!loading && workflows.length === 0" class="empty-state">
      <div class="empty-icon">📂</div>
      <h3>未找到相关工作流</h3>
      <p>请尝试更换搜索关键词或联系管理员开通权限。</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import WorkflowCard from './WorkflowCard.vue'

interface Workflow {
  id: number
  name: string
  description: string
  icon: string
  color?: string
  category: string
  is_active: boolean
  has_permission: boolean
  status: 'available' | 'no_permission'
  n8n_webhook_url?: string
}

interface Props {
  workflows: Workflow[]
  loading: boolean
}

defineProps<Props>()

defineEmits<{
  workflowClick: [workflow: Workflow]
}>()
</script>

<style scoped>
.workflow-grid {
  display: grid; 
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); 
  gap: 30px;
}

.skeleton-card { 
  height: 280px; 
  background: rgba(248, 250, 252, 0.8); 
  border: 1px solid rgba(0, 0, 0, 0.04);
  border-radius: 20px; 
  animation: pulse 1.5s infinite; 
}

.empty-state { 
  grid-column: 1 / -1; 
  text-align: center; 
  padding: 60px; 
  color: #64748b; 
}
.empty-state h3 {
  color: #334155;
  margin: 16px 0 8px 0;
}
.empty-icon { 
  font-size: 3rem; 
  margin-bottom: 16px; 
  opacity: 0.5; 
}

@keyframes pulse { 
  0% { opacity: 0.6; } 
  50% { opacity: 0.3; } 
  100% { opacity: 0.6; } 
}
</style>