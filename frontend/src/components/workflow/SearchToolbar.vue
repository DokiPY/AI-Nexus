<!-- 搜索工具栏组件，包含搜索框和分类筛选标签 -->
<template>
  <div class="toolbar fade-in-up delay-2">
    <div class="search-box">
      <i class="search-icon">🔍</i>
      <input 
        type="text" 
        :value="searchQuery"
        @input="$emit('update:searchQuery', ($event.target as HTMLInputElement).value)"
        placeholder="搜索工作流名称或描述..."
      >
    </div>
    
    <div class="filter-tabs">
      <button 
        v-for="tab in categories" 
        :key="tab"
        :class="{ active: currentCategory === tab }"
        @click="$emit('update:currentCategory', tab)"
      >
        {{ tab }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  searchQuery: string
  currentCategory: string
  categories: string[]
}

defineProps<Props>()

defineEmits<{
  'update:searchQuery': [value: string]
  'update:currentCategory': [value: string]
}>()
</script>

<style scoped>
.toolbar {
  margin-top: 40px; display: flex; flex-direction: column; align-items: center; gap: 20px;
}
.search-box {
  position: relative; width: 100%; max-width: 500px;
}
.search-box input {
  width: 100%; padding: 14px 20px 14px 45px;
  background: rgba(255,255,255,0.9); border: 1px solid rgba(59, 130, 246, 0.1);
  border-radius: 12px; color: #1e293b; font-size: 1rem; transition: all 0.3s;
}
.search-box input:focus { outline: none; background: rgba(255,255,255,0.95); border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1); }
.search-box input::placeholder { color: #64748b; }
.search-icon { position: absolute; left: 15px; top: 50%; transform: translateY(-50%); opacity: 0.6; color: #3b82f6; }

.filter-tabs {
  display: flex; gap: 8px; flex-wrap: wrap; justify-content: center;
}
.filter-tabs button {
  padding: 8px 16px; background: rgba(248, 250, 252, 0.8); border: 1px solid rgba(0, 0, 0, 0.06); color: #64748b; cursor: pointer; border-radius: 20px; font-size: 0.9rem; transition: all 0.2s;
}
.filter-tabs button:hover { color: #334155; background: rgba(241, 245, 249, 0.9); border-color: rgba(59, 130, 246, 0.2); }
.filter-tabs button.active { background: linear-gradient(135deg, #3b82f6, #10b981); color: #fff; border-color: transparent; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.25); }

.fade-in-up { opacity: 0; animation: fadeInUp 0.6s ease-out forwards; transform: translateY(20px); }
.delay-2 { animation-delay: 0.2s; }

@keyframes fadeInUp { to { opacity: 1; transform: translateY(0); } }

@media (max-width: 768px) {
  .toolbar { width: 100%; }
}
</style>