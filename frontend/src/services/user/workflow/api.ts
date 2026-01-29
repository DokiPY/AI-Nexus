// 用户工作流API

import type { WorkflowListResponse, CategoryResponse, ChatHistoryResponse, SendMessageRequest, SendMessageResponse } from './types'
import { http } from '../../http'

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
   * 发送消息 - POST /user/chat/{workflow_id}/messages
   */
  static async sendMessage(workflowId: number, data: SendMessageRequest): Promise<SendMessageResponse> {
    return http.post<SendMessageResponse>(`/user/chat/${workflowId}/messages`, data)
  }

  /**
   * 清空聊天记录 - DELETE /user/chat/{workflow_id}
   */
  static async clearChatHistory(workflowId: number): Promise<void> {
    return http.delete<void>(`/user/chat/${workflowId}`)
  }
}
