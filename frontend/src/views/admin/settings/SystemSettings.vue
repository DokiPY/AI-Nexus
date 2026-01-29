<!--
 * @component SystemSettings
 * @description 系统设置页面
-->
<template>
  <div class="system-settings">
    <ContentContainer>
      <div class="section-header">
      <div class="header-left">
        <h1>系统设置</h1>
        <p>配置系统参数和选项</p>
      </div>
    </div>
    
    <div class="empty-state">
      <div class="empty-icon">
        <div class="icon-circle">⚙️</div>
      </div>
      <h3>功能开发中</h3>
      <p>系统设置功能正在开发中...</p>
    </div>
    </ContentContainer>
  </div>
</template>

<script setup lang="ts">
import { ContentContainer } from '@/components'
</script>

<style scoped>
.system-settings {
  height: calc(100vh - 70px - 48px);
  display: flex;
  flex-direction: column;
  color: #1e293b;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 32px;
}

.section-header h1 {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 8px 0;
  color: #1e293b;
  letter-spacing: -0.5px;
}

.section-header p {
  color: #64748b;
  font-size: 1rem;
  margin: 0;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: #64748b;
}

.empty-icon {
  position: relative;
  display: inline-block;
  margin-bottom: 24px;
}

.icon-circle {
  width: 80px;
  height: 80px;
  background: rgba(248, 250, 252, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  margin: 0 auto;
}

.empty-state h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #334155;
  margin: 0 0 8px 0;
}

.empty-state p {
  color: #64748b;
  margin: 0;
}
</style>