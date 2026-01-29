<!-- Hero区域组件，包含标题、统计信息和搜索工具栏 -->
<template>
  <section class="hero-section">
    <h1 class="fade-in-up">选择您的 AI 助手</h1>
    <p class="fade-in-up delay-1">
      已为您加载 <span class="highlight">{{ workflowCount }}</span> 个授权工作流
    </p>
    
    <SearchToolbar
      :search-query="searchQuery"
      :current-category="currentCategory"
      :categories="categories"
      @update:search-query="$emit('update:searchQuery', $event)"
      @update:current-category="$emit('update:currentCategory', $event)"
    />
  </section>
</template>

<script setup lang="ts">
import SearchToolbar from './SearchToolbar.vue'

interface Props {
  workflowCount: number
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
.hero-section { 
  text-align: center; 
  margin-bottom: 60px; 
}
.hero-section h1 { 
  font-size: 2.5rem; 
  font-weight: 700; 
  margin-bottom: 10px; 
  background: linear-gradient(135deg, #0f172a, #3b82f6, #10b981);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.hero-section p { 
  color: #64748b; 
  font-size: 1.1rem; 
}
.highlight { 
  color: #3b82f6; 
  font-weight: 600; 
}

.fade-in-up { 
  opacity: 0; 
  animation: fadeInUp 0.6s ease-out forwards; 
  transform: translateY(20px); 
}
.delay-1 { 
  animation-delay: 0.1s; 
}

@keyframes fadeInUp { 
  to { 
    opacity: 1; 
    transform: translateY(0); 
  } 
}

@media (max-width: 768px) {
  .hero-section h1 { 
    font-size: 2rem; 
  }
}
</style>