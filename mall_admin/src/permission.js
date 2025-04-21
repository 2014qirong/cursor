import router from './router'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import { getToken } from '@/utils/auth'
import { ElMessage } from 'element-plus'

NProgress.configure({ showSpinner: false })

// 白名单路由
const whiteList = ['/login', '/404']

router.beforeEach(async (to, from, next) => {
  NProgress.start()
  
  document.title = to.meta.title ? `${to.meta.title} - 商城小程序后台管理系统` : '商城小程序后台管理系统'
  
  try {
    const hasToken = getToken()

    if (hasToken) {
      if (to.path === '/login') {
        next({ path: '/' })
        NProgress.done()
      } else {
        // 这里可以添加获取用户信息和权限判断
        // const hasRoles = store.getters.roles && store.getters.roles.length > 0
        // 如果没有获取过用户信息，在这里获取
        next()
      }
    } else {
      if (whiteList.indexOf(to.path) !== -1) {
        next()
      } else {
        next(`/login?redirect=${to.path}`)
        ElMessage.warning('请先登录')
        NProgress.done()
      }
    }
  } catch (error) {
    console.error('路由导航错误:', error)
    next('/login')
    NProgress.done()
  }
})

router.afterEach(() => {
  NProgress.done()
}) 