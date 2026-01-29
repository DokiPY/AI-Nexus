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
    return http.get<ChatTrend[]>('/admin/statistics/trend', { days })
  }

  static async getWorkflowRanking(limit: number = 10): Promise<WorkflowRanking[]> {
    return http.get<WorkflowRanking[]>('/admin/statistics/workflow-ranking', { limit })
  }

  static async getCompanyDistribution(): Promise<CompanyDistribution[]> {
    return http.get<CompanyDistribution[]>('/admin/statistics/company-distribution')
  }

  static async getUserActivity(days: number = 7, limit: number = 20): Promise<CompanyUserActivity[]> {
    return http.get<CompanyUserActivity[]>('/admin/statistics/user-activity', { days, limit })
  }

  static async getResponseTimeDistribution(): Promise<ResponseTimeDistribution[]> {
    return http.get<ResponseTimeDistribution[]>('/admin/statistics/response-time-distribution')
  }

  static async getResponseTimeByWorkflow(days: number = 7, limit: number = 10): Promise<ResponseTimeByWorkflow[]> {
    return http.get<ResponseTimeByWorkflow[]>('/admin/statistics/response-time-by-workflow', { days, limit })
  }

  static async getHourlyHeatmap(): Promise<HourlyHeatmap[]> {
    return http.get<HourlyHeatmap[]>('/admin/statistics/hourly-heatmap')
  }

  static async getRecentChats(page: number = 1, pageSize: number = 20): Promise<RecentChatsResponse> {
    return http.get<RecentChatsResponse>('/admin/statistics/recent-chats', { page, page_size: pageSize })
  }
}
