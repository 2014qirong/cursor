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
    }
  ]
}

export default statisticsRoutes 