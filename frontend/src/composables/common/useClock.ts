import { ref, onMounted, onBeforeUnmount } from 'vue'

/**
 * 共享时钟 composable，提供当前时间和日期（中文格式）
 * 每分钟自动更新一次
 */
export function useClock() {
  const currentTime = ref('')
  const currentDate = ref('')
  let timer: ReturnType<typeof setInterval> | null = null

  function updateTime() {
    const now = new Date()
    currentTime.value = now.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
    currentDate.value = now.toLocaleDateString('zh-CN', { month: 'long', day: 'numeric', weekday: 'short' })
  }

  onMounted(() => {
    updateTime()
    timer = setInterval(updateTime, 60_000)
  })

  onBeforeUnmount(() => {
    if (timer) clearInterval(timer)
  })

  return { currentTime, currentDate }
}
