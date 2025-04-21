import { defineStore } from 'pinia'
import { getToken, setToken, removeToken } from '@/utils/auth'
// import { login, logout, getUserInfo } from '@/api/auth'

export const useUserStore = defineStore({
  id: 'user',
  state: () => ({
    token: getToken(),
    name: '',
    avatar: '',
    roles: [],
    permissions: []
  }),
  
  getters: {
    hasRoles: (state) => state.roles && state.roles.length > 0
  },
  
  actions: {
    // 设置Token
    setToken(token) {
      this.token = token
      setToken(token)
    },
    
    // 清除Token
    resetToken() {
      this.token = ''
      this.name = ''
      this.avatar = ''
      this.roles = []
      this.permissions = []
      removeToken()
    },
    
    // 登录
    async login(userInfo) {
      try {
        // 实际项目中应该调用登录接口
        // const { data } = await login(userInfo)
        // this.setToken(data.token)
        // return data
        
        // 模拟登录
        const token = 'admin-token'
        this.setToken(token)
        return { token }
      } catch (error) {
        console.error('登录失败:', error)
        throw error
      }
    },
    
    // 获取用户信息
    async getUserInfo() {
      try {
        // 实际项目中应该调用获取用户信息接口
        // const { data } = await getUserInfo()
        // const { roles, name, avatar, permissions } = data
        
        // 模拟用户信息 - 设置为管理员角色，拥有所有权限
        const roles = ['admin']
        const name = '管理员'
        const avatar = 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif'
        
        // 添加所有功能模块的权限 (使用*通配符表示拥有全部权限)
        const permissions = ['*:*:*']
        
        // 检查角色是否为非空数组
        if (!roles || roles.length <= 0) {
          throw new Error('用户角色不能为空!')
        }
        
        this.roles = roles
        this.name = name
        this.avatar = avatar
        this.permissions = permissions
        
        return { roles, name, avatar, permissions }
      } catch (error) {
        console.error('获取用户信息失败:', error)
        throw error
      }
    },
    
    // 登出
    async logout() {
      try {
        // 实际项目中应该调用登出接口
        // await logout()
        this.resetToken()
      } catch (error) {
        console.error('登出失败:', error)
        throw error
      }
    }
  }
}) 