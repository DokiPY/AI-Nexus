<template>
  <el-card>
    <template #header>
      <span class="chart-title">响应耗时排行（按工作流 / 平均耗时）</span>
    </template>
    <div class="chart-wrapper">
      <EmptyChart 
        v-if="!data || data.length === 0"
        title="暂无响应耗时数据"
        description="当有AI响应记录后，这里将显示各工作流的响应耗时"
      />
      <div v-else ref="chartRef" class="chart-container"></div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import EmptyChart from './EmptyChart.vue'
import type { ResponseTimeByWorkflow } from '../../../services/admin/statistics'

const props = defineProps<{
  data: ResponseTimeByWorkflow[]
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

  const labels = props.data.map(d => d.workflow_name)
  const values = props.data.map(d => Number((d.avg_response_time_ms / 1000).toFixed(2)))

  const option: echarts.EChartsOption = {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#e2e8f0',
      textStyle: { color: '#1e293b' },
      extraCssText: 'box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); border-radius: 8px;',
      formatter: (params: any) => {
        const p = Array.isArray(params) ? params[0] : params
        const idx = p?.dataIndex ?? 0
        const d = props.data[idx]
        const avgS = (d?.avg_response_time_ms ?? 0) / 1000
        const maxS = (d?.max_response_time_ms ?? 0) / 1000
        return [
          `<div style="font-weight: 600; margin-bottom: 4px;">${d?.workflow_name ?? '-'}</div>`,
          `平均耗时：${avgS.toFixed(2)}s`,
          `最大耗时：${maxS.toFixed(2)}s`,
          `样本数：${d?.count ?? 0}`
        ].join('<br/>')
      }
    },
    grid: { left: 20, right: 20, top: 30, bottom: 60, containLabel: true },
    xAxis: {
      type: 'category',
      data: labels,
      axisLine: { show: false },
      axisTick: { show: false },
      axisLabel: {
        interval: 0,
        rotate: 25,
        color: '#64748b',
        formatter: (value: string) => (value.length > 12 ? `${value.slice(0, 12)}…` : value)
      }
    },
    yAxis: {
      type: 'value',
      name: '秒(s)',
      nameTextStyle: { color: '#94a3b8', padding: [0, 0, 0, 20] },
      minInterval: 1,
      splitLine: {
        lineStyle: { type: 'dashed', color: '#f1f5f9' }
      },
      axisLabel: { color: '#94a3b8' }
    },
    series: [{
      type: 'bar',
      barWidth: 20,
      data: values,
      itemStyle: {
        borderRadius: [4, 4, 0, 0],
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#10b981' },
          { offset: 1, color: '#059669' }
        ])
      },
      showBackground: true,
      backgroundStyle: {
        color: '#f8fafc',
        borderRadius: [4, 4, 0, 0]
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

const handleResize = () => chart?.resize()

onMounted(() => {
  if (props.data && props.data.length > 0) {
    initChart()
  }
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
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
    min-height: 260px;
  }
  
  .chart-container {
    height: 260px;
  }
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}
</style>
