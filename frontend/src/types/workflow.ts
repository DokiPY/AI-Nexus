export interface Workflow {
  id: string
  name: string
  description: string
  icon: string
  color: string
  category: string
  status: 'active' | 'maintenance'
}

export interface WorkflowFilters {
  searchQuery: string
  currentCategory: string
}