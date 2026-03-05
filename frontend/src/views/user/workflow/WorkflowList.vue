<template>
  <div class="workflow-layout">
    <AppHeader @logout="logout" />

    <div class="workspace">
      <WorkflowSidebar
        ref="sidebarRef"
        :collapsed="isSidebarCollapsed"
        :pulse="sidebarPulse"
        :search-query="searchQuery"
        :current-category="currentCategory"
        :categories="categories"
        :workflows="filteredWorkflows"
        :active-workflow-id="activeWorkflow?.id"
        :loading="loading"
        @toggle-collapse="isSidebarCollapsed = !isSidebarCollapsed"
        @update:search-query="searchQuery = $event"
        @update:current-category="currentCategory = $event"
        @select-workflow="selectWorkflow"
      />

      <main class="main">
        <div v-if="!activeWorkflow" class="empty-wrapper">
          <NoWorkflowState v-if="!loading && filteredWorkflows.length === 0" />
          <WorkflowEmptyState
            v-else
            :loading="loading"
            :workflows="filteredWorkflows"
            :sidebar-collapsed="isSidebarCollapsed"
            @open-search="openAndFocusSearch"
            @toggle-sidebar="isSidebarCollapsed = false"
            @select-workflow="selectWorkflow"
          />
        </div>

        <WorkflowChatArea
          v-else
          :workflow="activeWorkflow"
          :messages="messages"
          :input-message="input"
          :is-typing="isTyping"
          @clear-messages="clearMessages"
          @update:input-message="input = $event"
          @send-message="send"
        />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick } from 'vue'
import { AppHeader, WorkflowSidebar, WorkflowChatArea, WorkflowEmptyState, NoWorkflowState } from '@/components'
import { useWorkflowList } from '@/composables'
import { WorkflowApi } from '../../../services/user/workflow/api'
import { ElMessage } from 'element-plus'

const {
  loading,
  searchQuery,
  currentCategory,
  categories,
  filteredWorkflows,
  logout
} = useWorkflowList()

const isSidebarCollapsed = ref(false)
const sidebarPulse = ref(false)
const sidebarRef = ref<any>(null)
const activeWorkflow = ref<any>(null)
const messages = ref<{ role: 'user' | 'agent'; content: string }[]>([])
const input = ref('')
const isTyping = ref(false)
const didAutoSelectDefault = ref(false)
const chatHistoryCache = new Map<number, any[]>() // 聊天历史缓存

const openAndFocusSearch = () => {
  isSidebarCollapsed.value = false
  sidebarPulse.value = true
  setTimeout(() => {
    sidebarPulse.value = false
  }, 900)

  nextTick(() => {
    sidebarRef.value?.focusSearch?.()
  })
}

watch(
  () => [loading.value, filteredWorkflows.value?.length] as const,
  ([isLoading]) => {
    if (didAutoSelectDefault.value) return
    if (isLoading) return
    if (activeWorkflow.value) return
    if (!filteredWorkflows.value?.length) return

    didAutoSelectDefault.value = true
    selectWorkflow(filteredWorkflows.value[0])
  },
  { immediate: true }
)

const selectWorkflow = async (wf: any) => {
  // 如果点击的是当前已选中的，不重复请求
  if (activeWorkflow.value?.id === wf.id) {
    return
  }
  
  activeWorkflow.value = wf
  
  // 先检查缓存
  if (chatHistoryCache.has(wf.id)) {
    messages.value = chatHistoryCache.get(wf.id) || []
    return
  }
  
  messages.value = []
  
  try {
    const history = await WorkflowApi.getChatHistory(wf.id)
    const formattedMessages = history.messages.map(msg => ({
      role: (msg.role === 'user' ? 'user' : 'agent') as 'user' | 'agent',
      content: msg.message
    }))
    
    // 缓存聊天历史
    chatHistoryCache.set(wf.id, formattedMessages)
    messages.value = formattedMessages
  } catch (error: any) {
    ElMessage.error(error.message || '获取聊天历史失败')
  }
}

const clearMessages = async () => {
  if (!activeWorkflow.value) return
  
  try {
    await WorkflowApi.clearChatHistory(activeWorkflow.value.id)
    messages.value = []
    // 清空缓存
    chatHistoryCache.delete(activeWorkflow.value.id)
    ElMessage.success('聊天记录已清空')
  } catch (error: any) {
    ElMessage.error(error.message || '清空失败')
  }
}

const send = async () => {
  if (!input.value.trim() || isTyping.value || !activeWorkflow.value) return

  const userMessage = input.value
  messages.value.push({
    role: 'user',
    content: userMessage,
  })

  input.value = ''
  isTyping.value = true

  try {
    // 等待 SSE 第一个 chunk 到达后再创建 agent 气泡，避免和 typing 动画重叠
    let agentIdx = -1

    const fullText = await WorkflowApi.sendMessageStream(
      activeWorkflow.value.id,
      { message: userMessage },
      (chunk: string) => {
        if (agentIdx === -1) {
          // 收到第一个 chunk：关闭 typing 动画，插入 agent 消息
          isTyping.value = false
          messages.value.push({ role: 'agent', content: chunk })
          agentIdx = messages.value.length - 1
        } else {
          // 后续 chunk：通过替换数组元素触发 Vue 响应式更新
          const prev = messages.value[agentIdx]!
          messages.value[agentIdx] = { role: prev.role, content: prev.content + chunk }
        }
      }
    )

    // 更新缓存
    if (chatHistoryCache.has(activeWorkflow.value.id)) {
      const cached = chatHistoryCache.get(activeWorkflow.value.id) || []
      chatHistoryCache.set(activeWorkflow.value.id, [
        ...cached,
        { role: 'user' as const, content: userMessage },
        { role: 'agent' as const, content: fullText }
      ])
    }
  } catch (error: any) {
    // 出错时显示错误提示
    messages.value.push({ role: 'agent', content: '抱歉，消息发送失败，请稍后重试。' })
    ElMessage.error(error.message || '发送消息失败')
  } finally {
    isTyping.value = false
  }
}
</script>

<style scoped>
.workflow-layout {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #f6f7f9;
  font-family: Inter, -apple-system, sans-serif;
}

.workspace {
  display: flex;
  flex: 1;
  overflow: hidden;
  border-top: 1px solid #eef2f7;
}

.main {
  flex: 1;
  display: flex;
  justify-content: stretch;
  align-items: stretch;
  background: #f6f7f9;
  padding: 0 12px 12px;
  min-width: 0;
}

.empty-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}


</style>
