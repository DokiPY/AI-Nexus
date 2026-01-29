import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { setupRouterGuards } from './guards'

// 路由配置
const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/login/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/workflows',
    name: 'WorkflowList',
    component: () => import('../views/user/workflow/WorkflowList.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/admin',
    component: () => import('../views/admin/AdminDashboard.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: '',
        redirect: '/admin/users'
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: () => import('../views/admin/users/UserManagement.vue')
      },
      {
        path: 'companies',
        name: 'AdminCompanies',
        component: () => import('../views/admin/companies/CompanyManagement.vue')
      },
      {
        path: 'workflows',
        name: 'WorkflowManagement',
        component: () => import('../views/admin/workflows/WorkflowManagement.vue')
      },
      {
        path: 'statistics',
        name: 'StatisticsManagement',
        component: () => import('../views/admin/statistics/StatisticsManagement.vue')
      },
      // {
      //   path: 'settings',
      //   name: 'SystemSettings',
      //   component: () => import('../views/admin/settings/SystemSettings.vue')
      // }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    redirect: '/login'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 设置路由守卫
setupRouterGuards(router)

export default router