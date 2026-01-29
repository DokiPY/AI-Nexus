<template>
  <div class="login-card">
    <LoginHeader />
    <LoginFormContent 
      :loading="loading"
      @submit="$emit('submit', $event)"
      @contact-admin="$emit('contact-admin')"
    />
    <LoginFooter @contact-admin="$emit('contact-admin')" />
  </div>
</template>

<script setup lang="ts">
import LoginHeader from './LoginHeader.vue'
import LoginFormContent from './LoginFormContent.vue'
import LoginFooter from './LoginFooter.vue'
import type { LoginRequest } from '../../services/login/types'

defineProps<{
  loading: boolean
}>()

defineEmits<{
  submit: [form: LoginRequest]
  'contact-admin': []
}>()
</script>

<style scoped>
.login-card {
  width: 420px;
  padding: 48px 40px;
  background: rgba(255,255,255,0.95);
  border-radius: 20px;
  border: 1px solid #e5e7eb;
  box-shadow:
    0 24px 48px rgba(0,0,0,0.08),
    0 1px 0 rgba(255,255,255,0.6) inset;
}
</style>
