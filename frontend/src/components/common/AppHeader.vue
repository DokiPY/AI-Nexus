<!-- 顶部导航组件 - 适配暮光蓝灰主题 -->
<template>
  <header class="top-nav">
    <!-- 左侧品牌区 -->
    <div class="nav-brand">
      <div class="logo-wrapper">
        <div class="logo-icon"></div>
        <div class="logo-glow"></div>
      </div>
      <span class="brand-name">Nexus Console</span>
    </div>
    
    <!-- 右侧用户区 -->
    <div class="nav-user">
      <div class="tenant-badge" v-if="tenantName">
        <svg class="tenant-icon" viewBox="0 0 18 18" fill="none" xmlns="http://www.w3.org/2000/svg">
          <rect x="2" y="2" width="14" height="15" rx="1.2" stroke="currentColor" stroke-width="1.4"/>
          <path d="M6 6h2M10 6h2M6 9h2M10 9h2M6 12h2M10 12h2" stroke="currentColor" stroke-width="1.3" stroke-linecap="round"/>
          <path d="M7 17v-4h4v4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        <span class="text">{{ tenantName }}</span>
      </div>
      
      <div class="user-profile" 
           :class="{ 'active': showUserMenu }"
           @click="toggleUserMenu"
           v-click-outside="closeUserMenu"
      >
        <img :src="userAvatar" :alt="userName" />
        <span class="user-name">{{ userName }}</span>
        <span class="dropdown-arrow">▼</span>
        
        <!-- 下拉菜单 -->
        <transition name="scale-fade">
          <div v-if="showUserMenu" class="user-dropdown">
            <div class="dropdown-header">
              <div class="user-info">
                <strong>{{ userName }}</strong>
                <span>{{ userEmail }}</span>
              </div>
            </div>
            
            <div class="dropdown-divider"></div>
            
            <!-- <button class="menu-item">
              <span class="icon">👤</span> 个人中心
            </button>
            <button class="menu-item">
              <span class="icon">⚙️</span> 账户设置
            </button> -->
            
            <!-- <div class="dropdown-divider"></div> -->

            <button @click="handleLogout" class="menu-item danger">
              <span class="icon">🚪</span> 退出登录
            </button>
          </div>
        </transition>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '../../stores/login/user'

const userStore = useUserStore()

const userName = computed(() => userStore.userInfo?.username || 'Admin')
const userEmail = computed(() => userStore.userInfo?.email || 'admin@nexus.com')
// 使用更现代的 Avatar 风格
const userAvatar = computed(() => 
  `https://api.dicebear.com/7.x/notionists/svg?seed=${userStore.userInfo?.username || 'admin'}&backgroundColor=6366f1`
)
const tenantName = computed(() => userStore.userInfo?.company?.name || '')

const emit = defineEmits<{
  logout: []
}>()

const showUserMenu = ref(false)

const toggleUserMenu = (e: Event) => {
  e.stopPropagation()
  showUserMenu.value = !showUserMenu.value
}

const closeUserMenu = () => {
  showUserMenu.value = false
}

// 点击外部关闭 (简单的实现，或者你可以使用 vueuse 的 onClickOutside)
const handleClickOutside = (e: MouseEvent) => {
  const target = e.target as HTMLElement
  if (!target.closest('.user-profile')) {
    showUserMenu.value = false
  }
}

onMounted(() => document.addEventListener('click', handleClickOutside))
onUnmounted(() => document.removeEventListener('click', handleClickOutside))

const handleLogout = async () => {
  await userStore.logout()
  emit('logout')
}
</script>

<style scoped>
.top-nav {
  position: sticky; top: 0; z-index: 50;
  height: 70px;
  display: flex; justify-content: space-between; align-items: center;
  padding: 0 40px;
  /* Ceramic Clean 主题：半透明的纯白背景 */
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px) saturate(180%);
  border-bottom: 1px solid rgba(0, 0, 0, 0.06);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
  transition: all 0.3s ease;
  box-sizing: border-box;
}

/* 品牌 Logo 区域 */
.nav-brand { display: flex; align-items: center; gap: 14px; }

.logo-wrapper { position: relative; width: 28px; height: 28px; }
.logo-icon { 
  width: 100%; height: 100%; 
  background: linear-gradient(135deg, #4f46e5, #06b6d4); 
  border-radius: 8px; 
  position: relative; z-index: 2;
}
/* 给 Logo 加一点光晕 */
.logo-glow {
  position: absolute; inset: -4px;
  background: inherit;
  filter: blur(8px);
  opacity: 0.4;
  z-index: 1;
  background: linear-gradient(135deg, #4f46e5, #06b6d4);
}

.brand-name { 
  font-weight: 700; 
  font-size: 1.15rem; 
  letter-spacing: -0.5px; 
  color: #1e293b;
  text-shadow: none;
}

/* 右侧用户区 */
.nav-user { display: flex; align-items: center; gap: 20px; }

.tenant-badge { 
  display: flex; align-items: center; gap: 8px; 
  padding: 6px 14px; 
  background: rgba(248, 250, 252, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.06);
  border-radius: 20px; 
  font-size: 0.85rem; 
  color: #64748b;
  transition: all 0.2s;
}
.tenant-badge:hover {
  background: rgba(241, 245, 249, 0.9);
  border-color: rgba(99, 102, 241, 0.2);
  color: #475569;
}
.tenant-badge .tenant-icon {
  width: 17px;
  height: 17px;
  flex-shrink: 0;
  color: #94a3b8;
}

/* 用户头像与下拉 */
.user-profile { 
  display: flex; align-items: center; gap: 10px; 
  cursor: pointer; position: relative;
  padding: 6px 8px; 
  border-radius: 10px; 
  transition: all 0.2s;
  border: 1px solid transparent;
}

.user-profile:hover, .user-profile.active { 
  background: rgba(0, 0, 0, 0.03); 
}
.user-profile.active {
  background: rgba(248, 250, 252, 0.8);
  border-color: rgba(0, 0, 0, 0.06);
}

.user-profile img { 
  width: 36px; height: 36px; 
  border-radius: 50%; 
  border: 2px solid rgba(0, 0, 0, 0.06);
  background: #f8fafc;
}

.user-name { font-size: 0.95rem; font-weight: 500; color: #334155; }
.dropdown-arrow { font-size: 0.7rem; color: #64748b; transition: transform 0.2s; }
.user-profile.active .dropdown-arrow { transform: rotate(180deg); }

/* 下拉菜单容器 */
.user-dropdown {
  position: absolute; top: calc(100% + 12px); right: 0;
  width: 240px;
  background: #ffffff;
  border: 1px solid rgba(0, 0, 0, 0.08); 
  border-radius: 14px;
  padding: 8px;
  box-shadow: 
    0 4px 6px -1px rgba(0, 0, 0, 0.05), 
    0 20px 25px -5px rgba(0, 0, 0, 0.1);
  transform-origin: top right;
}

.dropdown-header { padding: 8px 12px; }
.user-info strong { display: block; color: #1e293b; font-size: 0.95rem; margin-bottom: 2px; }
.user-info span { color: #64748b; font-size: 0.8rem; }

.dropdown-divider {
  height: 1px;
  background: rgba(0, 0, 0, 0.06);
  margin: 6px 0;
}

/* 菜单项 */
.menu-item {
  width: 100%;
  display: flex; align-items: center; gap: 10px;
  padding: 10px 12px;
  background: none; border: none;
  color: #475569;
  font-size: 0.9rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.menu-item:hover {
  background: rgba(0, 0, 0, 0.03);
  color: #1e293b;
}

.menu-item .icon { font-size: 1.1rem; width: 20px; text-align: center; }

.menu-item.danger { color: #dc2626; }
.menu-item.danger:hover { 
  background: rgba(239, 68, 68, 0.05); 
  color: #b91c1c; 
}

/* 动画效果 */
.scale-fade-enter-active, .scale-fade-leave-active {
  transition: all 0.2s ease;
}
.scale-fade-enter-from, .scale-fade-leave-to {
  opacity: 0;
  transform: translateY(-8px) scale(0.95);
}

@media (max-width: 768px) {
  .top-nav { padding: 0 20px; }
  .user-name { display: none; } /* 移动端隐藏用户名 */
  .tenant-badge { display: none; }
}
</style>