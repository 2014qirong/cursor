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
    },
    {
      path: 'refund',
      component: () => import('@/views/order/refund/index.vue'),
      name: 'OrderRefund',
      meta: { title: '退款/售后' }
    },
    {
      path: 'refund-detail/:id',
      component: () => import('@/views/order/refund-detail/index.vue'),
      name: 'RefundDetail',
      meta: { title: '退款详情', activeMenu: '/order/refund' },
      hidden: true
    },
    {
      path: 'stats',
      component: () => import('@/views/order/stats/index.vue'),
      name: 'OrderStats',
      meta: { title: '订单统计' }
    },
    {
      path: 'delivery',
      component: () => import('@/views/order/delivery/index.vue'),
      name: 'OrderDelivery',
      meta: { title: '发货管理' }
    }
  ]
}

export default orderRoutes 