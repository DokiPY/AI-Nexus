<template>
  <div class="card-footer">
    <span class="footer-text">
      尚未订阅 AI Agent Workflow？
    </span>
    <span class="link" @click="$emit('contact-admin')">了解方案 / 联系我们</span>
  </div>
</template>

<script setup lang="ts">
defineEmits<{
  'contact-admin': []
}>()
</script>

<style scoped>
.card-footer {
  margin-top: 24px;
  padding-top: 20px;
  border-top: 1px dashed #e5e7eb;
  text-align: center;
  font-size: 13px;
}

.footer-text {
  color: #6b7280;
}

.link {
  margin-left: 4px;
  color: #1f3a5f;
  font-weight: 600;
  cursor: pointer;
}
</style>
