// 用户工作流API

import type { WorkflowListResponse, CategoryResponse, ChatHistoryResponse, SendMessageRequest } from './types'
import { http } from '../../http'
import { API_BASE_URL } from '../../index'

export class WorkflowApi {
  /**
   * 获取用户可见的工作流列表 - GET /user/workflows/
   */
  static async getWorkflows(category?: string): Promise<WorkflowListResponse> {
    const params: Record<string, any> = {}
    if (category && category !== '全部') {
      params.category = category
    }
    return http.get<WorkflowListResponse>('/user/workflows/', params)
  }

  /**
   * 获取工作流分类 - GET /user/workflows/categories
   */
  static async getCategories(): Promise<CategoryResponse> {
    return http.get<CategoryResponse>('/user/workflows/categories')
  }

  /**
   * 获取聊天历史 - GET /user/chat/{workflow_id}
   */
  static async getChatHistory(workflowId: number): Promise<ChatHistoryResponse> {
    return http.get<ChatHistoryResponse>(`/user/chat/${workflowId}`)
  }

  /**
   * 流式发送消息 - POST /user/chat/{workflow_id}/messages
   * 返回 ReadableStream，调用方逐块读取
   */
  static async sendMessageStream(
    workflowId: number,
    data: SendMessageRequest,
    onChunk: (content: string) => void,
    onDone?: (data: { id: number; response_time_ms: number }) => void
  ): Promise<string> {
    const response = await fetch(`${API_BASE_URL}/user/chat/${workflowId}/messages`, {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    })

    if (response.status === 401 || response.status === 403) {
      const errorData = await response.json().catch(() => ({}))
      const errorMsg = errorData.detail || '登录已过期，请重新登录'
      throw new Error(errorMsg)
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.detail || errorData.message || '发送消息失败')
    }

    const reader = response.body!.getReader()
    const decoder = new TextDecoder()
    let fullText = ''
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      // 保留最后一个可能不完整的行
      buffer = lines.pop() || ''

      for (const line of lines) {
        if (!line.startsWith('data: ')) continue
        try {
          const event = JSON.parse(line.slice(6))
          if (event.type === 'chunk') {
            fullText += event.content
            onChunk(event.content)
          } else if (event.type === 'done' && onDone) {
            onDone(event.data)
          }
        } catch {
          // 忽略解析失败的行
        }
      }
    }

    return fullText
  }

  /**
   * 清空聊天记录 - DELETE /user/chat/{workflow_id}
   */
  static async clearChatHistory(workflowId: number): Promise<void> {
    return http.delete<void>(`/user/chat/${workflowId}`)
  }
}
