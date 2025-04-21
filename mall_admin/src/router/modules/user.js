import Layout from '@/layout/index.vue'

const userRoutes = {
  path: '/user',
  component: Layout,
  redirect: '/user/list',
  name: 'User',
  meta: { title: '用户管理', icon: 'User' },
  children: [
    {
      path: 'list',
      component: () => import('@/views/user/list/index.vue'),
      name: 'UserList',
      meta: { title: '用户列表' }
    },
    {
      path: 'detail/:id',
      component: () => import('@/views/user/detail/index.vue'),
      name: 'UserDetail',
      meta: { title: '用户详情', activeMenu: '/user/list' },
      hidden: true
    },
    {
      path: 'level',
      component: () => import('@/views/user/level/index.vue'),
      name: 'UserLevel',
      meta: { title: '等级管理' }
    },
    {
      path: 'stats',
      component: () => import('@/views/user/stats/index.vue'),
      name: 'UserStats',
      meta: { title: '用户统计' }
    },
    {
      path: 'feedback',
      component: () => import('@/views/user/feedback/index.vue'),
      name: 'UserFeedback',
      meta: { title: '用户反馈' }
    }
  ]
}

export default userRoutes 