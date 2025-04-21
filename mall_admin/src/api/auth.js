import request from '@/utils/request'

/**
 * 登录接口
 * @param {Object} data
 * @param {string} data.username 用户名
 * @param {string} data.password 密码
 * @returns {Promise}
 */
export function login(data) {
  return request({
    url: '/auth/login',
    method: 'post',
    data
  })
}

/**
 * 登出接口
 * @returns {Promise}
 */
export function logout() {
  return request({
    url: '/auth/logout',
    method: 'post'
  })
}

/**
 * 获取用户信息接口
 * @returns {Promise}
 */
export function getUserInfo() {
  return request({
    url: '/auth/info',
    method: 'get'
  })
}

/**
 * 修改密码接口
 * @param {Object} data
 * @param {string} data.oldPassword 旧密码
 * @param {string} data.newPassword 新密码
 * @returns {Promise}
 */
export function updatePassword(data) {
  return request({
    url: '/auth/password',
    method: 'put',
    data
  })
} 