import router from './router'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'
import { getToken } from '@/utils/auth'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/store/modules/user'

NProgress.configure({ showSpinner: false })

// 白名单路由
const whiteList = ['/login', '/404']

router.beforeEach(async (to, from, next) => {
  NProgress.start()
  
  document.title = to.meta.title ? `${to.meta.title} - 商城小程序后台管理系统` : '商城小程序后台管理系统'
  
  try {
    const hasToken = getToken()
    const userStore = useUserStore()

    if (hasToken) {
      if (to.path === '/login') {
        next({ path: '/' })
        NProgress.done()
      } else {
        // 判断是否已获取用户信息和角色
        const hasRoles = userStore.hasRoles
        console.log('当前用户角色状态:', hasRoles, '用户角色:', userStore.roles)
        
        if (hasRoles) {
          next()
        } else {
          try {
            // 获取用户信息
            const { roles } = await userStore.getUserInfo()
            console.log('成功获取用户角色:', roles)
            
            // 所有路由已在router/index.js中注册
            console.log('已注册的路由:', router.getRoutes().map(route => route.path))
            next({ ...to, replace: true })
          } catch (error) {
            // 获取用户信息失败，清除token并跳转到登录页
            await userStore.resetToken()
            ElMessage.error(error.message || '获取用户信息失败')
            next(`/login?redirect=${to.path}`)
            NProgress.done()
          }
        }
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