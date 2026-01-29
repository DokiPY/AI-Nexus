<template>
  <el-row :gutter="20">
    <el-col :xs="12" :sm="12" :md="6" :lg="6" :xl="6">
      <div class="stat-card blue">
        <div class="icon-wrapper">
          <el-icon><ChatDotRound /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ overview.total_messages.toLocaleString() }}</div>
          <div class="stat-label">总对话次数</div>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :md="6" :lg="6" :xl="6">
      <div class="stat-card green">
        <div class="icon-wrapper">
          <el-icon><User /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ overview.active_users.toLocaleString() }}</div>
          <div class="stat-label">活跃用户数</div>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :md="6" :lg="6" :xl="6">
      <div class="stat-card orange">
        <div class="icon-wrapper">
          <el-icon><Timer /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ overview.avg_response_time }}<span class="unit">ms</span></div>
          <div class="stat-label">平均响应时间</div>
        </div>
      </div>
    </el-col>
    <el-col :xs="12" :sm="12" :md="6" :lg="6" :xl="6">
      <div class="stat-card purple">
        <div class="icon-wrapper">
          <el-icon><TrendCharts /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ overview.today_messages.toLocaleString() }}</div>
          <div class="stat-label">今日对话量</div>
        </div>
      </div>
    </el-col>
  </el-row>
</template>

<script setup lang="ts">
import { ChatDotRound, User, Timer, TrendCharts } from '@element-plus/icons-vue'
import type { StatisticsOverview } from '../../../services/admin/statistics'

defineProps<{
  overview: StatisticsOverview
}>()
</script>

<style scoped>
.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s ease;
  border: 1px solid rgba(0,0,0,0.04);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
  height: 100%;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08), 0 4px 6px -2px rgba(0, 0, 0, 0.04);
}

.icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  flex-shrink: 0;
}

/* 颜色主题 */
.stat-card.blue .icon-wrapper { background: #eff6ff; color: #3b82f6; }
.stat-card.green .icon-wrapper { background: #ecfdf5; color: #10b981; }
.stat-card.orange .icon-wrapper { background: #fffbeb; color: #f59e0b; }
.stat-card.purple .icon-wrapper { background: #f3e8ff; color: #8b5cf6; }

.stat-content {
  flex: 1;
  min-width: 0;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  line-height: 1.2;
  margin-bottom: 4px;
  font-family: 'Inter', sans-serif;
  letter-spacing: -0.5px;
}

.unit {
  font-size: 16px;
  font-weight: 500;
  color: #94a3b8;
  margin-left: 4px;
}

.stat-label {
  font-size: 14px;
  font-weight: 500;
  color: #64748b;
}

@media (max-width: 768px) {
  .stat-card {
    padding: 16px;
    gap: 16px;
    border-radius: 12px;
  }
  
  .icon-wrapper {
    width: 48px;
    height: 48px;
    font-size: 24px;
    border-radius: 12px;
  }
  
  .stat-value {
    font-size: 24px;
  }
}
</style>
