// 登录相关的数据类型定义

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  user_info: UserInfo  // 不再返回access_token
}

export interface UserInfo {
  id: string  // UUID
  username: string
  email: string
  role: string
  company: {
    id: number
    name: string
  }
}

// 新增用户请求参数
export interface CreateUserRequest {
  username: string
  email: string
  company_name: string
  role: 'user'
  is_active: boolean
  password: string
}

// 公司信息
export interface Company {
  id: number
  name: string
  domain: string
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface ApiResponse<T> {
  data?: T
  message?: string
  error?: string
}