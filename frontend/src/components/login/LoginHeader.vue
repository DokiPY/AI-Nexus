<template>
  <div class="card-header">
    <div class="logo-box">
      <Workflow :size="28" color="#ffffff" stroke-width="1.8" />
    </div>
    <h1 class="title">Agent Flow</h1>
    <p class="subtitle">
      企业级 AI Agent Workflow 订阅与执行平台
    </p>
  </div>
</template>

<script setup lang="ts">
import { Workflow } from 'lucide-vue-next'
</script>

<style scoped>
.card-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-box {
  width: 56px;
  height: 56px;
  margin: 0 auto 16px;
  border-radius: 14px;
  background: #1f3a5f;
  display: flex;
  align-items: center;
  justify-content: center;
}

.title {
  font-size: 24px;
  font-weight: 700;
  color: #1f2937;
}

.subtitle {
  margin-top: 8px;
  font-size: 14px;
  color: #0f766e;
}
</style>
