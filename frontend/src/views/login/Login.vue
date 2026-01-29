<template>
  <div class="login-container">
    <LoginCard 
      :loading="loading"
      @submit="handleLogin"
      @contact-admin="showContactAdmin"
    />
    
    <div class="copyright">
      © 2025 Agent Nexus · Powered by n8n Workflow
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { LoginCard } from '@/components'
import { LoginApi } from '../../services/login/api'
import type { LoginRequest } from '../../services/login/types'
import { useLoginStore, useUserStore } from '../../stores'

const router = useRouter()
const loginStore = useLoginStore()
const userStore = useUserStore()
const loading = ref(false)

const showContactAdmin = () => {
  ElMessage({
    message: '请联系管理员：admin@company.com',
    type: 'success',
    duration: 4000
  })
}

const handleLogin = async (form: LoginRequest) => {
  loading.value = true
  
  try {
    // 1. 登录（Cookie自动设置）
    await loginStore.login(form)
    
    // 2. 获取用户信息
    const userInfo = LoginApi.getUserInfo()
    if (!userInfo) {
      throw new Error('获取用户信息失败')
    }
    userStore.setUserInfo(userInfo)
    
    // 3. 根据用户角色跳转
    if (userInfo.role === 'admin') {
      router.push('/admin')
    } else {
      router.push('/workflows')
    }
  } catch (error: any) {
    userStore.clearUserData()
    const errorMsg = error.message || '登录失败，请稍后重试'
    ElMessage.error(errorMsg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  width: 100vw;
  height: 100vh;
  background:
    radial-gradient(
      circle at 50% 45%,
      rgba(255, 255, 255, 0.90),
      rgba(249, 248, 246, 0.86) 32%,
      rgba(243, 244, 246, 0.80) 55%,
      transparent 72%
    ),
    radial-gradient(
      circle at 20% 25%,
      rgba(14, 116, 109, 0.07),
      transparent 48%
    ),
    radial-gradient(
      circle at 80% 78%,
      rgba(59, 78, 110, 0.06),
      transparent 52%
    ),
    #f4f5f3;

  display: flex;
  justify-content: center;
  align-items: center;
  font-family: 'Inter', -apple-system, sans-serif;
  position: relative;
}

.login-container::after {
  content: '';
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 400 400' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
  opacity: 0.015;
}

.copyright {
  position: absolute;
  bottom: 20px;
  font-size: 12px;
  color: #6b7280;
  opacity: 0.6;
}
</style>
