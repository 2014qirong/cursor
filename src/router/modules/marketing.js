import Layout from '@/layout/index.vue'

const marketingRoutes = {
  path: '/marketing',
  component: Layout,
  redirect: '/marketing/coupon',
  name: 'Marketing',
  meta: { title: '营销管理', icon: 'Present' },
  children: [
    {
      path: 'coupon',
      component: () => import('@/views/marketing/coupon/index.vue'),
      name: 'Coupon',
      meta: { title: '优惠券管理' }
    },
    {
      path: 'promotion',
      component: () => import('@/views/marketing/promotion/index.vue'),
      name: 'Promotion',
      meta: { title: '促销活动' }
    },
    {
      path: 'points-mall',
      component: () => import('@/views/marketing/points-mall/index.vue'),
      name: 'PointsMall',
      meta: { title: '积分商城' }
    },
    {
      path: 'group-buy',
      component: () => import('@/views/marketing/group-buy/index.vue'),
      name: 'GroupBuy',
      meta: { title: '拼团活动' }
    }
  ]
}

export default marketingRoutes 