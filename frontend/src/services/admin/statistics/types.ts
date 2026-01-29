export interface StatisticsOverview {
  total_messages: number
  active_users: number
  avg_response_time: number
  today_messages: number
}

export interface ChatTrend {
  date: string
  user_messages: number
  ai_messages: number
}

export interface WorkflowRanking {
  workflow_id: number
  workflow_name: string
  icon: string
  usage_count: number
}

export interface CompanyDistribution {
  company_name: string
  message_count: number
}

export interface ResponseTimeDistribution {
  range: string
  count: number
}

export interface CompanyUserActivity {
  company_id: number
  company_name: string
  user_id: string
  username: string
  message_count: number
  last_active_at: string | null
}

export interface ResponseTimeByWorkflow {
  workflow_id: number
  workflow_name: string
  count: number
  avg_response_time_ms: number
  max_response_time_ms: number
}

export interface HourlyHeatmap {
  day: number
  hour: number
  count: number
}

export interface ChatRecord {
  id: number
  role: string
  message: string
  response_time_ms: number | null
  created_at: string
  username: string
  company_name: string
  workflow_name: string
}

export interface RecentChatsResponse {
  total: number
  page: number
  page_size: number
  records: ChatRecord[]
}
