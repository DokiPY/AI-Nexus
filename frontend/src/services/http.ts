/**
 * HTTP 请求客户端
 * 统一处理请求/响应、错误处理、token 管理
 */

interface RequestConfig extends RequestInit {
  params?: Record<string, any>
}

class HttpClient {
  private baseURL: string

  constructor(baseURL: string) {
    this.baseURL = baseURL
  }

  /**
   * 处理 URL 参数
   */
  private buildURL(url: string, params?: Record<string, any>): string {
    if (!params) return url

    const queryString = Object.entries(params)
      .filter(([_, value]) => value !== undefined && value !== null)
      .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(value)}`)
      .join('&')

    return queryString ? `${url}?${queryString}` : url
  }

  /**
   * 处理未授权错误
   */
  private handleUnauthorized(message: string) {
    if ((window as any).__logoutInProgress) return

    (window as any).__logoutInProgress = true
    alert(message)
    localStorage.removeItem('user_info')
    window.location.href = '/login'
  }

  /**
   * 通用请求方法
   */
  async request<T = any>(url: string, config: RequestConfig = {}): Promise<T> {
    const { params, ...options } = config

    const fullURL = this.buildURL(`${this.baseURL}${url}`, params)

    const response = await fetch(fullURL, {
      ...options,
      credentials: 'include',  // 自动携带Cookie
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    })

    // 处理未授权
    if (response.status === 401 || response.status === 403) {
      const errorData = await response.json().catch(() => ({}))
      const errorMsg = errorData.detail || '登录已过期，请重新登录'
      this.handleUnauthorized(errorMsg)
      throw new Error(errorMsg)
    }

    // 处理错误响应
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || errorData.message || '请求失败')
    }

    // 处理 204 No Content
    if (response.status === 204) {
      return undefined as T
    }

    const json = await response.json()

    // 统一解包后端标准响应格式 { success, code, message, data }
    if (json && typeof json === 'object' && 'success' in json) {
      if (!json.success) {
        throw new Error(json.message || '请求失败')
      }
      return json.data as T
    }

    return json as T
  }

  /**
   * GET 请求
   */
  get<T = any>(url: string, params?: Record<string, any>): Promise<T> {
    return this.request<T>(url, { method: 'GET', params })
  }

  /**
   * POST 请求
   */
  post<T = any>(url: string, data?: any): Promise<T> {
    return this.request<T>(url, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined
    })
  }

  /**
   * PUT 请求
   */
  put<T = any>(url: string, data?: any): Promise<T> {
    return this.request<T>(url, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined
    })
  }

  /**
   * DELETE 请求
   */
  delete<T = any>(url: string): Promise<T> {
    return this.request<T>(url, { method: 'DELETE' })
  }
}

// 导出单例
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'
export const http = new HttpClient(API_BASE_URL)
