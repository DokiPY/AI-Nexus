<template>
  <div class="chat-container">
    <div class="chat-header">
      <div class="chat-header-left">
        <div class="header-icon">
          {{ (workflow?.name?.[0] || 'W').toUpperCase() }}
        </div>
        <div class="header-info">
          <strong class="chat-title">{{ workflow.name }}</strong>
          <div class="status-indicator">
            <span class="status-dot"></span>
            <span class="status-text">Ready to chat</span>
          </div>
        </div>
      </div>
      <div class="chat-header-actions">
        <el-tooltip content="清空对话" placement="bottom">
          <button class="action-btn" type="button" @click="$emit('clear-messages')">
            <el-icon><Delete /></el-icon>
          </button>
        </el-tooltip>
      </div>
    </div>

    <div class="chat-body" ref="chatBody">
      <div v-if="messages.length === 0" class="chat-welcome">
        <div class="welcome-icon">👋</div>
        <h3>你好，我是 {{ workflow.name }}</h3>
        <p>{{ workflow.description || '我可以帮你处理任务，请直接告诉我你的需求。' }}</p>
      </div>

      <div
        v-for="(msg, idx) in messages"
        :key="idx"
        :class="['msg-row', msg.role]"
      >
        <div class="avatar">
          <img v-if="msg.role === 'user'" :src="userAvatar" alt="User" class="user-avatar" />
          <span v-else>{{ (workflow?.name?.[0] || 'A').toUpperCase() }}</span>
        </div>
        <div class="msg-content">
          <div class="bubble" :class="{ 'markdown-body': msg.role === 'agent' }">
            <div v-if="msg.role === 'agent'" v-html="renderMarkdown(msg.content)"></div>
            <div v-else>{{ msg.content }}</div>
          </div>
        </div>
      </div>

      <div v-if="isTyping" class="msg-row agent">
        <div class="avatar">
          <span>{{ (workflow?.name?.[0] || 'A').toUpperCase() }}</span>
        </div>
        <div class="msg-content">
          <div class="bubble typing">
            <div class="dot-flashing"></div>
          </div>
        </div>
      </div>
    </div>

    <div class="chat-footer">
      <div class="input-wrapper">
        <el-input
          :model-value="inputMessage"
          @update:model-value="$emit('update:inputMessage', $event)"
          placeholder="输入消息..."
          @keyup.enter.exact="$emit('send-message')"
          class="chat-input-field"
          type="textarea"
          :autosize="{ minRows: 1, maxRows: 4 }"
          resize="none"
        />
        <el-button
          class="send-btn"
          type="primary"
          :icon="Position"
          :loading="isTyping"
          :disabled="isTyping || !inputMessage.trim()"
          circle
          @click="$emit('send-message')"
        />
      </div>
      <div class="footer-note">Press Enter to send</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, nextTick, computed } from 'vue'
import { Position, Delete } from '@element-plus/icons-vue'
import { useUserStore } from '../../../stores/login/user'
import { marked } from 'marked'
import 'highlight.js/styles/github.css'

const renderMarkdown = (text: string) => {
  return marked.parse(text, {
    breaks: true,
    gfm: true
  })
}

const props = defineProps<{
  workflow: any
  messages: any[]
  inputMessage: string
  isTyping: boolean
}>()

defineEmits<{
  'clear-messages': []
  'update:inputMessage': [value: string]
  'send-message': []
}>()

const chatBody = ref<HTMLElement>()

const userStore = useUserStore()
const userAvatar = computed(() => 
  `https://api.dicebear.com/7.x/notionists/svg?seed=${userStore.userInfo?.username || 'admin'}&backgroundColor=6366f1`
)

const scrollToBottom = () => {
  nextTick(() => {
    if (chatBody.value) {
      chatBody.value.scrollTo({
        top: chatBody.value.scrollHeight,
        behavior: 'smooth'
      })
    }
  })
}

watch(() => props.messages.length, scrollToBottom)
watch(() => props.isTyping, scrollToBottom)

defineExpose({
  scrollToBottom
})
</script>

<style scoped>
.chat-container {
  width: 100%;
  height: 100%;
  background: transparent;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

/* Header */
.chat-header {
  padding: 14px 16px;
  border-bottom: 1px solid #e5e7eb;
  border-radius: 14px 14px 0 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 15px;
  background: #ffffff;
  box-shadow: 0 8px 24px rgba(17, 24, 39, 0.06);
  margin-top: 12px;
}

.header-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
  color: #3b82f6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
}

.chat-header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-info {
  display: flex;
  flex-direction: column;
}

.chat-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
}

.status-indicator {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-top: 2px;
}

.status-dot {
  width: 6px;
  height: 6px;
  background: #10b981;
  border-radius: 50%;
  box-shadow: 0 0 0 2px rgba(16, 185, 129, 0.2);
}

.status-text {
  font-size: 12px;
  color: #64748b;
}

.action-btn {
  width: 36px;
  height: 36px;
  border: none;
  background: transparent;
  border-radius: 8px;
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.action-btn:hover {
  background: #f1f5f9;
  color: #ef4444;
}

/* Body */
.chat-body {
  flex: 1;
  padding: 18px 16px;
  overflow-y: auto;
  scroll-behavior: smooth;
  background: #ffffff;
  border-left: 1px solid #e5e7eb;
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.chat-welcome {
  text-align: center;
  margin-top: 40px;
  margin-bottom: 20px;
  color: #64748b;
  opacity: 0;
  animation: fadeIn 0.8s ease forwards;
}

.welcome-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.chat-welcome h3 {
  color: #1e293b;
  font-size: 18px;
  margin-bottom: 8px;
}

.msg-row {
  display: flex;
  gap: 16px;
  max-width: 85%;
  opacity: 0;
  animation: slideIn 0.3s ease forwards;
}

.msg-row.user {
  align-self: flex-end;
  flex-direction: row-reverse;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 14px;
  font-weight: 600;
}

.msg-row.agent .avatar {
  background: #f1f5f9;
  color: #475569;
}

.msg-row.user .avatar {
  background: transparent;
  padding: 0;
}

.user-avatar {
  width: 100%;
  height: 100%;
  border-radius: 10px;
  object-fit: cover;
}

.bubble {
  padding: 12px 18px;
  border-radius: 16px;
  font-size: 15px;
  line-height: 1.6;
  position: relative;
  word-wrap: break-word;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

.msg-row.agent .bubble {
  /* 调整为 Slate-100 经典灰底，保证与白色背景有足够对比度 */
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  color: #1e293b;
  border-top-left-radius: 2px;
  /* 阴影保持轻微，避免脏感 */
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.msg-row.user .bubble {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-top-right-radius: 2px;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15);
}

/* Typing Indicator */
.dot-flashing {
  position: relative;
  width: 6px;
  height: 6px;
  border-radius: 5px;
  background-color: #94a3b8;
  color: #94a3b8;
  animation: dot-flashing 1s infinite linear alternate;
  animation-delay: 0.5s;
  margin: 0 8px;
}
.dot-flashing::before, .dot-flashing::after {
  content: "";
  display: inline-block;
  position: absolute;
  top: 0;
  width: 6px;
  height: 6px;
  border-radius: 5px;
  background-color: #94a3b8;
  color: #94a3b8;
  animation: dot-flashing 1s infinite alternate;
}
.dot-flashing::before { left: -10px; animation-delay: 0s; }
.dot-flashing::after { left: 10px; animation-delay: 1s; }

@keyframes dot-flashing {
  0% { background-color: #94a3b8; }
  50%, 100% { background-color: #cbd5e1; }
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
  to { opacity: 1; }
}

/* Footer */
.chat-footer {
  padding: 12px 14px;
  border: 1px solid #e5e7eb;
  border-top: none;
  background: #ffffff;
  border-radius: 0 0 14px 14px;
  box-shadow: 0 8px 24px rgba(17, 24, 39, 0.06);
}

.input-wrapper {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 24px;
  padding: 4px;
  padding-left: 14px;
  display: flex;
  align-items: flex-end;
  gap: 8px;
  transition: all 0.2s;
  box-shadow: none;
}

.input-wrapper:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.chat-input-field :deep(.el-textarea__inner) {
  box-shadow: none !important;
  padding: 8px 0;
  background: transparent;
  border: none;
  resize: none;
  font-size: 15px;
  line-height: 1.5;
  color: #1e293b;
}

.chat-input-field :deep(.el-textarea__inner::placeholder) {
  color: #94a3b8;
}

.send-btn {
  width: 40px;
  height: 40px !important;
  margin-bottom: 2px;
  font-size: 18px;
}

.footer-note {
  text-align: center;
  font-size: 12px;
  color: #cbd5e1;
  margin-top: 8px;
}

/* Markdown 样式 */
.markdown-body {
  font-size: 15px;
  line-height: 1.7;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  margin-top: 16px;
  margin-bottom: 8px;
  font-weight: 600;
  color: #1e293b;
}

.markdown-body :deep(h1) { font-size: 20px; }
.markdown-body :deep(h2) { font-size: 18px; }
.markdown-body :deep(h3) { font-size: 16px; }

.markdown-body :deep(p) {
  margin: 8px 0;
}

.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  margin: 8px 0;
  padding-left: 24px;
}

.markdown-body :deep(li) {
  margin: 4px 0;
}

.markdown-body :deep(strong) {
  font-weight: 600;
  color: #0f172a;
}

.markdown-body :deep(code) {
  background: #f1f5f9;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 14px;
  font-family: 'Consolas', 'Monaco', monospace;
  color: #e11d48;
}

.markdown-body :deep(pre) {
  background: #1e293b;
  padding: 12px;
  border-radius: 8px;
  overflow-x: auto;
  margin: 12px 0;
}

.markdown-body :deep(pre code) {
  background: transparent;
  padding: 0;
  color: #e2e8f0;
  font-size: 13px;
}

.markdown-body :deep(blockquote) {
  border-left: 3px solid #3b82f6;
  padding-left: 12px;
  margin: 12px 0;
  color: #64748b;
}

.markdown-body :deep(a) {
  color: #3b82f6;
  text-decoration: none;
}

.markdown-body :deep(a:hover) {
  text-decoration: underline;
}
</style>