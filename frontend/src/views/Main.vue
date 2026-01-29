<template>
  <router-view />
</template>

<script setup lang="ts">
// 这里只注册页面模块，不处理路由逻辑
import './login/Login.vue'
import './user/workflow/WorkflowList.vue'
</script>