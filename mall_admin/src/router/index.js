import { createRouter, createWebHistory } from 'vue-router'

/* 布局组件 */
import Layout from '@/layout/index.vue'

/* 路由模块 */
// 导入各个模块的路由
import productRoutes from './modules/product'
import orderRoutes from './modules/order'
import userRoutes from './modules/user'
import marketingRoutes from './modules/marketing'
import contentRoutes from './modules/content'
import systemRoutes from './modules/system'
import statisticsRoutes from './modules/statistics'

/**
 * 基础路由
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index.vue'),
    hidden: true,
    meta: { title: '登录' }
  },
  {
    path: '/404',
    component: () => import('@/views/error/404.vue'),
    hidden: true,
    meta: { title: '404' }
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        name: 'Dashboard',
        meta: { title: '首页', icon: 'HomeFilled' }
      }
    ]
  },
  // 直接添加各个模块路由
  productRoutes,
  orderRoutes,
  userRoutes,
  marketingRoutes,
  contentRoutes,
  systemRoutes,
  statisticsRoutes,
  // 404 页面必须放在最后
  { path: '/:pathMatch(.*)*', redirect: '/404', hidden: true }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  scrollBehavior: () => ({ top: 0 }),
  routes: constantRoutes
})

export function resetRouter() {
  const newRouter = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    scrollBehavior: () => ({ top: 0 }),
    routes: constantRoutes
  })
  // Vue Router v4不再使用matcher，这里需要重新创建路由器
  // router.matcher = newRouter.matcher
}

export default router 