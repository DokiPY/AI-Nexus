import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import VueDevTools from 'vite-plugin-vue-devtools'
import path from 'path'
import dotenv from 'dotenv'

// 获取环境变量 VITE_ENV
const mode = process.env.VITE_ENV || 'local'

// 动态加载对应的 .env 文件
dotenv.config({ path: `.env.${mode}` })

console.log(`🔥 当前环境: ${mode}, 加载配置: .env.${mode}`)

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    VueDevTools()
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src')
    }
  },
  server: {
    host: '0.0.0.0',
    port: 5173
  },
  build: {
    outDir: `dist-${mode}`,
    chunkSizeWarningLimit: 1000,  // 提高警告阈值到 1000KB
    rollupOptions: {
      output: {
        manualChunks: {
          'element-plus': ['element-plus'],  // Element Plus 单独打包
          'echarts': ['echarts'],            // ECharts 单独打包
          'vendor': ['vue', 'vue-router', 'pinia']  // Vue 全家桶单独打包
        }
      }
    }
  }
})
