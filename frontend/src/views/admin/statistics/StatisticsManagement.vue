<!--
 * @component StatisticsManagement
 * @description 数据统计页面
-->
<template>
  <div class="statistics-management">
    <ContentContainer>
      <div v-loading="loading" class="statistics-content">
        <StatisticsCards :overview="overview" />
        
        <el-row :gutter="20" style="margin-top: 20px">
          <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
            <ChatTrendChart 
              :data="chatTrend" 
              :loading="trendLoading"
              @change="handleTrendChange" 
            />
          </el-col>
          <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
            <WorkflowRankingChart :data="workflowRanking" />
          </el-col>
        </el-row>
        
        <el-row :gutter="20" style="margin-top: 20px">
          <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
            <UserActivityChart :data="userActivity" />
          </el-col>
          <el-col :xs="24" :sm="24" :md="12" :lg="12" :xl="12">
            <ResponseTimeByWorkflowChart :data="responseTimeByWorkflow" />
          </el-col>
        </el-row>
      </div>
    </ContentContainer>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { 
  ContentContainer, 
  StatisticsCards, 
  ChatTrendChart, 
  WorkflowRankingChart, 
  UserActivityChart, 
  ResponseTimeByWorkflowChart 
} from '@/components'
import { useStatistics } from '@/composables'
import { throttleWithWarning } from '@/utils'

const {
  loading,
  overview,
  chatTrend,
  workflowRanking,
  userActivity,
  responseTimeByWorkflow,
  loadAllData,
  loadChatTrend
} = useStatistics()

const trendLoading = ref(false)

const handleTrendChange = throttleWithWarning(async (days: number) => {
  trendLoading.value = true
  try {
    await loadChatTrend(days)
  } finally {
    trendLoading.value = false
  }
}, 2000, 3)

onMounted(() => {
  loadAllData()
})
</script>

<style scoped>
.statistics-management {
  /* 这里不要固定高度/在本层滚动：
   * 统计页在小屏会变成单列，内容高度会大于视口；
   * 若外层滚动而 ContentContainer(height:100%) 固定，会导致内容溢出背景。
   * 让滚动交给 AdminDashboard 的 .main-content 即可。
   */
  width: 100%;
}

.statistics-content {
  padding: 20px;
}

@media (max-width: 768px) {
  .statistics-content {
    padding: 10px;
  }
  
  :deep(.el-col) {
    margin-bottom: 20px;
  }
}
</style>
