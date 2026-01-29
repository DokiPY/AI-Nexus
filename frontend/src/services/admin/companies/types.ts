// 公司管理相关类型定义

export interface Company {
  id: number
  name: string
  domain: string | null
  is_active: boolean
  user_count?: number
  created_at: string
  updated_at: string
}

export interface CreateCompanyRequest {
  name: string
  domain?: string
  is_active?: boolean
}

export interface UpdateCompanyRequest {
  name?: string
  domain?: string
  is_active?: boolean
}

export interface CompanyListResponse {
  total: number
  companies: Company[]
}
