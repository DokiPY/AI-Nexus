<template>
  <el-form
    ref="formRef"
    :model="formData"
    :rules="rules"
    class="login-form"
    size="large"
    @keyup.enter="handleSubmit"
  >
    <el-form-item prop="username">
      <el-input
        v-model="formData.username"
        placeholder="请输入账号 / 企业邮箱"
        :prefix-icon="User"
      />
    </el-form-item>

    <el-form-item prop="password">
      <el-input
        v-model="formData.password"
        type="password"
        placeholder="请输入密码"
        show-password
        :prefix-icon="Lock"
      />
    </el-form-item>

    <div class="capability-hint">
      ✓ 登录后将自动启用您已订阅的 AI Agent Workflow
    </div>

    <div class="form-footer">
      <div class="security-hint">
        <el-icon><Lock /></el-icon>
        <span>安全加密连接</span>
      </div>
      <span class="forgot-btn" @click="$emit('contact-admin')">忘记密码?</span>
    </div>

    <el-button
      type="primary"
      :loading="loading"
      class="submit-btn"
      @click="handleSubmit"
    >
      {{ loading ? '正在连接系统...' : '进入 Agent 控制台' }}
    </el-button>
  </el-form>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { User, Lock } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import type { LoginRequest } from '../../services/login/types'

defineProps<{
  loading: boolean
}>()

const emit = defineEmits<{
  submit: [form: LoginRequest]
  'contact-admin': []
}>()

const formRef = ref<FormInstance>()

const formData = reactive<LoginRequest>({
  username: '',
  password: ''
})

const rules: FormRules = {
  username: [{ required: true, message: '请输入账号或邮箱', trigger: 'blur' }],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少 6 位', trigger: 'blur' }
  ]
}

const handleSubmit = async () => {
  if (!formRef.value) return
  await formRef.value.validate((valid) => {
    if (valid) {
      emit('submit', formData)
    }
  })
}
</script>

<style scoped>
.login-form :deep(.el-input__wrapper) {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
}

.login-form :deep(.el-input__wrapper.is-focus) {
  border-color: #0f766e;
  box-shadow: 0 0 0 3px #e6f4f1;
}

.login-form :deep(.el-form-item__error) {
  color: #dc2626;
  font-size: 12px;
}

.capability-hint {
  font-size: 12px;
  color: #0f766e;
  opacity: 0.8;
  text-align: center;
  margin-bottom: 12px;
}

.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.security-hint {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #64748b;
  opacity: 0.8;
}

.security-hint .el-icon {
  font-size: 14px;
}

.forgot-btn {
  font-size: 13px;
  color: #0f766e;
  cursor: pointer;
}

.submit-btn {
  width: 100%;
  height: 48px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 600;
  background: #1f3a5f;
  border: none;
}

.submit-btn:hover {
  background: #162c47;
}
</style>
