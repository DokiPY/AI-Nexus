/**
 * @module RouterGuards
 * @description 路由守卫 - 处理登录验证和权限控制
 */

import type { Router } from 'vue-router'
import { LoginApi } from '../services/login/api'
import { useUserStore } from '../stores/login/user'

export function setupRouterGuards(router: Router) {
  router.beforeEach((to, _from, next) => {
    const userStore = useUserStore()
    const isLoggedIn = !!LoginApi.getUserInfo()  // 通过userInfo判断登录状态
    
    // 1. 未登录用户访问需要认证的页面
    if (to.meta.requiresAuth !== false && !isLoggedIn) {
      return next('/login')
    }
    
    // 2. 已登录用户访问登录页
    if (to.path === '/login' && isLoggedIn) {
      const redirectPath = userStore.userInfo?.role === 'admin' ? '/admin' : '/workflows'
      return next(redirectPath)
    }
    
    // 3. 检查管理员权限
    if (to.meta.requiresAdmin && userStore.userInfo?.role !== 'admin') {
      return next('/workflows')
    }
    
    next()
  })
}