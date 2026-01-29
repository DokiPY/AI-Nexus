// 刷新控制通用 Hook

import { ref } from 'vue'
import { ElMessage } from 'element-plus'

/**
 * 刷新控制 Hook
 * 提供频繁刷新检测和最小 loading 时间
 */
export function useRefreshControl() {
  const loading = ref(false)
  let lastRefreshTime = 0
  let refreshCount = 0
  let refreshCountTimer: ReturnType<typeof setTimeout> | null = null

  /**
   * 执行刷新操作
   * @param loadFn 加载数据的函数
   * @param showSuccessMsg 是否显示成功提示
   * @param minDelay 最小 loading 时间（毫秒）
   */
  const executeRefresh = async (
    loadFn: () => Promise<void>,
    showSuccessMsg = false,
    minDelay = 300
  ) => {
    if (loading.value) return

    // 频繁刷新检测
    const now = Date.now()
    if (showSuccessMsg) {
      if (now - lastRefreshTime < 3000) {
        refreshCount++
        if (refreshCount >= 3) {
          ElMessage.warning('刷新太频繁啦，休息一下吧 😊')
          return
        }
      } else {
        refreshCount = 0
      }
      lastRefreshTime = now

      if (refreshCountTimer) clearTimeout(refreshCountTimer)
      refreshCountTimer = setTimeout(() => {
        refreshCount = 0
      }, 5000)
    }

    loading.value = true

    // 最小loading时间,让用户有感知
    const startTime = Date.now()

    try {
      await loadFn()

      const elapsed = Date.now() - startTime

      if (elapsed < minDelay) {
        await new Promise(resolve => setTimeout(resolve, minDelay - elapsed))
      }

      if (showSuccessMsg) {
        ElMessage.success('刷新成功')
      }
    } finally {
      loading.value = false
    }
  }

  return {
    loading,
    executeRefresh
  }
}
