<template>
  <div class="user-management">
    <ContentContainer>
      <ActionBar
        :search-query="searchQuery"
        :loading="loading"
        create-button-text="新增用户"
        create-button-variant="soft"
        search-placeholder="搜索用户名、邮箱..."
        @update:search-query="searchQuery = $event"
        @create="showCreateDialog = true"
        @refresh="handleRefresh"
      >
        <template #right-extra>
          <div class="filters">
            <el-select 
              v-model="roleFilter" 
              class="filter-select" 
              placeholder="角色" 
              :teleported="false"
              clearable
            >
              <el-option label="管理员" value="admin" />
              <el-option label="普通用户" value="user" />
            </el-select>

            <el-select 
              v-model="statusFilter" 
              class="filter-select" 
              placeholder="状态" 
              :teleported="false"
              clearable
            >
              <el-option label="启用" value="active" />
              <el-option label="禁用" value="inactive" />
            </el-select>
          </div>
        </template>
      </ActionBar>

      <div class="table-wrapper">
        <UserTable
          :users="paginatedUsers"
          :loading="loading"
          :current-page="currentPage"
          :page-size="pageSize"
          @sort-change="handleSortChange"
          @edit="editUser"
          @delete="deleteUser"
          @manage-workflows="manageWorkflows"
          @reset-password="resetPassword"
        />
      </div>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="totalUsers"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </ContentContainer>

    <UserFormDialog
      v-model:visible="showCreateDialog"
      :form="userForm"
      :companies="companies"
      :is-edit="false"
      @save="saveUser"
    />

    <UserFormDialog
      v-model:visible="showEditDialog"
      :form="userForm"
      :companies="companies"
      :is-edit="true"
      @save="saveUser"
    />

    <WorkflowPermissionDialog
      v-model:visible="showWorkflowDialog"
      :selected-user="selectedUser"
      :workflows="availableWorkflows"
      :selected-workflows="selectedWorkflows"
      @update:selected-workflows="selectedWorkflows = $event"
      @save="saveWorkflowPermissions"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { ContentContainer, ActionBar, UserTable, UserFormDialog, WorkflowPermissionDialog } from '@/components'
import { useUserManagement } from '@/composables'

const {
  companies,
  availableWorkflows,
  loading,
  searchQuery,
  roleFilter,
  statusFilter,
  // companyIdsFilter and hasActiveFilters are not used in template
  currentPage,
  pageSize,
  totalUsers,
  showCreateDialog,
  showEditDialog,
  showWorkflowDialog,
  selectedUser,
  selectedWorkflows,
  userForm,
  paginatedUsers,
  loadUsers,
  loadCompanies,
  editUser,
  deleteUser,
  resetPassword,
  manageWorkflows,
  saveUser,
  saveWorkflowPermissions,
  handleSizeChange,
  handleCurrentChange,
  // clearFilters is not used in template
  handleSortChange,
  handleRefresh
} = useUserManagement()

onMounted(() => {
  loadUsers()
  loadCompanies()
})
</script>

<style scoped>
.user-management {
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

.filters {
  display: inline-flex;
  gap: 8px;
  align-items: center;
}

.filter-select {
  width: 110px;
}

/* 筛选框样式与搜索框完全一致 - 直接复制 ActionBar 的 search-input 样式 */
.filter-select :deep(.el-input__wrapper) {
  border-radius: 10px;
  box-shadow: none;
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.08);
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
  height: 40px;
}

.filter-select :deep(.el-input__wrapper.is-focus) {
  border-color: rgba(59, 130, 246, 0.4);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.08);
  background: #ffffff;
}
</style>
