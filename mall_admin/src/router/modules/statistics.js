import Layout from '@/layout/index.vue'

const statisticsRoutes = {
  path: '/statistics',
  component: Layout,
  redirect: '/statistics/sales',
  name: 'Statistics',
  meta: { title: '数据统计', icon: 'DataLine' },
  children: [
    {
      path: 'sales',
      component: () => import('@/views/statistics/sales/index.vue'),
      name: 'SalesStatistics',
      meta: { title: '销售统计' }
    },
    {
      path: 'users',
      component: () => import('@/views/statistics/users/index.vue'),
      name: 'UserStatistics',
      meta: { title: '用户统计' }
    },
    {
      path: 'products',
      component: () => import('@/views/statistics/products/index.vue'),
      name: 'ProductStatistics',
      meta: { title: '商品统计' }
    },
    {
      path: 'dashboard',
      component: () => import('@/views/statistics/dashboard/index.vue'),
      name: 'StatisticsDashboard',
      meta: { title: '统计看板' }
    },
    {
      path: 'export',
      component: () => import('@/views/statistics/export/index.vue'),
      name: 'DataExport',
      meta: { title: '数据导出' }
    }
  ]
}

export default statisticsRoutes 