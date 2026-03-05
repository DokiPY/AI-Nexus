<!--
 * @component AdminSidebar
 * @description 管理员左侧导航栏 - 极致优化版
 * - 性能优化：使用 will-change 提升折叠性能
 * - 视觉优化：SVG 图标、丝滑过渡、Ceramic Clean 风格
-->
<template>
  <aside class="sidebar" :class="{ collapsed: collapsed }">
    <!-- 悬浮折叠按钮 -->
    <button class="toggle-btn" @click="$emit('toggle')" title="切换菜单">
      <span class="arrow-icon" :class="{ rotated: collapsed }">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
      </span>
    </button>

    <div class="sidebar-header">
      <div class="logo-area">
        <span class="menu-label" :class="{ hidden: collapsed }">MENU</span>
        <span class="menu-dots" :class="{ visible: collapsed }">●</span>
      </div>
    </div>
    
    <nav class="sidebar-nav">
      <div 
        v-for="item in menuItems" 
        :key="item.key"
        class="nav-item" 
        :class="{ 
          active: activeMenu === item.key,
          disabled: item.disabled 
        }"
        @click="!item.disabled && $emit('menu-change', item.key)"
        :title="collapsed ? item.label : ''"
      >
        <div class="nav-content">
          <div class="nav-icon-wrapper">
            <!-- SVG 图标映射 -->
            <svg v-if="item.key === 'users'" class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
              <circle cx="9" cy="7" r="4"></circle>
              <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
              <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>
            <svg v-else-if="item.key === 'companies'" class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
              <polyline points="9 22 9 12 15 12 15 22"></polyline>
            </svg>
            <svg v-else-if="item.key === 'workflows'" class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
            </svg>
            <svg v-else-if="item.key === 'statistics'" class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="20" x2="18" y2="10"></line>
              <line x1="12" y1="20" x2="12" y2="4"></line>
              <line x1="6" y1="20" x2="6" y2="14"></line>
            </svg>
            <svg v-else-if="item.key === 'settings'" class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <circle cx="12" cy="12" r="3"></circle>
              <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
            </svg>
            <!-- 默认图标 -->
            <span v-else class="text-icon">{{ item.label ? item.label[0] : '?' }}</span>
          </div>
          
          <span class="nav-text">{{ item.label }}</span>

          <!-- 橙色徽标 -->
          <span v-if="item.badge" class="status-badge">{{ item.badge }}</span>
        </div>
        
        <!-- 选中光效 -->
        <div class="active-indicator"></div>
      </div>
    </nav>

    <!-- 底部时间天气 -->
    <div class="sidebar-footer">
      <WeatherWidget :mini="collapsed" />
    </div>
  </aside>
</template>

<script setup lang="ts">
import WeatherWidget from './WeatherWidget.vue'

interface MenuItem {
  key: string
  label: string
  badge?: string
  disabled?: boolean
}

defineProps<{
  collapsed: boolean
  activeMenu: string
  menuItems: MenuItem[]
}>()

defineEmits<{
  toggle: []
  'menu-change': [key: string]
}>()
</script>

<style scoped>
/* Ceramic Clean 主题变量 */
.sidebar {
  --accent-blue: #3b82f6;
  --accent-blue-soft: rgba(59, 130, 246, 0.1);
  --bg-white: rgba(255, 255, 255, 0.95);
  --text-primary: #334155;
  --text-secondary: #64748b;
  --sidebar-width: 260px;
  --sidebar-collapsed-width: 72px;
  
  width: var(--sidebar-width);
  background: var(--bg-white);
  border-right: 1px solid rgba(226, 232, 240, 0.8);
  /* 优化：减少 backdrop-filter 的开销，或者完全移除如果仍然卡顿 */
  backdrop-filter: blur(10px); 
  display: flex;
  flex-direction: column;
  padding: 24px 16px;
  position: relative;
  z-index: 10;
  box-shadow: 4px 0 24px rgba(0, 0, 0, 0.02);
  white-space: nowrap;
  
  /* 性能优化关键：告诉浏览器这个属性会变化 */
  will-change: width;
  /* 使用 transform 可能会更流畅，但会影响布局流，这里保持 width transition 但优化曲线 */
  transition: width 0.3s cubic-bezier(0.2, 0, 0, 1);
}

.sidebar.collapsed {
  width: var(--sidebar-collapsed-width);
  padding: 24px 12px;
}

/* ================== 悬浮折叠按钮 ================== */
.toggle-btn {
  position: absolute;
  top: 32px;
  right: -12px;
  width: 24px;
  height: 24px;
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 50%;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  z-index: 20;
  transition: all 0.2s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
  outline: none;
}

.toggle-btn:hover {
  border-color: var(--accent-blue);
  color: var(--accent-blue);
  transform: scale(1.1);
}

.arrow-icon {
  display: flex;
  align-items: center;
  transition: transform 0.3s ease;
}

.arrow-icon.rotated {
  transform: rotate(180deg);
}

/* ================== 头部 ================== */
.sidebar-header {
  height: 40px;
  margin-bottom: 24px;
  padding-left: 8px;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.logo-area {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
}

.menu-label {
  font-size: 0.75rem;
  font-weight: 800;
  color: #94a3b8;
  letter-spacing: 2px;
  transition: opacity 0.2s;
  position: absolute;
  left: 0;
}

.menu-label.hidden {
  opacity: 0;
  pointer-events: none;
}

.menu-dots {
  position: absolute;
  left: 0;
  width: 100%;
  text-align: center;
  color: var(--accent-blue);
  font-size: 0.6rem;
  letter-spacing: 2px;
  opacity: 0;
  transform: scale(0.5);
  transition: opacity 0.2s 0.1s, transform 0.2s 0.1s;
}

.menu-dots.visible {
  opacity: 1;
  transform: scale(1);
}

/* ================== 导航项 ================== */
.sidebar-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
  overflow-x: hidden;
  overflow-y: auto;
  scrollbar-width: none;
}
.sidebar-nav::-webkit-scrollbar { display: none; }

.nav-item {
  position: relative;
  height: 48px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--text-secondary);
  display: flex;
  align-items: center;
}

.nav-item:hover:not(.disabled) {
  background: #f8fafc;
  color: var(--text-primary);
}

.nav-item.active {
  background: var(--accent-blue-soft);
  color: var(--accent-blue);
}

/* 内部内容容器 */
.nav-content {
  display: flex;
  align-items: center;
  width: 100%;
  padding: 0 12px;
  height: 100%;
}

.sidebar.collapsed .nav-content {
  justify-content: center;
  padding: 0;
}

.nav-icon-wrapper {
  width: 24px;
  height: 24px;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-shrink: 0;
  transition: transform 0.2s;
}

.nav-icon {
  width: 20px;
  height: 20px;
  stroke-linecap: round;
  stroke-linejoin: round;
  transition: all 0.2s;
}

.text-icon {
  font-size: 1rem;
  font-weight: 600;
  color: var(--accent-blue);
}

.nav-item:hover .nav-icon-wrapper {
  transform: scale(1.1);
}

.nav-item.active .nav-icon {
  stroke-width: 2.5;
}

.nav-text {
  margin-left: 12px;
  font-weight: 500;
  font-size: 0.95rem;
  transition: opacity 0.2s ease, transform 0.2s ease;
  opacity: 1;
  transform: translateX(0);
  white-space: nowrap;
}

/* 关键优化：折叠时将文本移出文档流 */
.sidebar.collapsed .nav-text,
.sidebar.collapsed .status-badge {
  opacity: 0;
  transform: translateX(10px);
  position: absolute;
  pointer-events: none;
}

.status-badge {
  margin-left: auto;
  font-size: 0.7rem;
  font-weight: 600;
  background: #f59e0b;
  color: #fff;
  padding: 2px 6px;
  border-radius: 6px;
  transition: opacity 0.2s;
}

/* 选中指示器 */
.active-indicator {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  height: 20px;
  width: 3px;
  background: var(--accent-blue);
  border-radius: 0 2px 2px 0;
  opacity: 0;
  transition: opacity 0.2s, height 0.2s;
}

.nav-item.active .active-indicator {
  opacity: 1;
  height: 24px;
}

.nav-item.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  filter: grayscale(1);
}

/* ================== 底部时间天气 ================== */
.sidebar-footer {
  margin-top: auto;
  padding-top: 20px;
  border-top: 1px solid rgba(226, 232, 240, 0.6);
}

/* 移动端适配 */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    height: 100vh;
    left: 0;
    top: 0;
    transform: translateX(-100%);
    transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  /* 移动端逻辑：collapsed 类名实际上表示是否显示 */
  .sidebar.collapsed {
    transform: translateX(0);
    width: 260px; /* 移动端始终全宽 */
  }
  
  .sidebar.collapsed .nav-text,
  .sidebar.collapsed .status-badge {
    opacity: 1;
    transform: none;
    position: static;
  }
}
</style>
