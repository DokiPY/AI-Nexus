// 公共组件
export { default as AppBackground } from './common/AppBackground.vue'
export { default as AppHeader } from './common/AppHeader.vue'
export { default as AdminSidebar } from './common/AdminSidebar.vue'
export { default as ContentContainer } from './common/ContentContainer.vue'
export { default as ActionBar } from './common/ActionBar.vue'

// 登录组件
export { default as LoginCard } from './login/LoginCard.vue'
export { default as LoginHeader } from './login/LoginHeader.vue'
export { default as LoginFormContent } from './login/LoginFormContent.vue'
export { default as LoginFooter } from './login/LoginFooter.vue'

// 用户管理组件
export { default as UserTable } from './admin/users/UserTable.vue'
export { default as UserFormDialog } from './admin/users/UserFormDialog.vue'
export { default as WorkflowPermissionDialog } from './admin/users/WorkflowPermissionDialog.vue'

// 公司管理组件
export { default as CompanyTable } from './admin/companies/CompanyTable.vue'
export { default as CompanyFormDialog } from './admin/companies/CompanyFormDialog.vue'
export { default as CompanyUsersDialog } from './admin/companies/CompanyUsersDialog.vue'

// 工作流管理组件
export { default as WorkflowTable } from './admin/workflows/WorkflowTable.vue'
export { default as WorkflowFormDialog } from './admin/workflows/WorkflowFormDialog.vue'

// 统计组件
export { default as StatisticsCards } from './admin/statistics/StatisticsCards.vue'
export { default as ChatTrendChart } from './admin/statistics/ChatTrendChart.vue'
export { default as UserActivityChart } from './admin/statistics/UserActivityChart.vue'
export { default as WorkflowRankingChart } from './admin/statistics/WorkflowRankingChart.vue'
export { default as ResponseTimeChart } from './admin/statistics/ResponseTimeChart.vue'
export { default as ResponseTimeByWorkflowChart } from './admin/statistics/ResponseTimeByWorkflowChart.vue'
export { default as CompanyDistributionChart } from './admin/statistics/CompanyDistributionChart.vue'

// 用户工作流组件
export { default as WorkflowSidebar } from './user/workflow/WorkflowSidebar.vue'
export { default as WorkflowChatArea } from './user/workflow/WorkflowChatArea.vue'
export { default as WorkflowEmptyState } from './user/workflow/WorkflowEmptyState.vue'
export { default as NoWorkflowState } from './user/workflow/NoWorkflowState.vue'