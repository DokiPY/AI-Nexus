// Admin布局逻辑

import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { LoginApi } from '../../services/login/api'

export function useAdminLayout() {
  const router = useRouter()
  const route = useRoute()
  const activeMenu = ref('users')
  const sidebarCollapsed = ref(false)

  // 菜单项配置
  const menuItems = [
    { key: 'users', label: '用户管理', icon: 'UserIcon' },
    { key: 'companies', label: '公司管理', icon: 'CompanyIcon' },
    { key: 'workflows', label: '工作流管理', icon: 'WorkflowIcon' },
    { key: 'statistics', label: '数据统计', icon: 'ChartIcon' }
    // { key: 'settings', label: '系统设置', icon: 'SettingsIcon' }
  ]

  // 根据当前路由设置活跃菜单
  watch(
    () => route.path,
    (path) => {
      const match = path.match(/\/admin\/(\w+)/)
      if (match && match[1]) {
        activeMenu.value = match[1]
      }
    },
    { immediate: true }
  )

  // 验证用户状态
  onMounted(async () => {
    await LoginApi.validateUser()
  })

  // 处理菜单切换
  const handleMenuChange = (key: string) => {
    // 如果已经在当前页面，不重复跳转
    if (activeMenu.value === key) {
      return
    }
    
    activeMenu.value = key
    router.push(`/admin/${key}`)
  }

  // 退出登录 - 只负责跳转
  const logout = () => {
    router.push('/login')
  }

  return {
    activeMenu,
    sidebarCollapsed,
    menuItems,
    handleMenuChange,
    logout
  }
}
