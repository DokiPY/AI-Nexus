<!--
 * @component AdminDashboard
 * @description 管理员后台主页面 - 优化的左侧栏与内容布局
-->
<template>
  <div class="admin-container">
    <!-- 背景与顶部导航保持不变 -->
    <AppBackground />
    <AppHeader @logout="logout" />
    
    <div class="admin-layout">
      <!-- 左侧导航栏 -->
      <AdminSidebar 
        :collapsed="sidebarCollapsed"
        :active-menu="activeMenu"
        :menu-items="menuItems"
        @toggle="sidebarCollapsed = !sidebarCollapsed"
        @menu-change="handleMenuChange"
      />
      
      <!-- 右侧主内容区 -->
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component" />
          </keep-alive>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { AppBackground, AppHeader, AdminSidebar } from '@/components'
import { useAdminLayout } from '@/composables'

const {
  activeMenu,
  sidebarCollapsed,
  menuItems,
  handleMenuChange,
  logout
} = useAdminLayout()
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.admin-container {
  min-height: 100vh;
  background-color: #fefefe; 
  font-family: 'Inter', sans-serif;
  color: #1e293b;
  position: relative;
  overflow: hidden;
}

.admin-layout {
  display: flex;
  height: calc(100vh - 70px);
  position: relative;
  z-index: 1;
}

.main-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  box-sizing: border-box;
  min-height: calc(100vh - 70px - 48px);
  scrollbar-width: thin;
  scrollbar-color: rgba(0,0,0,0.1) transparent;
}

@media (max-width: 768px) {
  .admin-layout { 
    flex-direction: column; 
    height: auto; 
  }
  .main-content { 
    padding: 20px; 
  }
}
</style>