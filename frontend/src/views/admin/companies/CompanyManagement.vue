<template>
  <div class="company-management">
    <ContentContainer>
      <ActionBar
        :search-query="searchQuery"
        :loading="loading"
        create-button-text="新增公司"
        create-button-variant="soft"
        search-placeholder="搜索公司名称..."
        @update:search-query="searchQuery = $event"
        @create="showCreateDialog = true"
        @refresh="handleRefresh"
      />

      <div class="table-wrapper">
        <CompanyTable
          :companies="paginatedCompanies"
          :loading="loading"
          @edit="editCompany"
          @delete="deleteCompany"
          @view-users="viewUsers"
        />
      </div>

      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="totalCompanies"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </ContentContainer>

    <CompanyFormDialog
      v-model:visible="showCreateDialog"
      :form="companyForm"
      :is-edit="false"
      @save="saveCompany"
    />

    <CompanyFormDialog
      v-model:visible="showEditDialog"
      :form="companyForm"
      :is-edit="true"
      @save="saveCompany"
    />

    <CompanyUsersDialog
      v-model:visible="showUsersDialog"
      :company-name="selectedCompany?.name || ''"
      :users="companyUsers"
      :loading="loadingUsers"
    />
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { ContentContainer, ActionBar, CompanyTable, CompanyFormDialog, CompanyUsersDialog } from '@/components'
import { useCompanyManagement } from '@/composables'
import { useAdminDataStore } from '../../../stores'

const { loadCompanies: loadCompaniesFromStore } = useAdminDataStore()

const {
  loading,
  searchQuery,
  currentPage,
  pageSize,
  totalCompanies,
  showCreateDialog,
  showEditDialog,
  showUsersDialog,
  companyForm,
  paginatedCompanies,
  selectedCompany,
  companyUsers,
  loadingUsers,
  loadCompanies,
  editCompany,
  deleteCompany,
  saveCompany,
  handleSizeChange,
  handleCurrentChange,
  handleRefresh,
  viewUsers
} = useCompanyManagement()

onMounted(() => {
  loadCompaniesFromStore()
  loadCompanies()
})
</script>

<style scoped>
.company-management {
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
