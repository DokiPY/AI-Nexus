/**
 * @module AuthUtils
 * @description 认证工具函数 - 处理自动登出和token刷新
 * @author AI Assistant
 * @since 2024
 */

import { useUserStore } from '../stores'
import { useRouter } from 'vue-router'

// 自动登出定时器
let autoLogoutTimer: ReturnType<typeof setTimeout> | null = null

/**
 * 设置自动登出定时器
 * @param minutes 分钟数，默认30分钟无操作自动登出
 */
export function setupAutoLogout(minutes: number = 30) {
  clearAutoLogout()
  
  autoLogoutTimer = setTimeout(() => {
    const userStore = useUserStore()
    const router = useRouter()
    
    userStore.logout()
    router.push('/login')
    alert('长时间未操作，已自动退出登录')
  }, minutes * 60 * 1000)
}

/**
 * 清除自动登出定时器
 */
export function clearAutoLogout() {
  if (autoLogoutTimer) {
    clearTimeout(autoLogoutTimer)
    autoLogoutTimer = null
  }
}

/**
 * 重置自动登出定时器（用户有操作时调用）
 */
export function resetAutoLogout() {
  const userStore = useUserStore()
  if (userStore.isLoggedIn) {
    setupAutoLogout()
  }
}

/**
 * 手动登出
 */
export function logout() {
  const userStore = useUserStore()
  const router = useRouter()
  
  clearAutoLogout()
  userStore.logout()
  router.push('/login')
}

/**
 * 监听用户活动，重置自动登出定时器
 */
export function setupActivityListener() {
  const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click']
  
  const resetTimer = () => {
    resetAutoLogout()
  }
  
  events.forEach(event => {
    document.addEventListener(event, resetTimer, true)
  })
  
  // 返回清理函数
  return () => {
    events.forEach(event => {
      document.removeEventListener(event, resetTimer, true)
    })
  }
}