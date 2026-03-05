// 工作流管理相关的类型定义

export interface Workflow {
  id: number
  name: string
  description?: string
  category: string
  http_method: string
  n8n_webhook_url: string
  stream_enabled: boolean
  icon?: string
  created_at: string
  updated_at?: string
}

export interface CreateWorkflowRequest {
  name: string
  description?: string
  category: string
  http_method: string
  n8n_webhook_url: string
  stream_enabled?: boolean
  icon?: string
}

export interface UpdateWorkflowRequest {
  name?: string
  description?: string
  category?: string
  http_method?: string
  n8n_webhook_url?: string
  stream_enabled?: boolean
  icon?: string
}
