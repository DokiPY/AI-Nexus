<!--
 * @component WorkflowManagement
 * @description 工作流管理页面
-->
<template>
  <div class="workflow-management">
    <ContentContainer>
      <ActionBar
        :search-query="searchQuery"
        :loading="loading"
        create-button-text="新建工作流"
        create-button-variant="soft"
        search-placeholder="搜索工作流..."
        @update:search-query="searchQuery = $event"
        @create="showCreateDialog = true"
        @refresh="handleRefresh"
      />

      <div class="table-wrapper">
        <WorkflowTable
          :workflows="paginatedWorkflows"
          :loading="loading"
          :current-page="currentPage"
          :page-size="pageSize"
          @edit="editWorkflow"
          @delete="deleteWorkflow"
        />
      </div>

      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="totalWorkflows"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </ContentContainer>

    <WorkflowFormDialog
      v-model:visible="showCreateDialog"
      :form="workflowForm"
      :is-edit="false"
      @save="saveWorkflow"
    />

    <WorkflowFormDialog
      v-model:visible="showEditDialog"
      :form="workflowForm"
      :is-edit="true"
      @save="saveWorkflow"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { ContentContainer, ActionBar, WorkflowTable, WorkflowFormDialog } from '@/components'
import { useWorkflowManagement } from '@/composables'

const {
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
} = useWorkflowManagement()

onMounted(() => {
  loadWorkflows()
})
</script>

<style scoped>
.workflow-management {
  height: calc(100vh - 70px - 48px);
  display: flex;
  flex-direction: column;
}

.table-wrapper {
  flex: 1;
  overflow: auto;
  min-height: 0;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
  flex-shrink: 0;
}
</style>