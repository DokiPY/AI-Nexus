import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { StatisticsApi } from '@/services'
import type {
  StatisticsOverview,
  ChatTrend,
  WorkflowRanking,
  CompanyUserActivity,
  ResponseTimeByWorkflow
} from '@/services'

export function useStatistics() {
  const loading = ref(false)
  const overview = ref<StatisticsOverview>({
    total_messages: 0,
    active_users: 0,
    avg_response_time: 0,
    today_messages: 0
  })
  const chatTrend = ref<ChatTrend[]>([])
  const workflowRanking = ref<WorkflowRanking[]>([])
  const userActivity = ref<CompanyUserActivity[]>([])
  const responseTimeByWorkflow = ref<ResponseTimeByWorkflow[]>([])

  const loadOverview = async () => {
    try {
      overview.value = await StatisticsApi.getOverview()
    } catch (error: any) {
      ElMessage.error(error.message || '加载概览数据失败')
    }
  }

  const loadChatTrend = async (days: number = 7) => {
    try {
      chatTrend.value = await StatisticsApi.getChatTrend(days)
    } catch (error: any) {
      ElMessage.error(error.message || '加载趋势数据失败')
    }
  }

  const loadWorkflowRanking = async () => {
    try {
      workflowRanking.value = await StatisticsApi.getWorkflowRanking()
    } catch (error: any) {
      ElMessage.error(error.message || '加载排行数据失败')
    }
  }

  const loadUserActivity = async () => {
    try {
      userActivity.value = await StatisticsApi.getUserActivity()
    } catch (error: any) {
      ElMessage.error(error.message || '加载用户活跃度数据失败')
    }
  }

  const loadResponseTimeByWorkflow = async () => {
    try {
      responseTimeByWorkflow.value = await StatisticsApi.getResponseTimeByWorkflow()
    } catch (error: any) {
      ElMessage.error(error.message || '加载响应耗时数据失败')
    }
  }

  const loadAllData = async () => {
    loading.value = true
    try {
      await Promise.all([
        loadOverview(),
        loadChatTrend(),
        loadWorkflowRanking(),
        loadUserActivity(),
        loadResponseTimeByWorkflow()
      ])
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    overview,
    chatTrend,
    workflowRanking,
    userActivity,
    responseTimeByWorkflow,
    loadAllData,
    loadChatTrend
  }
}
