// 用户管理相关的API接口调用

import type { 
  User, 
  CreateUserRequest, 
  UpdateUserRequest, 
  UserListQuery, 
  UserListResponse,
  Workflow,
  Company
} from './types'
import { http } from '../../http'

export class UserApi {

  /**
   * 获取用户列表 - GET /admin/users/
   */
  static async getUserList(query: UserListQuery = {}): Promise<UserListResponse> {
    return http.get<UserListResponse>('/admin/users/', query)
  }

  /**
   * 新增用户 - POST /admin/users/
   */
  static async createUser(userData: CreateUserRequest): Promise<User> {
    return http.post<User>('/admin/users/', userData)
  }

  /**
   * 更新用户信息 - PUT /admin/users/{user_id}
   */
  static async updateUser(userId: string, userData: UpdateUserRequest): Promise<User> {
    return http.put<User>(`/admin/users/${userId}`, userData)
  }

  /**
   * 删除用户 - DELETE /admin/users/{user_id}
   */
  static async deleteUser(userId: string): Promise<void> {
    return http.delete<void>(`/admin/users/${userId}`)
  }

  /**
   * 获取用户详情 - GET /admin/users/{user_id}
   */
  static async getUserDetail(userId: string): Promise<User> {
    return http.get<User>(`/admin/users/${userId}`)
  }

  /**
   * 获取所有公司信息 - GET /admin/companies
   */
  static async getCompanies(): Promise<Company[]> {
    return http.get<Company[]>('/admin/companies')
  }

  /**
   * 获取所有工作流 - GET /admin/workflows/
   */
  static async getWorkflows(): Promise<Workflow[]> {
    return http.get<Workflow[]>('/admin/workflows/')
  }

  /**
   * 获取用户工作流权限 - GET /admin/users/{user_id}/workflows
   */
  static async getUserWorkflows(userId: string): Promise<number[]> {
    const data = await http.get<{ workflow_ids: number[] }>(`/admin/users/${userId}/workflows`)
    return data.workflow_ids || []
  }

  /**
   * 更新用户工作流权限 - PUT /admin/users/{user_id}/workflows
   */
  static async updateUserWorkflows(userId: string, workflowIds: number[]): Promise<void> {
    return http.put<void>(`/admin/users/${userId}/workflows`, { workflow_ids: workflowIds })
  }

  /**
   * 批量删除用户 - DELETE /admin/users/batch
   */
  static async batchDeleteUsers(_userIds: string[]): Promise<void> {
    return http.delete<void>('/admin/users/batch')
  }

  /**
   * 重置用户密码 - POST /admin/users/{user_id}/reset-password
   */
  static async resetUserPassword(userId: string, newPassword: string): Promise<void> {
    return http.post<void>(`/admin/users/${userId}/reset-password`, { new_password: newPassword })
  }
}