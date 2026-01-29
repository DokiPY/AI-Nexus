<template>
  <el-dialog
    class="company-form-dialog"
    :model-value="visible"
    :title="isEdit ? '编辑公司' : '新增公司'"
    width="500px"
    destroy-on-close
    append-to-body
    @update:model-value="$emit('update:visible', $event)"
  >
    <el-form :model="form" label-position="top" class="form">
      <el-form-item label="公司名称" required>
        <el-input v-model="form.name" placeholder="请输入公司名称" />
      </el-form-item>
      <el-form-item label="域名">
        <el-input v-model="form.domain" placeholder="example.com" />
      </el-form-item>
      <el-form-item label="状态">
        <div class="switch-row">
          <el-switch v-model="form.is_active" />
          <span class="switch-tip">{{ form.is_active ? '启用' : '禁用' }}</span>
        </div>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="$emit('update:visible', false)">取消</el-button>
      <el-button type="primary" @click="$emit('save')" round>
        {{ isEdit ? '保存修改' : '创建公司' }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
interface CompanyForm {
  name: string
  domain: string
  is_active: boolean
}

defineProps<{
  visible: boolean
  form: CompanyForm
  isEdit: boolean
}>()

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

.switch-row {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.switch-tip {
  color: #64748b;
  font-size: 0.9rem;
}
</style>
