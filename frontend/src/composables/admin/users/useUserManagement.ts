// 用户管理业务逻辑

import { ref, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { UserApi } from '../../../services'
import type { User, AdminWorkflow } from '../../../services'
import { useRefreshControl } from '../../common/useRefreshControl'
import { useAdminDataStore } from '../../../stores'

interface UserForm {
  username: string
  email: string
  password: string
  role: 'user' | 'admin'
  company_name: string
  is_active: boolean
}

export function useUserManagement() {
  const allUsers = ref<User[]>([])
  const { companies, loadCompanies: loadCompaniesFromStore } = useAdminDataStore()
  const availableWorkflows = ref<AdminWorkflow[]>([])
  const { loading, executeRefresh } = useRefreshControl()
  const searchQuery = ref('')
  const roleFilter = ref<'admin' | 'user' | ''>('')
  const statusFilter = ref<'active' | 'inactive' | ''>('')
  const companyIdsFilter = ref<number[]>([])

  const sortProp = ref<'created_at'>('created_at')
  const sortOrder = ref<'ascending' | 'descending'>('descending')

  const currentPage = ref(1)
  const pageSize = ref(10)

  const showCreateDialog = ref(false)
  const showEditDialog = ref(false)
  const showWorkflowDialog = ref(false)
  const selectedUser = ref<User | null>(null)
  const selectedWorkflows = ref<number[]>([])

  const userForm = ref<UserForm>({
    username: '',
    email: '',
    password: '',
    role: 'user',
    company_name: '',
    is_active: true
  })

  // 前端搜索 + 条件筛选
  const filteredUsers = computed(() => {
    const query = searchQuery.value.trim().toLowerCase()

    return allUsers.value.filter((user) => {
      // 搜索
      const matchesSearch =
        !query ||
        user.username.toLowerCase().includes(query) ||
        user.email?.toLowerCase().includes(query) ||
        user.company_name.toLowerCase().includes(query)

      // 角色
      const matchesRole = !roleFilter.value || user.role === roleFilter.value

      // 状态
      const matchesStatus =
        !statusFilter.value ||
        (statusFilter.value === 'active' ? user.is_active : !user.is_active)

      // 公司（多选）
      const matchesCompany =
        companyIdsFilter.value.length === 0 ? true : companyIdsFilter.value.includes(user.company_id)

      return matchesSearch && matchesRole && matchesStatus && matchesCompany
    })
  })

  const hasActiveFilters = computed(() => {
    return (
      !!searchQuery.value.trim() ||
      !!roleFilter.value ||
      !!statusFilter.value ||
      companyIdsFilter.value.length > 0
    )
  })

  // 前端排序（默认按创建时间最新）
  const sortedUsers = computed(() => {
    const list = [...filteredUsers.value]
    if (sortProp.value === 'created_at') {
      list.sort((a, b) => {
        const at = new Date(a.created_at).getTime()
        const bt = new Date(b.created_at).getTime()
        return sortOrder.value === 'ascending' ? at - bt : bt - at
      })
    }
    return list
  })

  const totalUsers = computed(() => sortedUsers.value.length)

  const paginatedUsers = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value
    const end = start + pageSize.value
    return sortedUsers.value.slice(start, end)
  })

  const clearFilters = () => {
    searchQuery.value = ''
    roleFilter.value = ''
    statusFilter.value = ''
    companyIdsFilter.value = []
  }

  const handleSortChange = (payload: { prop: string; order: 'ascending' | 'descending' | null }) => {
    if (payload.prop !== 'created_at') return
    sortProp.value = 'created_at'
    // Element Plus order 为空时回到默认（最新）
    sortOrder.value = payload.order || 'descending'
  }

  // 加载用户列表
  const loadUsers = async (showSuccessMsg = false) => {
    await executeRefresh(async () => {
      try {
        const response = await UserApi.getUserList({
          page: 1,
          page_size: 9999
        })
        allUsers.value = response.users
      } catch (error: any) {
        ElMessage.error(error.message || '加载用户失败')
        throw error
      }
    }, showSuccessMsg)
  }

  // 加载公司列表（使用缓存）
  const loadCompanies = async () => {
    try {
      await loadCompaniesFromStore()
    } catch (error: any) {
      ElMessage.error(error.message || '加载公司信息失败')
    }
  }

  // 加载工作流列表
  const loadWorkflows = async () => {
    try {
      availableWorkflows.value = await UserApi.getWorkflows() as any
    } catch (error: any) {
      ElMessage.error(error.message || '加载工作流失败')
    }
  }

  // 编辑用户
  const editUser = (user: User) => {
    selectedUser.value = user
    userForm.value = {
      username: user.username,
      email: user.email || '',
      password: '',
      role: user.role as 'user' | 'admin',
      company_name: user.company_name,
      is_active: user.is_active
    }
    showEditDialog.value = true
  }

  // 重置用户密码
  const resetPassword = async (user: User) => {
    try {
      const { value: newPassword } = await ElMessageBox.prompt(
        `请输入用户 "${user.username}" 的新密码`,
        '重置密码',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          inputType: 'password',
          inputPlaceholder: '请输入新密码（至少6位）',
          inputValidator: (value) => {
            if (!value) {
              return '密码不能为空'
            }
            if (value.length < 6) {
              return '密码长度至少6位'
            }
            return true
          }
        }
      )
      
      await UserApi.resetUserPassword(user.id.toString(), newPassword)
      ElMessage.success('密码重置成功')
    } catch (error: any) {
      if (error !== 'cancel') {
        ElMessage.error(error.message || '重置密码失败')
      }
    }
  }

  // 删除用户
  const deleteUser = async (user: User) => {
    try {
      await ElMessageBox.confirm(`确定要删除用户 "${user.username}" 吗？`, '确认删除', {
        type: 'warning'
      })
      
      await UserApi.deleteUser(user.id.toString())
      await loadUsers()
      ElMessage.success('用户删除成功')
    } catch (error: any) {
      if (error !== 'cancel') {
        ElMessage.error(error.message || '删除用户失败')
      }
    }
  }

  // 管理工作流权限
  const manageWorkflows = async (user: User) => {
    selectedUser.value = user
    await loadWorkflows()
    try {
      const workflowIds = await UserApi.getUserWorkflows(user.id.toString())
      selectedWorkflows.value = workflowIds
      
      // 更新用户的 workflow_count 为实际数量
      const targetUser = allUsers.value.find(u => u.id === user.id)
      if (targetUser) {
        targetUser.workflow_count = workflowIds.length
      }
    } catch (error: any) {
      ElMessage.error(error.message || '获取用户权限失败')
      selectedWorkflows.value = []
    }
    showWorkflowDialog.value = true
  }

  // 保存用户
  const saveUser = async () => {
    try {
      if (showCreateDialog.value) {
        await UserApi.createUser({
          username: userForm.value.username,
          email: userForm.value.email,
          password: userForm.value.password,
          role: userForm.value.role,
          company_name: userForm.value.company_name,
          is_active: userForm.value.is_active
        })
        ElMessage.success('用户创建成功')
      } else if (selectedUser.value) {
        await UserApi.updateUser(selectedUser.value.id.toString(), {
          email: userForm.value.email,
          role: userForm.value.role,
          company_name: userForm.value.company_name,
          is_active: userForm.value.is_active
        })
        ElMessage.success('用户更新成功')
      }
      await loadUsers()
      closeDialog()
    } catch (error: any) {
      ElMessage.error(error.message || '保存失败')
    }
  }

  // 保存工作流权限
  const saveWorkflowPermissions = async () => {
    try {
      if (!selectedUser.value) return
      
      await UserApi.updateUserWorkflows(
        selectedUser.value.id.toString(),
        selectedWorkflows.value
      )
      
      // 重新加载用户列表以更新 workflow_count
      await loadUsers()
      ElMessage.success('权限保存成功')
      showWorkflowDialog.value = false
    } catch (error: any) {
      ElMessage.error(error.message || '保存权限失败')
    }
  }

  // 关闭对话框
  const closeDialog = () => {
    showCreateDialog.value = false
    showEditDialog.value = false
    resetForm()
  }

  // 重置表单
  const resetForm = () => {
    userForm.value = {
      username: '',
      email: '',
      password: '',
      role: 'user',
      company_name: '',
      is_active: true
    }
    selectedUser.value = null
  }

  // 处理分页大小变化
  const handleSizeChange = (val: number) => {
    pageSize.value = val
    currentPage.value = 1
  }

  // 处理当前页变化
  const handleCurrentChange = (val: number) => {
    currentPage.value = val
  }
  
  // 手动刷新
  const handleRefresh = () => {
    loadUsers(true)
  }

  // 搜索时重置到第一页
  watch(searchQuery, () => {
    currentPage.value = 1
  })

  watch([roleFilter, statusFilter, companyIdsFilter], () => {
    currentPage.value = 1
  })

  return {
    // 状态
    companies,
    availableWorkflows,
    loading,
    searchQuery,
    roleFilter,
    statusFilter,
    companyIdsFilter,
    hasActiveFilters,
    currentPage,
    pageSize,
    totalUsers,
    showCreateDialog,
    showEditDialog,
    showWorkflowDialog,
    selectedUser,
    selectedWorkflows,
    userForm,
    
    // 计算属性
    paginatedUsers,
    
    // 方法
    clearFilters,
    handleSortChange,
    loadUsers,
    loadCompanies,
    loadWorkflows,
    editUser,
    deleteUser,
    resetPassword,
    manageWorkflows,
    saveUser,
    saveWorkflowPermissions,
    closeDialog,
    resetForm,
    handleSizeChange,
    handleCurrentChange,
    handleRefresh
  }
}