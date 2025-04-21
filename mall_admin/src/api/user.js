import request from '@/utils/request'

/**
 * 获取用户列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getUserList(params) {
  return request({
    url: '/user/list',
    method: 'get',
    params
  })
}

/**
 * 获取用户详情
 * @param {number|string} id - 用户ID
 * @returns {Promise}
 */
export function getUserDetail(id) {
  return request({
    url: `/user/${id}`,
    method: 'get'
  })
}

/**
 * 创建新用户
 * @param {Object} data - 用户数据
 * @returns {Promise}
 */
export function createUser(data) {
  return request({
    url: '/user',
    method: 'post',
    data
  })
}

/**
 * 更新用户信息
 * @param {number|string} id - 用户ID
 * @param {Object} data - 用户数据
 * @returns {Promise}
 */
export function updateUser(id, data) {
  return request({
    url: `/user/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除用户
 * @param {number|string} id - 用户ID
 * @returns {Promise}
 */
export function deleteUser(id) {
  return request({
    url: `/user/${id}`,
    method: 'delete'
  })
}

/**
 * 批量删除用户
 * @param {Array} ids - 用户ID数组
 * @returns {Promise}
 */
export function batchDeleteUsers(ids) {
  return request({
    url: '/user/batch',
    method: 'delete',
    data: { ids }
  })
}

/**
 * 修改用户状态
 * @param {number|string} id - 用户ID
 * @param {number} status - 状态值(0-禁用，1-启用)
 * @returns {Promise}
 */
export function updateUserStatus(id, status) {
  return request({
    url: `/user/${id}/status`,
    method: 'patch',
    data: { status }
  })
}

/**
 * 获取用户等级列表
 * @returns {Promise}
 */
export function getUserLevels() {
  return request({
    url: '/user/levels',
    method: 'get'
  })
}

/**
 * 获取用户统计数据
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getUserStats(params) {
  return request({
    url: '/user/stats',
    method: 'get',
    params
  })
} 