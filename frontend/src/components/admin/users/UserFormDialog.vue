<template>
  <!-- 新增/编辑用户对话框 -->
  <el-dialog
    class="user-form-dialog"
    :model-value="visible"
    :title="isEdit ? '编辑用户' : '新增用户'"
    width="500px"
    destroy-on-close
    append-to-body
    @update:model-value="$emit('update:visible', $event)"
  >
    <el-form :model="form" label-position="top" class="form">
      <el-form-item label="用户名" required>
        <el-input v-model="form.username" :disabled="isEdit" placeholder="请输入用户名" />
      </el-form-item>
      <el-form-item label="邮箱">
        <el-input v-model="form.email" type="email" placeholder="name@company.com" />
      </el-form-item>
      <el-form-item label="密码" required v-if="!isEdit">
        <el-input v-model="form.password" type="password" show-password placeholder="设置登录密码" />
      </el-form-item>
      <el-form-item label="角色" required>
        <el-select v-model="form.role" style="width: 100%">
          <el-option label="普通用户" value="user" />
          <el-option label="管理员" value="admin" />
        </el-select>
      </el-form-item>
      <el-form-item label="公司" required>
        <el-select v-model="form.company_name" style="width: 100%">
          <el-option
            v-for="company in companies"
            :key="company.id"
            :label="company.name"
            :value="company.name"
          />
        </el-select>
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
        {{ isEdit ? '保存修改' : '创建用户' }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import type { AdminCompany } from '../../../services'

interface UserForm {
  username: string
  email: string
  password: string
  role: string
  company_name: string
  is_active: boolean
}

defineProps<{
  visible: boolean
  form: UserForm
  companies: AdminCompany[]
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