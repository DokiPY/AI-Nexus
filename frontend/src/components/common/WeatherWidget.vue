<!--
 * @component WeatherWidget
 * @description 共享时间天气小组件 - 旋转太阳 + 时间日期
 * 用于 AdminSidebar 和 WorkflowSidebar 底部
-->
<template>
  <div class="weather-widget" :class="{ mini: mini }">
    <div class="weather-icon-box">
      <svg class="weather-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="5" />
        <line x1="12" y1="1" x2="12" y2="3" />
        <line x1="12" y1="21" x2="12" y2="23" />
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
        <line x1="1" y1="12" x2="3" y2="12" />
        <line x1="21" y1="12" x2="23" y2="12" />
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
      </svg>
    </div>
    <div class="time-info">
      <div class="current-time">{{ currentTime }}</div>
      <div class="current-date">{{ currentDate }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useClock } from '../../composables/common/useClock'

defineProps<{
  mini?: boolean
}>()

const { currentTime, currentDate } = useClock()
</script>

<style scoped>
.weather-widget {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 10px 12px;
  border-radius: 12px;
  transition: all 0.2s ease;
  color: #64748b;
}

.weather-widget:hover {
  background: rgba(59, 130, 246, 0.04);
}

.weather-widget.mini {
  justify-content: center;
  padding: 10px 0;
  gap: 0;
}

.weather-icon-box {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  color: #f59e0b;
}

.weather-icon {
  width: 28px;
  height: 28px;
  animation: weather-spin 10s linear infinite;
}

@keyframes weather-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.time-info {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  transition: opacity 0.2s, transform 0.2s;
  opacity: 1;
  transform: translateX(0);
}

.weather-widget.mini .time-info {
  opacity: 0;
  transform: translateX(10px);
  position: absolute;
  pointer-events: none;
}

.current-time {
  font-size: 1.2rem;
  font-weight: 700;
  color: #334155;
  line-height: 1.2;
  font-family: 'Inter', sans-serif;
  letter-spacing: -0.5px;
}

.current-date {
  font-size: 0.78rem;
  color: #64748b;
  margin-top: 3px;
  white-space: nowrap;
}
</style>
