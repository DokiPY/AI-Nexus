// 工作流列表业务逻辑

import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { WorkflowApi } from '../../../services'
import { LoginApi } from '../../../services'

// 工作流颜色映射
const WORKFLOW_COLORS: Record<string, string> = {
  '办公助手': 'linear-gradient(135deg, #FF9A9E 0%, #FECFEF 100%)',
  '数据分析': 'linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)',
  '客户服务': 'linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%)',
  '开发工具': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  '其他': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
}

export function useWorkflowList() {
  const router = useRouter()
  
  const loading = ref(true)
  const searchQuery = ref('')
  const currentCategory = ref('全部')
  const categories = ref<string[]>(['全部'])
  const workflows = ref<any[]>([])

  // 过滤后的工作流
  const filteredWorkflows = computed(() => {
    return workflows.value.filter((item: any) => {
      const matchSearch = item.name.toLowerCase().includes(searchQuery.value.toLowerCase()) || 
                          item.description.toLowerCase().includes(searchQuery.value.toLowerCase())
      const matchCategory = currentCategory.value === '全部' || item.category === currentCategory.value
      const hasPermission = item.has_permission === true  // 只显示有权限的
      
      return matchSearch && matchCategory && hasPermission
    })
  })

  // 加载工作流列表
  const loadWorkflows = async () => {
    loading.value = true
    try {
      // 不传category参数，获取所有工作流，由前端过滤
      const response = await WorkflowApi.getWorkflows()
      
      workflows.value = response.workflows.map((w: any) => ({
        ...w,
        category: w.category || '其他',
        has_permission: w.has_permission ?? true,
        status: (w.status || 'available') as 'available' | 'no_permission',
        created_at: w.created_at || new Date().toISOString(),
        color: WORKFLOW_COLORS[w.category || '其他'] || WORKFLOW_COLORS['其他']
      }))
    } catch (error: any) {
      ElMessage.error(error.message || '加载工作流失败')
    } finally {
      loading.value = false
    }
  }

  // 加载分类
  const loadCategories = async () => {
    try {
      const response = await WorkflowApi.getCategories()
      categories.value = response.categories
    } catch (error: any) {
      ElMessage.error(error.message || '加载分类失败')
    }
  }

  // 退出登录
  const logout = () => {
    LoginApi.logout()
    router.push('/login')
  }

  // 进入聊天
  const handleEnterChat = (item: any) => {
    if (!item.has_permission) {
      ElMessage.warning('您没有该工作流的使用权限，请联系管理员')
      return
    }
    
    router.push(`/workflows/${item.id}/chat`)
  }

  // 初始化
  onMounted(async () => {
    await LoginApi.validateUser()
    await Promise.all([loadCategories(), loadWorkflows()])
  })

  return {
    loading,
    searchQuery,
    currentCategory,
    categories,
    filteredWorkflows,
    logout,
    handleEnterChat,
    loadWorkflows
  }
}
