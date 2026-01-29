<template>
  <el-card>
    <template #header>
      <span class="chart-title">用户活跃度（公司 / 员工）</span>
    </template>
    <div class="chart-wrapper">
      <EmptyChart 
        v-if="!data || data.length === 0"
        title="暂无用户活跃数据"
        description="当用户开始使用系统后，这里将显示活跃度排行"
      />
      <div v-else ref="chartRef" class="chart-container"></div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, nextTick } from 'vue'
import * as echarts from 'echarts'
import EmptyChart from './EmptyChart.vue'
import type { CompanyUserActivity } from '../../../services/admin/statistics'

const props = defineProps<{
  data: CompanyUserActivity[]
}>()

const chartRef = ref<HTMLElement>()
let chart: echarts.ECharts | null = null

const makeLabel = (d: CompanyUserActivity) => `${d.company_name} / ${d.username}`

const initChart = () => {
  if (!chartRef.value) return
  chart = echarts.init(chartRef.value)
  updateChart()
}

const updateChart = () => {
  if (!chart || !props.data || props.data.length === 0) return

  const labels = props.data.map(makeLabel)
  const values = props.data.map(d => d.message_count)

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
        if (!d) return ''
        const last = d.last_active_at ? new Date(d.last_active_at).toLocaleString() : '-'
        return [
          `<div style="font-weight: 600; margin-bottom: 4px;">${makeLabel(d)}</div>`,
          `用户消息数：${d.message_count ?? 0}`,
          `最后活跃：${last}`
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
      name: '消息数',
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
          { offset: 0, color: '#8b5cf6' },
          { offset: 1, color: '#6366f1' }
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
