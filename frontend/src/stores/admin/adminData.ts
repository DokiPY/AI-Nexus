// 管理后台数据缓存
import { ref } from 'vue'
import { CompanyApi } from '@/services'
import type { Company } from '@/services'

const companies = ref<Company[]>([])
const companiesLoaded = ref(false)
const companiesLoading = ref(false)

export function useAdminDataStore() {
  const loadCompanies = async (forceRefresh = false) => {
    if (companiesLoaded.value && !forceRefresh) {
      return companies.value
    }
    
    if (companiesLoading.value) {
      // 等待正在进行的请求
      await new Promise(resolve => {
        const check = setInterval(() => {
          if (!companiesLoading.value) {
            clearInterval(check)
            resolve(null)
          }
        }, 100)
      })
      return companies.value
    }
    
    companiesLoading.value = true
    try {
      const result = await CompanyApi.getCompanies()
      companies.value = result.companies ?? []
      companiesLoaded.value = true
      return companies.value
    } finally {
      companiesLoading.value = false
    }
  }

  // 直接设置公司列表缓存，避免重复请求
  const setCompanies = (data: Company[]) => {
    companies.value = data
    companiesLoaded.value = true
  }

  const clearCache = () => {
    companies.value = []
    companiesLoaded.value = false
  }

  return {
    companies,
    companiesLoaded,
    loadCompanies,
    setCompanies,
    clearCache
  }
}
