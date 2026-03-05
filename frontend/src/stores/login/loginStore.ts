/**
 * @module LoginStore
 * @description 登录状态管理 - 处理登录流程和认证状态
 * @author AI Assistant
 * @since 2024
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import { LoginApi } from '../../services/login/api'
import type { LoginRequest } from '../../services/login/types'
import { useUserStore } from './user'

export const useLoginStore = defineStore('login', () => {
  const loading = ref(false)
  const error = ref<string | null>(null)

  const login = async (credentials: LoginRequest) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await LoginApi.login(credentials)
      
      // login() 使用原生 fetch，后端返回标准格式 { success, code, message, data }
      // 手动解包 data 层
      const userInfo = (response as any).data ?? (response as any).user_info ?? response
      
      // 保存用户信息到localStorage
      LoginApi.saveUserInfo(userInfo)
      
      // 设置UserStore
      const userStore = useUserStore()
      userStore.setUserInfo(userInfo)
      
      // 验证HttpOnly Cookie（开发环境）
      if (import.meta.env.DEV) {
        const hasTokenInCookie = document.cookie.includes('access_token')
        console.log('🔒 HttpOnly Cookie验证:', hasTokenInCookie ? '❌ 失败（Cookie可被JS读取）' : '✅ 成功（Cookie已设置且HttpOnly）')
      }
      
      return response
    } catch (err: any) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    loading,
    error,
    login,
    clearError
  }
})