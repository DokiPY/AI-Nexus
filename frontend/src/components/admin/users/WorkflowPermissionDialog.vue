<template>
  <!-- 权限管理对话框 -->
  <el-dialog
    class="workflow-permission-dialog"
    :model-value="visible"
    :title="`管理工作流权限 - ${selectedUser?.username}`"
    width="600px"
    destroy-on-close
    append-to-body
    @update:model-value="$emit('update:visible', $event)"
  >
    <div class="summary">
      <span class="summary-title">已选择</span>
      <el-tag type="primary" round effect="light">{{ selectedWorkflows?.length || 0 }}</el-tag>
      <span class="summary-sub">个工作流</span>
    </div>

    <div class="workflow-list">
      <el-checkbox-group
        :model-value="selectedWorkflows"
        @update:model-value="$emit('update:selectedWorkflows', $event)"
      >
        <div
          v-for="workflow in workflows"
          :key="workflow.id"
          class="workflow-item"
          :class="{ checked: selectedWorkflows?.includes(workflow.id) }"
        >
          <el-checkbox :label="workflow.id">
            <div class="workflow-info">
              <span class="workflow-icon">{{ workflow.icon }}</span>
              <div class="workflow-text">
                <div class="workflow-name">{{ workflow.name }}</div>
                <div class="workflow-desc">{{ workflow.description }}</div>
              </div>
            </div>
          </el-checkbox>
        </div>
      </el-checkbox-group>
    </div>
    <template #footer>
      <el-button @click="$emit('update:visible', false)">取消</el-button>
      <el-button type="primary" @click="$emit('save')" round>保存权限</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import type { User, AdminWorkflow } from '../../../services'

defineProps<{
  visible: boolean
  selectedUser: User | null
  workflows: AdminWorkflow[]
  selectedWorkflows: number[]
}>()

defineEmits<{
  'update:visible': [value: boolean]
  'update:selectedWorkflows': [value: number[]]
  save: []
}>()
</script>

<style scoped>
.summary {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
  color: #64748b;
}

.summary-title {
  font-weight: 700;
}

.summary-sub {
  font-size: 0.9rem;
}

.workflow-list {
  max-height: 420px;
  overflow: auto;
  padding-right: 4px;
}

.workflow-item {
  margin-bottom: 12px;
  padding: 12px 14px;
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 12px;
  background: rgba(248, 250, 252, 0.75);
  transition: border-color 0.2s ease, background 0.2s ease, transform 0.2s ease;
}

.workflow-item:hover {
  border-color: rgba(59, 130, 246, 0.25);
  background: rgba(255, 255, 255, 0.85);
  transform: translateY(-1px);
}

.workflow-item.checked {
  border-color: rgba(59, 130, 246, 0.35);
  background: rgba(59, 130, 246, 0.06);
}

.workflow-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.workflow-icon {
  font-size: 24px;
}

.workflow-text {
  min-width: 0;
}

.workflow-name {
  font-weight: 700;
  color: #334155;
}

.workflow-desc {
  font-size: 12px;
  color: #64748b;
  margin-top: 2px;
}

.workflow-list :deep(.el-checkbox) {
  width: 100%;
}

.workflow-list :deep(.el-checkbox__label) {
  width: 100%;
}
</style>