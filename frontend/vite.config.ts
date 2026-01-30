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
  preview: {
    host: '0.0.0.0',
    port: 5173,
    allowedHosts: [
      'nexus.berivena.com',
      'localhost',
      '127.0.0.1'
    ]
  },
  build: {
    outDir: `dist-${mode}`,
    chunkSizeWarningLimit: 1000,  // 提高警告阈值到 1000KB
    rollupOptions: {
      output: {
        manualChunks(id) {
          // 将 node_modules 中的包按照包名分组
          if (id.includes('node_modules')) {
            if (id.includes('element-plus')) {
              return 'element-plus'
            }
            if (id.includes('echarts')) {
              return 'echarts'
            }
            if (id.includes('vue') || id.includes('pinia') || id.includes('@vue')) {
              return 'vendor'
            }
          }
        }
      }
    }
  }
})

