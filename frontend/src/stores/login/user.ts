/**
 * @module UserStore
 * @description 用户信息状态管理 - 处理用户信息、权限和登录状态
 * @author AI Assistant
 * @since 2024
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { UserInfo } from '../../services/login/types'
import { LoginApi } from '../../services/login/api'

export const useUserStore = defineStore('user', () => {

  // 初始化时从 LoginApi 加载用户信息
  const userInfo = ref<UserInfo | null>(LoginApi.getUserInfo())
  const loading = ref(false)

  const isLoggedIn = computed(() => {
    return !!LoginApi.getUserInfo()
  })

  const setUserInfo = (info: UserInfo) => {
    userInfo.value = info
  }

  const clearUserData = () => {
    userInfo.value = null
    LoginApi.clearUserInfo()
  }

  const logout = async () => {
    await LoginApi.logout()
    clearUserData()
  }

  return {
    userInfo,
    loading,
    isLoggedIn,
    setUserInfo,
    clearUserData,
    logout
  }
})