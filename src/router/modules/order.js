import Layout from '@/layout/index.vue'

const orderRoutes = {
  path: '/order',
  component: Layout,
  redirect: '/order/list',
  name: 'Order',
  meta: { title: '订单管理', icon: 'Document' },
  children: [
    {
      path: 'list',
      component: () => import('@/views/order/list/index.vue'),
      name: 'OrderList',
      meta: { title: '订单列表' }
    },
    {
      path: 'detail/:id',
      component: () => import('@/views/order/detail/index.vue'),
      name: 'OrderDetail',
      meta: { title: '订单详情', activeMenu: '/order/list' },
      hidden: true
    }
  ]
}

export default orderRoutes 