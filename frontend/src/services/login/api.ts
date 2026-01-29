// 登录相关的API接口调用

import type { LoginRequest, LoginResponse, UserInfo, CreateUserRequest, Company } from './types'
import { API_BASE_URL } from '../index'

export class LoginApi {
  /**
   * 用户登录 - POST /auth/login
   */
  static async login(credentials: LoginRequest): Promise<LoginResponse> {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      credentials: 'include',  // 允许携带Cookie
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || '登录失败')
    }

    return await response.json()
  }

  /**
   * 登出
   */
  static async logout(): Promise<void> {
    await fetch(`${API_BASE_URL}/auth/logout`, {
      method: 'POST',
      credentials: 'include'
    })
    this.clearUserInfo()
  }

  /**
   * 保存用户信息到localStorage
   */
  static saveUserInfo(userInfo: UserInfo): void {
    localStorage.setItem('user_info', JSON.stringify(userInfo))
  }

  /**
   * 获取保存的用户信息
   */
  static getUserInfo(): UserInfo | null {
    try {
      const stored = localStorage.getItem('user_info')
      return stored ? JSON.parse(stored) : null
    } catch {
      return null
    }
  }

  /**
   * 验证用户状态 - GET /auth/me
   */
  static async validateUser(): Promise<UserInfo> {
    const response = await this.apiRequest('/auth/me')
    
    if (!response.ok) {
      throw new Error('用户验证失败')
    }
    
    const userInfo = await response.json()
    this.saveUserInfo(userInfo)
    return userInfo
  }

  /**
   * 清除用户信息
   */
  static clearUserInfo(): void {
    localStorage.removeItem('user_info')
  }

  /**
   * 获取所有公司信息 - GET /admin/companies
   */
  static async getCompanies(): Promise<Company[]> {
    const response = await this.apiRequest('/admin/companies')
    
    if (!response.ok) {
      throw new Error('获取公司信息失败')
    }
    
    return await response.json()
  }

  /**
   * 新增用户 - POST /admin/users
   */
  static async createUser(userData: CreateUserRequest): Promise<void> {
    const response = await this.apiRequest('/admin/users', {
      method: 'POST',
      body: JSON.stringify(userData)
    })
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || '新增用户失败')
    }
  }

  /**
   * 带Cookie的API请求封装
   */
  static async apiRequest(url: string, options: RequestInit = {}): Promise<Response> {
    const response = await fetch(`${API_BASE_URL}${url}`, {
      ...options,
      credentials: 'include',  // 自动携带Cookie
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    })

    // 检查401/403错误,自动退出登录
    if (response.status === 401 || response.status === 403) {
      const errorData = await response.json().catch(() => ({}))
      const errorMsg = errorData.detail || '登录已过期，请重新登录'
      
      if (!(window as any).__logoutInProgress) {
        (window as any).__logoutInProgress = true
        alert(errorMsg)
        this.clearUserInfo()
        window.location.href = '/login'
      }
      
      throw new Error(errorMsg)
    }

    return response
  }
}