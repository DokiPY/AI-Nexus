import { ref, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { WorkflowManagementApi } from '../../../services'
import type { AdminWorkflowType as Workflow, CreateWorkflowRequest, UpdateWorkflowRequest } from '../../../services'
import { useRefreshControl } from '../../common/useRefreshControl'

interface WorkflowForm {
  name: string
  description: string
  category: string
  http_method: string
  n8n_webhook_url: string
  icon: string
}

export type { Workflow }

export function useWorkflowManagement() {
  const workflows = ref<Workflow[]>([])
  const { loading, executeRefresh } = useRefreshControl()
  const searchQuery = ref('')
  const currentPage = ref(1)
  const pageSize = ref(10)
  const showCreateDialog = ref(false)
  const showEditDialog = ref(false)
  const currentWorkflow = ref<Workflow | null>(null)

  const workflowForm = ref<WorkflowForm>({
    name: '',
    description: '',
    category: '办公助手',
    http_method: 'POST',
    n8n_webhook_url: '',
    icon: ''
  })



  const filteredWorkflows = computed(() => {
    if (!searchQuery.value) return workflows.value
    return workflows.value.filter(w => 
      w.name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  })

  const totalWorkflows = computed(() => filteredWorkflows.value.length)

  const paginatedWorkflows = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value
    const end = start + pageSize.value
    return filteredWorkflows.value.slice(start, end)
  })

  const loadWorkflows = async (showSuccessMsg = false) => {
    await executeRefresh(async () => {
      try {
        workflows.value = await WorkflowManagementApi.getWorkflows()
      } catch (error) {
        ElMessage.error('加载工作流失败')
        throw error
      }
    }, showSuccessMsg)
  }

  const editWorkflow = (workflow: Workflow) => {
    currentWorkflow.value = workflow
    workflowForm.value = {
      name: workflow.name,
      description: workflow.description || '',
      category: workflow.category,
      http_method: workflow.http_method,
      n8n_webhook_url: workflow.n8n_webhook_url,
      icon: workflow.icon || ''
    }
    showEditDialog.value = true
  }

  const deleteWorkflow = async (workflow: Workflow) => {
    try {
      await ElMessageBox.confirm(
        `确定要删除工作流 "${workflow.name}" 吗？`,
        '确认删除',
        { type: 'warning' }
      )
      
      loading.value = true
      await WorkflowManagementApi.deleteWorkflow(workflow.id)
      workflows.value = workflows.value.filter(w => w.id !== workflow.id)
      ElMessage.success('删除成功')
    } catch (error) {
      if (error !== 'cancel') {
        ElMessage.error('删除失败')
      }
    } finally {
      loading.value = false
    }
  }

  const saveWorkflow = async () => {
    if (!workflowForm.value.name || !workflowForm.value.n8n_webhook_url) {
      ElMessage.warning('请填写必填项')
      return
    }

    loading.value = true
    try {
      if (showEditDialog.value && currentWorkflow.value) {
        const updateData: UpdateWorkflowRequest = {
          name: workflowForm.value.name,
          description: workflowForm.value.description,
          category: workflowForm.value.category,
          http_method: workflowForm.value.http_method,
          n8n_webhook_url: workflowForm.value.n8n_webhook_url,
          icon: workflowForm.value.icon
        }
        await WorkflowManagementApi.updateWorkflow(currentWorkflow.value.id, updateData)
        await loadWorkflows()
        ElMessage.success('更新成功')
      } else {
        const createData: CreateWorkflowRequest = {
          name: workflowForm.value.name,
          description: workflowForm.value.description,
          category: workflowForm.value.category,
          http_method: workflowForm.value.http_method,
          n8n_webhook_url: workflowForm.value.n8n_webhook_url,
          icon: workflowForm.value.icon
        }
        await WorkflowManagementApi.createWorkflow(createData)
        await loadWorkflows()
        ElMessage.success('创建成功')
      }
      
      showCreateDialog.value = false
      showEditDialog.value = false
      resetForm()
    } catch (error) {
      ElMessage.error('保存失败')
    } finally {
      loading.value = false
    }
  }

  const resetForm = () => {
    workflowForm.value = {
      name: '',
      description: '',
      category: '办公助手',
      http_method: 'POST',
      n8n_webhook_url: '',
      icon: ''
    }
    currentWorkflow.value = null
  }

  const handleSizeChange = (size: number) => {
    pageSize.value = size
    currentPage.value = 1
  }

  const handleCurrentChange = (page: number) => {
    currentPage.value = page
  }

  const handleRefresh = () => {
    loadWorkflows(true)
  }

  return {
    workflows,
    loading,
    searchQuery,
    currentPage,
    pageSize,
    totalWorkflows,
    showCreateDialog,
    showEditDialog,
    workflowForm,
    paginatedWorkflows,
    loadWorkflows,
    editWorkflow,
    deleteWorkflow,
    saveWorkflow,
    handleSizeChange,
    handleCurrentChange,
    handleRefresh
  }
}
