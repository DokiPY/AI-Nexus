// 用户工作流相关类型定义

export interface Workflow {
  id: number
  name: string
  description: string
  icon: string
  category: string
  n8n_webhook_url?: string
  is_active: boolean
  has_permission: boolean
  status: 'available' | 'no_permission'
  created_at: string
  color?: string // 前端UI用
}

export interface WorkflowListResponse {
  total_workflows: number
  available_count: number
  workflows: Workflow[]
}

export interface CategoryResponse {
  categories: string[]
}

export interface ChatMessage {
  id: number
  role: 'user' | 'ai'
  message: string
  created_at: string
}

export interface ChatHistoryResponse {
  workflow: {
    id: number
    name: string
    description: string
    icon: string
  }
  messages: ChatMessage[]
}

export interface SendMessageRequest {
  message: string
}

export interface SendMessageResponse {
  user_message: ChatMessage
  ai_message: ChatMessage
}
