import Layout from '@/layout/index.vue'

const systemRoutes = {
  path: '/system',
  component: Layout,
  redirect: '/system/base',
  name: 'System',
  meta: { title: '系统设置', icon: 'Setting' },
  children: [
    {
      path: 'base',
      component: () => import('@/views/system/base/index.vue'),
      name: 'SystemBase',
      meta: { title: '基础设置' }
    },
    {
      path: 'payment',
      component: () => import('@/views/system/payment/index.vue'),
      name: 'Payment',
      meta: { title: '支付设置' }
    },
    {
      path: 'logistics',
      component: () => import('@/views/system/logistics/index.vue'),
      name: 'Logistics',
      meta: { title: '物流配置' }
    },
    {
      path: 'sms',
      component: () => import('@/views/system/sms/index.vue'),
      name: 'Sms',
      meta: { title: '短信配置' }
    },
    {
      path: 'permission',
      component: () => import('@/views/system/permission/index.vue'),
      name: 'Permission',
      meta: { title: '权限管理' }
    },
    {
      path: 'role',
      component: () => import('@/views/system/role/index.vue'),
      name: 'Role',
      meta: { title: '角色管理' }
    },
    {
      path: 'admin',
      component: () => import('@/views/system/admin/index.vue'),
      name: 'Admin',
      meta: { title: '管理员管理' }
    },
    {
      path: 'log',
      component: () => import('@/views/system/log/index.vue'),
      name: 'Log',
      meta: { title: '操作日志' }
    }
  ]
}

export default systemRoutes 