<template>
  <el-dialog
    class="workflow-form-dialog"
    :model-value="visible"
    @update:model-value="$emit('update:visible', $event)"
    :title="isEdit ? '编辑工作流' : '新建工作流'"
    width="500px"
    destroy-on-close
    append-to-body
  >
    <el-form :model="form" label-position="top" class="form">
      <el-form-item label="工作流名称" required>
        <el-input v-model="form.name" placeholder="请输入工作流名称" />
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="form.description" type="textarea" :rows="3" placeholder="请输入工作流描述" />
      </el-form-item>
      <el-form-item label="分类" required>
        <el-select
          v-model="form.category"
          placeholder="请选择或输入新分类"
          style="width: 100%"
          filterable
          allow-create
          default-first-option
        >
          <el-option
            v-for="cat in categories"
            :key="cat"
            :label="cat"
            :value="cat"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="请求方式" required>
        <el-select v-model="form.http_method" placeholder="请选择请求方式" style="width: 100%">
          <el-option label="POST" value="POST" />
          <el-option label="GET" value="GET" />
          <el-option label="PUT" value="PUT" />
          <el-option label="DELETE" value="DELETE" />
        </el-select>
      </el-form-item>
      <el-form-item label="N8N Webhook URL" required>
        <el-input v-model="form.n8n_webhook_url" placeholder="https://your-n8n.com/webhook/..." />
      </el-form-item>
      <el-form-item label="流式响应">
        <el-switch
          v-model="form.stream_enabled"
          active-text="开启"
          inactive-text="关闭"
          inline-prompt
        />
        <span class="form-tip">N8N 使用 Respond to Webhook 一次性返回时请关闭</span>
      </el-form-item>
      <el-form-item label="图标">
        <el-input v-model="form.icon" placeholder="输入 emoji 或图标" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="$emit('update:visible', false)">取消</el-button>
      <el-button type="primary" @click="$emit('save')" round>
        {{ isEdit ? '保存修改' : '创建工作流' }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
interface WorkflowForm {
  name: string
  description: string
  category: string
  http_method: string
  n8n_webhook_url: string
  stream_enabled: boolean
  icon: string
}

interface WorkflowFormDialogProps {
  visible: boolean
  form: WorkflowForm
  isEdit: boolean
  categories: string[]
}

defineProps<WorkflowFormDialogProps>()

defineEmits<{
  'update:visible': [value: boolean]
  save: []
}>()
</script>

<style scoped>
.form :deep(.el-form-item__label) {
  color: #64748b;
  font-weight: 700;
}

.form :deep(.el-input__wrapper),
.form :deep(.el-select__wrapper) {
  border-radius: 12px;
}

.form-tip {
  font-size: 12px;
  color: #94a3b8;
  margin-left: 12px;
}
</style>
