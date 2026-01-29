<template>
  <el-card>
    <template #header>
      <span class="chart-title">工作流使用排行</span>
    </template>
    <div class="chart-wrapper">
      <EmptyChart 
        v-if="!data || data.length === 0"
        title="暂无工作流使用数据"
        description="当用户开始使用工作流后，这里将显示使用排行"
      />
      <div v-else ref="chartRef" class="chart-container"></div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import EmptyChart from './EmptyChart.vue'
import type { WorkflowRanking } from '../../../services/admin/statistics'

const props = defineProps<{
  data: WorkflowRanking[]
}>()

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

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
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e2e8f0',
      textStyle: { color: '#1e293b' },
      extraCssText: 'box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border-radius: 8px;'
    },
    grid: {
      top: 10,
      right: 30,
      bottom: 20,
      left: 10,
      containLabel: true
    },
    xAxis: {
      type: 'value',
      splitLine: {
        lineStyle: { type: 'dashed', color: '#f1f5f9' }
      },
      axisLabel: { color: '#94a3b8' }
    },
    yAxis: {
      type: 'category',
      data: props.data.map(d => d.workflow_name).reverse(),
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        color: '#64748b',
        fontWeight: 500,
        formatter: (val: string) => val.length > 8 ? val.slice(0, 8) + '...' : val
      }
    },
    series: [{
      type: 'bar',
      barWidth: 20,
      data: props.data.map(d => d.usage_count).reverse(),
      itemStyle: {
        borderRadius: [0, 10, 10, 0],
        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
          { offset: 0, color: '#60a5fa' },
          { offset: 1, color: '#3b82f6' }
        ])
      },
      showBackground: true,
      backgroundStyle: {
        color: '#f8fafc',
        borderRadius: [0, 10, 10, 0]
      }
    }]
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
.chart-wrapper {
  min-height: 300px;
  width: 100%;
}

.chart-container {
  height: 300px;
  width: 100%;
}

@media (max-width: 768px) {
  .chart-wrapper {
    min-height: 250px;
  }
  
  .chart-container {
    height: 250px;
  }
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}
</style>
