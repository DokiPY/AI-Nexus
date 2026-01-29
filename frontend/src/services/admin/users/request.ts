// 用户管理模块的请求工具

import { API_BASE_URL } from '../../index'

/**
 * 用户管理模块的 API 请求封装
 */
export async function request<T = any>(url: string, options: RequestInit = {}): Promise<T> {
  const token = localStorage.getItem('access_token')
  if (!token) {
    throw new Error('未登录')
  }

  let parsedToken = token
  try {
    const tokenData = JSON.parse(token)
    parsedToken = tokenData.token
  } catch {
    // token可能是纯字符串格式
  }

  const response = await fetch(`${API_BASE_URL}${url}`, {
    ...options,
    headers: {
      'Authorization': `Bearer ${parsedToken}`,
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
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_info')
      window.location.href = '/login'
    }
    
    throw new Error(errorMsg)
  }

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || errorData.message || '请求失败')
  }

  if (response.status === 204) {
    return undefined as T
  }

  return await response.json()
}
