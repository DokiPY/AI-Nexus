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

    <div class="chat-body-wrapper">
      <div class="chat-body" ref="chatBody" @scroll="handleScroll">
      <div v-if="messages.length === 0" class="chat-welcome">
        <div class="welcome-bubble-wrap">
          <div class="welcome-mascot">
            <img src="../../../assets/ai.png" alt="AI" class="welcome-ai-img" />
          </div>
          <div class="welcome-bubble">
            <h3>Hi, 我是 <span class="welcome-name">{{ workflow.name }}</span></h3>
            <p class="welcome-desc">{{ workflow.description || '有什么我可以帮你的？直接输入你的需求开始对话吧。' }}</p>
          </div>
        </div>
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
          <!-- Agent 消息复制按钮 -->
          <div v-if="msg.role === 'agent' && msg.content" class="msg-actions">
            <button
              class="msg-action-btn"
              :title="copiedIdx === idx ? '已复制' : '复制全部'"
              @click="copyMessage(msg.content, idx)"
            >
              <svg v-if="copiedIdx !== idx" xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
              <svg v-else xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
              <span>{{ copiedIdx === idx ? '已复制' : '复制' }}</span>
            </button>
          </div>
        </div>
      </div>

      <div v-if="isTyping" class="msg-row agent">
        <div class="avatar">
          <span>{{ (workflow?.name?.[0] || 'A').toUpperCase() }}</span>
        </div>
        <div class="msg-content">
          <div class="bubble typing-bubble">
            <span class="dot"></span><span class="dot"></span><span class="dot"></span>
          </div>
        </div>
      </div>
      </div>

      <!-- 回到底部按钮 -->
      <transition name="scroll-btn-fade">
        <button
          v-if="showScrollBtn"
          class="scroll-to-bottom-btn"
          @click="scrollToBottom"
          title="回到底部"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
      </transition>
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
import { ref, watch, nextTick, computed, onMounted, onBeforeUnmount } from 'vue'
import { Position, Delete } from '@element-plus/icons-vue'
import { useUserStore } from '../../../stores/login/user'
import { Marked } from 'marked'
import hljs from 'highlight.js'
import 'highlight.js/styles/github-dark.css'

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
const copiedIdx = ref<number | null>(null)
const showScrollBtn = ref(false)

const userStore = useUserStore()
const userAvatar = computed(() =>
  `https://api.dicebear.com/7.x/notionists/svg?seed=${userStore.userInfo?.username || 'admin'}&backgroundColor=6366f1`
)

// ---- Markdown 渲染（带代码块复制按钮）----
const marked = new Marked({
  renderer: {
    code({ text, lang }: { text: string; lang?: string }) {
      const language = lang && hljs.getLanguage(lang) ? lang : 'plaintext'
      const highlighted = hljs.highlight(text, { language }).value
      const escaped = text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
      return `<div class="code-block-wrapper">
        <div class="code-block-header">
          <span class="code-lang">${language}</span>
          <button class="code-copy-btn" data-code="${escaped}" onclick="window.__copyCodeBlock(this)">
            <svg xmlns="http://www.w3.org/2000/svg" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
            <span>复制</span>
          </button>
        </div>
        <pre><code class="hljs language-${language}">${highlighted}</code></pre>
      </div>`
    }
  }
})

function renderMarkdown(content: string): string {
  if (!content) return ''
  return marked.parse(content, { breaks: true, gfm: true }) as string
}

// ---- 复制整条消息 ----
function copyMessage(content: string, idx: number) {
  navigator.clipboard.writeText(content).then(() => {
    copiedIdx.value = idx
    setTimeout(() => { copiedIdx.value = null }, 2000)
  })
}

// ---- 代码块复制（全局函数，供 innerHTML onclick 调用）----
function handleCopyCodeBlock(btn: HTMLButtonElement) {
  const raw = btn.getAttribute('data-code') || ''
  const decoded = raw
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
  navigator.clipboard.writeText(decoded).then(() => {
    const span = btn.querySelector('span')
    if (span) {
      span.textContent = '已复制'
      setTimeout(() => { span.textContent = '复制' }, 2000)
    }
  })
}

onMounted(() => {
  ;(window as any).__copyCodeBlock = handleCopyCodeBlock
})
onBeforeUnmount(() => {
  delete (window as any).__copyCodeBlock
})

// ---- 自动滚动到底部 ----
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

// ---- 滚动检测（显示/隐藏回到底部按钮）----
function handleScroll() {
  if (!chatBody.value) return
  const { scrollTop, scrollHeight, clientHeight } = chatBody.value
  showScrollBtn.value = scrollHeight - scrollTop - clientHeight > 150
}

watch(() => props.messages.length, scrollToBottom)
watch(
  () => props.messages[props.messages.length - 1]?.content,
  scrollToBottom
)
watch(() => props.isTyping, scrollToBottom)

defineExpose({ scrollToBottom })
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
  width: 7px;
  height: 7px;
  background: #22c55e;
  border-radius: 50%;
  box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.2);
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
.chat-body-wrapper {
  flex: 1;
  position: relative;
  overflow: hidden;
  min-height: 0;
}

.chat-body {
  height: 100%;
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
  margin-top: 60px;
  margin-bottom: 40px;
  color: #64748b;
  opacity: 0;
  animation: fadeIn 0.8s ease forwards;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* 气泡外层容器，用于定位吉祥物 */
.welcome-bubble-wrap {
  position: relative;
  padding-top: 90px; /* 给吉祥物留出空间 */
}

/* 吉祥物：站在气泡左上角，偶尔轻轻晃动 */
.welcome-mascot {
  position: absolute;
  top: -10px;
  left: -16px;
  z-index: 2;
  filter: drop-shadow(0 4px 12px rgba(59, 130, 246, 0.15));
  animation: mascotIdle 4s ease-in-out infinite;
}

.welcome-ai-img {
  width: 140px;
  height: 140px;
  object-fit: contain;
}

/* 待机动画：原地轻微摇晃 + 微弹 */
@keyframes mascotIdle {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  30% { transform: translateY(-3px) rotate(-2deg); }
  60% { transform: translateY(0) rotate(1.5deg); }
  80% { transform: translateY(-1px) rotate(0deg); }
}

.welcome-bubble {
  background: linear-gradient(145deg, #f7faff 0%, #eff5fc 100%);
  border: 1px solid #e3ecf5;
  border-radius: 20px;
  padding: 24px 32px 20px;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.06), 0 8px 24px rgba(59, 130, 246, 0.04);
  max-width: 420px;
  min-width: 320px;
  position: relative;
}

.welcome-bubble h3 {
  color: #1e293b;
  font-size: 20px;
  margin: 0 0 6px;
  font-weight: 600;
  letter-spacing: -0.3px;
}

.welcome-name {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.welcome-desc {
  color: #94a3b8;
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
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

.msg-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
  min-width: 0;
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
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: #fff;
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
  background: linear-gradient(145deg, #f7faff 0%, #eff5fc 100%);
  border: 1px solid #e3ecf5;
  color: #1e293b;
  border-top-left-radius: 2px;
  box-shadow: 0 1px 4px rgba(59, 130, 246, 0.06), 0 4px 12px rgba(59, 130, 246, 0.03);
}

.msg-row.user .bubble {
  background: linear-gradient(145deg, #4b93f7 0%, #2563eb 100%);
  color: white;
  border-bottom-right-radius: 4px;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.2), 0 4px 16px rgba(37, 99, 235, 0.1);
}

/* ---- 消息复制按钮（新增）---- */
.msg-actions {
  display: flex;
  gap: 4px;
  padding-top: 2px;
}

.msg-action-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: 1px solid transparent;
  cursor: pointer;
  padding: 3px 8px;
  border-radius: 6px;
  font-size: 12px;
  color: #94a3b8;
  transition: all 0.2s;
}

.msg-action-btn:hover {
  background: #f1f5f9;
  color: #3b82f6;
  border-color: #e2e8f0;
}

/* ---- 代码块样式（新增）---- */
.bubble :deep(.code-block-wrapper) {
  border-radius: 8px;
  overflow: hidden;
  margin: 12px 0;
  border: 1px solid #374151;
}

.bubble :deep(.code-block-header) {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 6px 12px;
  background: #1e1e2e;
  border-bottom: 1px solid #374151;
}

.bubble :deep(.code-lang) {
  font-size: 12px;
  color: #94a3b8;
  text-transform: lowercase;
}

.bubble :deep(.code-copy-btn) {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 12px;
  color: #94a3b8;
  padding: 2px 6px;
  border-radius: 4px;
  transition: all 0.2s;
}

.bubble :deep(.code-copy-btn:hover) {
  color: #e2e8f0;
  background: rgba(255, 255, 255, 0.08);
}

.bubble :deep(pre) {
  margin: 0;
  padding: 12px 16px;
  overflow-x: auto;
  background: #0d1117;
}

.bubble :deep(code) {
  font-family: 'Consolas', 'Monaco', monospace;
  font-size: 13px;
}

/* Typing Indicator */
.typing-bubble {
  display: flex;
  gap: 5px;
  padding: 12px 18px;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #94a3b8;
  animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

@keyframes slideIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
  to { opacity: 1; }
}

/* Scroll to bottom button */
.scroll-to-bottom-btn {
  position: absolute;
  bottom: 16px;
  right: 24px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  color: #64748b;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.2s;
  z-index: 10;
}

.scroll-to-bottom-btn:hover {
  background: #f8fafc;
  color: #3b82f6;
  border-color: #bfdbfe;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
}

.scroll-btn-fade-enter-active,
.scroll-btn-fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.scroll-btn-fade-enter-from,
.scroll-btn-fade-leave-to {
  opacity: 0;
  transform: translateY(8px);
}

/* Footer */
.chat-footer {
  padding: 14px 16px;
  border: 1px solid #e5e7eb;
  border-top: none;
  background: linear-gradient(180deg, #fafcff 0%, #f0f7ff 100%);
  border-radius: 0 0 14px 14px;
  box-shadow: 0 -2px 12px rgba(59, 130, 246, 0.04);
}

.input-wrapper {
  background: #ffffff;
  border: 1.5px solid #dbeafe;
  border-radius: 16px;
  padding: 4px 6px 4px 16px;
  display: flex;
  align-items: flex-end;
  gap: 8px;
  transition: all 0.25s ease;
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.04);
}

.input-wrapper:focus-within {
  border-color: #3b82f6;
  box-shadow: 0 4px 16px rgba(59, 130, 246, 0.12);
  background: #fefeff;
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
  width: 38px;
  height: 38px !important;
  margin-bottom: 3px;
  font-size: 17px;
  background: linear-gradient(135deg, #3b82f6, #2563eb) !important;
  border-color: transparent !important;
  transition: all 0.2s;
}

.send-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #60a5fa, #3b82f6) !important;
  transform: scale(1.05);
}

.send-btn:disabled {
  background: #cbd5e1 !important;
  border-color: transparent !important;
  opacity: 0.6;
}

.footer-note {
  text-align: center;
  font-size: 11px;
  color: #94a3b8;
  margin-top: 8px;
  letter-spacing: 0.3px;
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
