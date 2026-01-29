// 服务层统一导出

// API 基础配置
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

// 环境日志
if (import.meta.env.VITE_ENV === 'local') {
  console.log('当前环境：local')
} else if (import.meta.env.VITE_ENV === 'test') {
  console.log('当前环境：test')
} else if (import.meta.env.VITE_ENV === 'staging') {
  console.log('当前环境：staging')
} else if (import.meta.env.VITE_ENV === 'production') {
  console.log('当前环境：production')
}

// HTTP 客户端
export { http } from './http'

// 登录相关
export { LoginApi } from './login/api'
export type { LoginRequest, LoginResponse, UserInfo, CreateUserRequest, ApiResponse, Company as LoginCompany } from './login/types'

// 用户管理相关
export { UserApi } from './admin/users/api'
export type { User, CreateUserRequest as AdminCreateUserRequest, UpdateUserRequest, UserListQuery, UserListResponse, Company as AdminCompany, Workflow as AdminWorkflow } from './admin/users/types'

// 公司管理相关
export { CompanyApi } from './admin/companies/api'
export type { Company, CreateCompanyRequest, UpdateCompanyRequest, CompanyListResponse } from './admin/companies/types'

// 工作流管理相关
export { WorkflowApi as WorkflowManagementApi } from './admin/workflows/api'
export type { Workflow as AdminWorkflowType, CreateWorkflowRequest, UpdateWorkflowRequest } from './admin/workflows/types'

// 统计相关
export { StatisticsApi } from './admin/statistics/api'
export type { 
  StatisticsOverview, 
  ChatTrend, 
  WorkflowRanking, 
  CompanyDistribution, 
  ResponseTimeDistribution, 
  CompanyUserActivity, 
  ResponseTimeByWorkflow,
  HourlyHeatmap,
  ChatRecord,
  RecentChatsResponse
} from './admin/statistics/types'

// 用户工作流相关
export { WorkflowApi } from './user/workflow/api'
export type { Workflow, WorkflowListResponse, CategoryResponse, ChatMessage, ChatHistoryResponse, SendMessageRequest, SendMessageResponse } from './user/workflow/types'