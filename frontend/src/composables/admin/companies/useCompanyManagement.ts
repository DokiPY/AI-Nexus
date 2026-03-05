// 公司管理业务逻辑

import { ref, computed, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { CompanyApi } from '@/services'
import type { Company } from '@/services'
import { useRefreshControl } from '@/composables'
import { useAdminDataStore } from '@/stores'

interface CompanyForm {
  name: string
  domain: string
  is_active: boolean
}

export function useCompanyManagement() {
  const allCompanies = ref<Company[]>([])
  const { loading, executeRefresh } = useRefreshControl()
  const { setCompanies: setStoreCompanies } = useAdminDataStore()
  const searchQuery = ref('')
  
  const currentPage = ref(1)
  const pageSize = ref(10)
  
  const showCreateDialog = ref(false)
  const showEditDialog = ref(false)
  const showUsersDialog = ref(false)
  const selectedCompany = ref<Company | null>(null)
  const companyUsers = ref<any[]>([])
  const loadingUsers = ref(false)
  
  const companyForm = ref<CompanyForm>({
    name: '',
    domain: '',
    is_active: true
  })

  // 搜索过滤
  const filteredCompanies = computed(() => {
    if (!searchQuery.value) return allCompanies.value
    const query = searchQuery.value.toLowerCase()
    return allCompanies.value.filter(company => 
      company.name.toLowerCase().includes(query) ||
      company.domain?.toLowerCase().includes(query)
    )
  })

  const totalCompanies = computed(() => filteredCompanies.value.length)

  // 分页后的数据
  const paginatedCompanies = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value
    const end = start + pageSize.value
    return filteredCompanies.value.slice(start, end)
  })

  // 加载公司列表，同时同步 store 缓存
  const loadCompanies = async (showSuccessMsg = false) => {
    await executeRefresh(async () => {
      try {
        const result = await CompanyApi.getCompanies()
        allCompanies.value = result.companies ?? []
        // 直接同步到 store 缓存，避免额外请求
        setStoreCompanies(allCompanies.value)
      } catch (error: any) {
        ElMessage.error(error.message || '加载公司列表失败')
        throw error
      }
    }, showSuccessMsg)
  }

  // 编辑公司
  const editCompany = (company: Company) => {
    selectedCompany.value = company
    companyForm.value = {
      name: company.name,
      domain: company.domain || '',
      is_active: company.is_active
    }
    showEditDialog.value = true
  }

  // 删除公司
  const deleteCompany = async (company: Company) => {
    try {
      // 检查公司下是否有用户
      if (company.user_count && company.user_count > 0) {
        await ElMessageBox.alert(
          `无法删除公司 "${company.name}"，该公司下还有 ${company.user_count} 个用户。<br/><br/>请先删除或转移该公司下的所有用户后再进行删除操作。`,
          '无法删除',
          {
            type: 'warning',
            dangerouslyUseHTMLString: true,
            confirmButtonText: '我知道了'
          }
        )
        return
      }
      
      await ElMessageBox.confirm(
        `确定要删除公司 "${company.name}" 吗？`,
        '确认删除',
        {
          type: 'warning',
          confirmButtonText: '确定删除',
          cancelButtonText: '取消'
        }
      )
      
      await CompanyApi.deleteCompany(company.id)
      await loadCompanies()
      ElMessage.success('公司删除成功')
    } catch (error: any) {
      if (error !== 'cancel') {
        ElMessage.error(error.message || '删除公司失败')
      }
    }
  }

  // 保存公司
  const saveCompany = async () => {
    try {
      if (showCreateDialog.value) {
        await CompanyApi.createCompany({
          name: companyForm.value.name,
          domain: companyForm.value.domain || undefined,
          is_active: companyForm.value.is_active
        })
        ElMessage.success('公司创建成功')
      } else if (selectedCompany.value) {
        await CompanyApi.updateCompany(selectedCompany.value.id, {
          name: companyForm.value.name,
          domain: companyForm.value.domain || undefined,
          is_active: companyForm.value.is_active
        })
        ElMessage.success('公司更新成功')
      }
      await loadCompanies()
      closeDialog()
    } catch (error: any) {
      ElMessage.error(error.message || '保存失败')
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
    companyForm.value = {
      name: '',
      domain: '',
      is_active: true
    }
    selectedCompany.value = null
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
    loadCompanies(true)
  }

  // 查看公司用户
  const viewUsers = async (company: Company) => {
    selectedCompany.value = company
    showUsersDialog.value = true
    loadingUsers.value = true
    try {
      companyUsers.value = await CompanyApi.getCompanyUsers(company.id)
    } catch (error: any) {
      ElMessage.error(error.message || '获取用户列表失败')
      companyUsers.value = []
    } finally {
      loadingUsers.value = false
    }
  }

  // 搜索时重置到第一页
  watch(searchQuery, () => {
    currentPage.value = 1
  })

  return {
    // 状态
    loading,
    searchQuery,
    currentPage,
    pageSize,
    totalCompanies,
    showCreateDialog,
    showEditDialog,
    showUsersDialog,
    selectedCompany,
    companyForm,
    companyUsers,
    loadingUsers,
    
    // 计算属性
    paginatedCompanies,
    
    // 方法
    loadCompanies,
    editCompany,
    deleteCompany,
    saveCompany,
    closeDialog,
    resetForm,
    handleSizeChange,
    handleCurrentChange,
    handleRefresh,
    viewUsers
  }
}
