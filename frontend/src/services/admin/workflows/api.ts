// 工作流管理相关的API接口调用

import type { Workflow, CreateWorkflowRequest, UpdateWorkflowRequest } from './types'
import { http } from '../../http'

export class WorkflowApi {

  /**
   * 获取所有工作流 - GET /admin/workflows/
   */
  static async getWorkflows(): Promise<Workflow[]> {
    return http.get<Workflow[]>('/admin/workflows/')
  }

  /**
   * 创建工作流 - POST /admin/workflows/
   */
  static async createWorkflow(workflowData: CreateWorkflowRequest): Promise<{ message: string; id: number }> {
    return http.post<{ message: string; id: number }>('/admin/workflows/', workflowData)
  }

  /**
   * 更新工作流 - PUT /admin/workflows/{workflow_id}
   */
  static async updateWorkflow(workflowId: number, workflowData: UpdateWorkflowRequest): Promise<{ message: string }> {
    return http.put<{ message: string }>(`/admin/workflows/${workflowId}`, workflowData)
  }

  /**
   * 删除工作流 - DELETE /admin/workflows/{workflow_id}
   */
  static async deleteWorkflow(workflowId: number): Promise<{ message: string }> {
    return http.delete<{ message: string }>(`/admin/workflows/${workflowId}`)
  }
}
