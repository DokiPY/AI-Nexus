// 用户管理相关的数据类型定义

/**
 * 用户信息
 */
export interface User {
  id: string
  username: string
  email?: string
  role: string
  company_name: string
  company_id: number
  is_active: boolean
  workflow_count?: number
  created_at: string
  workflows?: Array<{ id: number; name: string; icon: string }>
}

/**
 * 新增用户请求参数
 */
export interface CreateUserRequest {
  username: string
  email: string
  password: string
  company_name: string
  role: 'user' | 'admin'
  is_active: boolean
}

/**
 * 更新用户请求参数
 */
export interface UpdateUserRequest {
  email?: string
  role?: 'user' | 'admin'
  company_name?: string
  is_active?: boolean
}

/**
 * 用户列表查询参数
 */
export interface UserListQuery {
  page?: number
  page_size?: number
  search?: string
  role?: string
  company_id?: number
  is_active?: boolean
}

/**
 * 用户列表响应
 */
export interface UserListResponse {
  users: User[]
  total: number
  page: number
  page_size: number
}

/**
 * 工作流信息
 */
export interface Workflow {
  id: number
  name: string
  description: string
  icon: string
  is_active: boolean
  created_at: string
}

/**
 * 用户工作流权限
 */
export interface UserWorkflowPermission {
  user_id: string
  workflow_ids: number[]
}

/**
 * 公司信息
 */
export interface Company {
  id: number
  name: string
  domain: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}