import Layout from '@/layout/index.vue'

const contentRoutes = {
  path: '/content',
  component: Layout,
  redirect: '/content/banner',
  name: 'Content',
  meta: { title: '内容管理', icon: 'Picture' },
  children: [
    {
      path: 'banner',
      component: () => import('@/views/content/banner/index.vue'),
      name: 'Banner',
      meta: { title: '轮播图管理' }
    },
    {
      path: 'recommend',
      component: () => import('@/views/content/recommend/index.vue'),
      name: 'Recommend',
      meta: { title: '推荐位管理' }
    },
    {
      path: 'notice',
      component: () => import('@/views/content/notice/index.vue'),
      name: 'Notice',
      meta: { title: '公告管理' }
    }
  ]
}

export default contentRoutes 