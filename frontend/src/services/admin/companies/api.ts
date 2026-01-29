// 公司管理API

import type { Company, CreateCompanyRequest, UpdateCompanyRequest } from './types'
import { http } from '../../http'

export class CompanyApi {
  /**
   * 获取公司列表 - GET /admin/companies/
   */
  static async getCompanies(): Promise<Company[]> {
    return http.get<Company[]>('/admin/companies')
  }

  /**
   * 创建公司 - POST /admin/companies
   */
  static async createCompany(data: CreateCompanyRequest): Promise<Company> {
    return http.post<Company>('/admin/companies', data)
  }

  /**
   * 更新公司 - PUT /admin/companies/{company_id}
   */
  static async updateCompany(companyId: number, data: UpdateCompanyRequest): Promise<Company> {
    return http.put<Company>(`/admin/companies/${companyId}`, data)
  }

  /**
   * 删除公司 - DELETE /admin/companies/{company_id}
   */
  static async deleteCompany(companyId: number): Promise<void> {
    return http.delete<void>(`/admin/companies/${companyId}`)
  }

  /**
   * 获取公司详情 - GET /admin/companies/{company_id}
   */
  static async getCompanyDetail(companyId: number): Promise<Company> {
    return http.get<Company>(`/admin/companies/${companyId}`)
  }

  /**
   * 获取公司用户列表 - GET /admin/companies/{company_id}/users
   */
  static async getCompanyUsers(companyId: number): Promise<any[]> {
    return http.get<any[]>(`/admin/companies/${companyId}/users`)
  }
}
