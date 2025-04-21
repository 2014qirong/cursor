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
    },
    {
      path: 'topic',
      component: () => import('@/views/content/topic/index.vue'),
      name: 'Topic',
      meta: { title: '专题页管理' }
    },
    {
      path: 'article',
      component: () => import('@/views/content/article/index.vue'),
      name: 'Article',
      meta: { title: '文章管理' }
    },
    {
      path: 'article/edit/:id',
      component: () => import('@/views/content/article/edit.vue'),
      name: 'ArticleEdit',
      meta: { title: '编辑文章', activeMenu: '/content/article' },
      hidden: true
    },
    {
      path: 'article/add',
      component: () => import('@/views/content/article/add.vue'),
      name: 'ArticleAdd',
      meta: { title: '添加文章', activeMenu: '/content/article' },
      hidden: true
    }
  ]
}

export default contentRoutes 