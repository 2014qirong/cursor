import Layout from '@/layout/index.vue'

const productRoutes = {
  path: '/product',
  component: Layout,
  redirect: '/product/list',
  name: 'Product',
  meta: { title: '商品管理', icon: 'Goods' },
  children: [
    {
      path: 'category',
      component: () => import('@/views/product/category/index.vue'),
      name: 'ProductCategory',
      meta: { title: '商品分类' }
    },
    {
      path: 'list',
      component: () => import('@/views/product/list/index.vue'),
      name: 'ProductList',
      meta: { title: '商品列表' }
    },
    {
      path: 'add',
      component: () => import('@/views/product/add/index.vue'),
      name: 'ProductAdd',
      meta: { title: '添加商品', activeMenu: '/product/list' },
      hidden: true
    },
    {
      path: 'edit/:id',
      component: () => import('@/views/product/edit/index.vue'),
      name: 'ProductEdit',
      meta: { title: '编辑商品', activeMenu: '/product/list' },
      hidden: true
    },
    {
      path: 'spec',
      component: () => import('@/views/product/spec/index.vue'),
      name: 'ProductSpec',
      meta: { title: '规格管理' }
    },
    {
      path: 'stock',
      component: () => import('@/views/product/stock/index.vue'),
      name: 'ProductStock',
      meta: { title: '库存管理' }
    }
  ]
}

export default productRoutes 