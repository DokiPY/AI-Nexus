<template>
  <el-card>
    <template #header>
      <div class="card-header">
        <span class="title">对话趋势</span>
        <div class="time-switch">
          <div 
            class="switch-item" 
            :class="{ active: days === 7 }" 
            @click="handleChange(7)"
          >
            最近7天
          </div>
          <div 
            class="switch-item" 
            :class="{ active: days === 30 }" 
            @click="handleChange(30)"
          >
            最近30天
          </div>
        </div>
      </div>
    </template>
    <div v-loading="loading" class="chart-wrapper">
      <div v-if="!loading && (!data || data.length === 0)" class="empty-state">
        <el-icon class="empty-icon"><DataLine /></el-icon>
        <p class="empty-text">暂无对话数据</p>
        <p class="empty-hint">当用户开始使用工作流后，这里将显示对话趋势</p>
      </div>
      <div v-else ref="chartRef" class="chart-container"></div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue'
import { DataLine } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import type { ChatTrend } from '../../../services/admin/statistics'

const props = defineProps<{
  data: ChatTrend[]
  loading?: boolean
}>()

const emit = defineEmits<{
  change: [days: number]
}>()

const days = ref(7)
const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

const handleChange = (val: number) => {
  if (days.value === val) return
  days.value = val
  emit('change', val)
}

const initChart = () => {
  if (!chartRef.value) return
  chart = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chart || !props.data || props.data.length === 0) return
  
  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e2e8f0',
      textStyle: { color: '#1e293b' },
      extraCssText: 'box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border-radius: 8px;'
    },
    legend: {
      data: ['用户消息', 'AI响应'],
      bottom: 0,
      icon: 'circle',
      itemGap: 24,
      textStyle: { color: '#64748b' }
    },
    grid: {
      top: 30,
      right: 20,
      bottom: 40,
      left: 20,
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: props.data.map(d => d.date),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: { color: '#94a3b8', margin: 12 }
    },
    yAxis: {
      type: 'value',
      minInterval: 1,
      splitLine: {
        lineStyle: { type: 'dashed', color: '#f1f5f9' }
      },
      axisLabel: { color: '#94a3b8' }
    },
    series: [
      {
        name: '用户消息',
        type: 'line',
        data: props.data.map(d => d.user_messages),
        smooth: 0.4,
        showSymbol: true,
        symbol: 'circle',
        symbolSize: 8,
        itemStyle: { color: '#3b82f6' },
        lineStyle: { width: 3 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(59, 130, 246, 0.2)' },
            { offset: 1, color: 'rgba(59, 130, 246, 0)' }
          ])
        }
      },
      {
        name: 'AI响应',
        type: 'line',
        data: props.data.map(d => d.ai_messages),
        smooth: 0.4,
        showSymbol: true,
        symbol: 'circle',
        symbolSize: 8,
        itemStyle: { color: '#10b981' },
        lineStyle: { width: 3 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(16, 185, 129, 0.2)' },
            { offset: 1, color: 'rgba(16, 185, 129, 0)' }
          ])
        }
      }
    ]
  }
  
  chart.setOption(option)
}

watch(() => props.data, async () => {
  if (props.data && props.data.length > 0) {
    await nextTick()
    if (!chart) {
      initChart()
    } else {
      updateChart()
    }
  }
}, { deep: true })

onMounted(() => {
  if (props.data && props.data.length > 0) {
    initChart()
  }
  window.addEventListener('resize', () => chart?.resize())
})

onUnmounted(() => {
  chart?.dispose()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
}

.title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.time-switch {
  display: flex;
  background: #f1f5f9;
  padding: 3px;
  border-radius: 8px;
}

.switch-item {
  padding: 4px 12px;
  font-size: 13px;
  color: #64748b;
  cursor: pointer;
  border-radius: 6px;
  transition: all 0.2s ease;
  user-select: none;
  font-weight: 500;
}

.switch-item:hover {
  color: #334155;
}

.switch-item.active {
  background: white;
  color: #3b82f6;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
  font-weight: 600;
}

.chart-wrapper {
  min-height: 300px;
  width: 100%;
  position: relative;
}

.chart-container {
  height: 300px;
  width: 100%;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  color: #94a3b8;
}

.empty-icon {
  font-size: 64px;
  color: #cbd5e1;
  margin-bottom: 16px;
}

.empty-text {
  font-size: 16px;
  font-weight: 500;
  color: #64748b;
  margin: 0 0 8px 0;
}

.empty-hint {
  font-size: 13px;
  color: #94a3b8;
  margin: 0;
  max-width: 300px;
  text-align: center;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .chart-container {
    height: 250px;
  }
  
  .chart-wrapper {
    min-height: 250px;
  }
  
  .empty-state {
    height: 250px;
  }
  
  .card-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
</style>
