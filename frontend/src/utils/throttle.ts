import { ElMessage } from 'element-plus'

/**
 * 节流函数（带频繁操作提示）
 * @param fn 需要节流的函数
 * @param delay 节流时间（毫秒）
 * @param maxCount 最大连续点击次数
 * @returns 节流后的函数
 */
export function throttleWithWarning<T extends (...args: any[]) => any>(
  fn: T,
  delay: number = 2000,
  maxCount: number = 3
): (...args: Parameters<T>) => void {
  let lastTime = 0
  let clickCount = 0
  let resetTimer: ReturnType<typeof setTimeout> | null = null

  return function (this: any, ...args: Parameters<T>) {
    const now = Date.now()
    
    // 检查是否在节流时间内
    if (now - lastTime < delay) {
      clickCount++
      
      // 超过最大点击次数，提示用户
      if (clickCount >= maxCount) {
        ElMessage.warning('操作太频繁啦，请稍后再试 😊')
        return
      }
      return
    }
    
    // 重置计数器
    clickCount = 0
    lastTime = now
    
    // 5秒后重置点击计数
    if (resetTimer) clearTimeout(resetTimer)
    resetTimer = setTimeout(() => {
      clickCount = 0
    }, 5000)
    
    fn.apply(this, args)
  }
}
