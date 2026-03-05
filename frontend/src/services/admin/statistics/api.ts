import type {
  StatisticsOverview,
  ChatTrend,
  WorkflowRanking,
  CompanyDistribution,
  ResponseTimeDistribution,
  CompanyUserActivity,
  ResponseTimeByWorkflow,
  HourlyHeatmap,
  RecentChatsResponse
} from './types'
import { http } from '../../http'

export class StatisticsApi {
  static async getOverview(): Promise<StatisticsOverview> {
    return http.get<StatisticsOverview>('/admin/statistics/overview')
  }

  static async getChatTrend(days: number = 7): Promise<ChatTrend[]> {
    const data = await http.get<{ trend: ChatTrend[] }>('/admin/statistics/trend', { days })
    return data?.trend ?? []
  }

  static async getWorkflowRanking(limit: number = 10): Promise<WorkflowRanking[]> {
    const data = await http.get<{ ranking: WorkflowRanking[] }>('/admin/statistics/workflow-ranking', { limit })
    return data?.ranking ?? []
  }

  static async getCompanyDistribution(): Promise<CompanyDistribution[]> {
    const data = await http.get<{ distribution: CompanyDistribution[] }>('/admin/statistics/company-distribution')
    return data?.distribution ?? []
  }

  static async getUserActivity(days: number = 7, limit: number = 20): Promise<CompanyUserActivity[]> {
    const data = await http.get<{ activity: CompanyUserActivity[] }>('/admin/statistics/user-activity', { days, limit })
    return data?.activity ?? []
  }

  static async getResponseTimeDistribution(): Promise<ResponseTimeDistribution[]> {
    const data = await http.get<{ distribution: ResponseTimeDistribution[] }>('/admin/statistics/response-time-distribution')
    return data?.distribution ?? []
  }

  static async getResponseTimeByWorkflow(days: number = 7, limit: number = 10): Promise<ResponseTimeByWorkflow[]> {
    const data = await http.get<{ ranking: ResponseTimeByWorkflow[] }>('/admin/statistics/response-time-by-workflow', { days, limit })
    return data?.ranking ?? []
  }

  static async getHourlyHeatmap(): Promise<HourlyHeatmap[]> {
    const data = await http.get<{ heatmap: HourlyHeatmap[] }>('/admin/statistics/hourly-heatmap')
    return data?.heatmap ?? []
  }

  static async getRecentChats(page: number = 1, pageSize: number = 20): Promise<RecentChatsResponse> {
    return http.get<RecentChatsResponse>('/admin/statistics/recent-chats', { page, page_size: pageSize })
  }
}
