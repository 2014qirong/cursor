import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getToken } from '@/utils/auth'

// 创建axios实例
const service = axios.create({
  baseURL: import.meta.env.VITE_APP_BASE_API || '',
  timeout: 10000
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    console.log(`[REQUEST] ${config.method.toUpperCase()} ${config.url}`, {
      params: config.params,
      data: config.data,
      headers: config.headers
    })
    
    // 如果存在token，添加到请求头中
    const token = getToken()
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
      console.log('[REQUEST] 添加认证token')
    }
    return config
  },
  error => {
    console.error('[REQUEST ERROR]', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    console.log(`[RESPONSE] ${response.config.method.toUpperCase()} ${response.config.url}`, {
      status: response.status,
      statusText: response.statusText,
      data: response.data
    })
    
    const res = response.data
    
    // 如果不需要特定的结果码判断，则直接返回数据
    if (!res.code) {
      console.log('[RESPONSE] 直接返回数据')
      return res
    }
    
    // 如果接口返回的code不是200，认为是错误
    if (res.code !== 200) {
      console.error('[RESPONSE ERROR]', {
        code: res.code,
        message: res.message
      })
      
      ElMessage({
        message: res.message || '请求失败',
        type: 'error',
        duration: 5 * 1000
      })
      
      // 50008: 非法令牌; 50012: 其他客户端已登录; 50014: 令牌过期;
      if (res.code === 50008 || res.code === 50012 || res.code === 50014) {
        console.log('[AUTH ERROR] 需要重新登录')
        // 重新登录
        ElMessageBox.confirm(
          '登录状态已过期，您可以继续留在该页面，或者重新登录',
          '系统提示',
          {
            confirmButtonText: '重新登录',
            cancelButtonText: '取消',
            type: 'warning'
          }
        ).then(() => {
          // 清除用户信息，重定向到登录页面
          localStorage.removeItem('token')
          location.reload()
        })
      }
      
      return Promise.reject(new Error(res.message || '请求失败'))
    } else {
      console.log('[RESPONSE] 请求成功')
      return res
    }
  },
  error => {
    console.error('[RESPONSE ERROR]', error)
    
    if (error.response) {
      // 请求已发出，但服务器响应的状态码不在 2xx 范围内
      console.error('[RESPONSE ERROR DETAIL]', {
        status: error.response.status,
        statusText: error.response.statusText,
        data: error.response.data
      })
      
      if (error.response.status === 401) {
        // 未授权，重定向到登录页
        console.log('[AUTH ERROR] 未授权，需要重新登录')
        ElMessageBox.confirm(
          '登录状态已过期，您可以继续留在该页面，或者重新登录',
          '系统提示',
          {
            confirmButtonText: '重新登录',
            cancelButtonText: '取消',
            type: 'warning'
          }
        ).then(() => {
          localStorage.removeItem('token')
          location.reload()
        })
      } else {
        let errorMessage = '服务器错误'
        if (error.response.data) {
          if (typeof error.response.data === 'string') {
            errorMessage = error.response.data
          } else if (error.response.data.message) {
            errorMessage = error.response.data.message
          } else if (error.response.data.error) {
            errorMessage = error.response.data.error
          }
        }
        
        ElMessage({
          message: errorMessage,
          type: 'error',
          duration: 5 * 1000
        })
      }
    } else if (error.request) {
      // 请求已发出，但没有收到响应
      console.error('[NETWORK ERROR] 请求未收到响应')
      ElMessage({
        message: '网络错误，请检查您的网络连接',
        type: 'error',
        duration: 5 * 1000
      })
    } else {
      // 在设置请求时发生了一些事情，触发了错误
      console.error('[REQUEST SETUP ERROR]', error.message)
      ElMessage({
        message: error.message || '请求错误',
        type: 'error',
        duration: 5 * 1000
      })
    }
    
    return Promise.reject(error)
  }
)

export default service 