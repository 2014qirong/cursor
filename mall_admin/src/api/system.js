import request from '@/utils/request'

/**
 * 获取管理员列表
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getAdminList(params) {
  return request({
    url: '/system/admins',
    method: 'get',
    params
  })
}

/**
 * 添加管理员
 * @param {Object} data 管理员数据
 * @returns {Promise} 返回Promise
 */
export function addAdmin(data) {
  return request({
    url: '/system/admins',
    method: 'post',
    data
  })
}

/**
 * 更新管理员
 * @param {String} id 管理员ID
 * @param {Object} data 更新数据
 * @returns {Promise} 返回Promise
 */
export function updateAdmin(id, data) {
  return request({
    url: `/system/admins/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除管理员
 * @param {String} id 管理员ID
 * @returns {Promise} 返回Promise
 */
export function deleteAdmin(id) {
  return request({
    url: `/system/admins/${id}`,
    method: 'delete'
  })
}

/**
 * 获取角色列表
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getRoleList(params) {
  return request({
    url: '/system/roles',
    method: 'get',
    params
  })
}

/**
 * 添加角色
 * @param {Object} data 角色数据
 * @returns {Promise} 返回Promise
 */
export function addRole(data) {
  return request({
    url: '/system/roles',
    method: 'post',
    data
  })
}

/**
 * 更新角色
 * @param {String} id 角色ID
 * @param {Object} data 更新数据
 * @returns {Promise} 返回Promise
 */
export function updateRole(id, data) {
  return request({
    url: `/system/roles/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除角色
 * @param {String} id 角色ID
 * @returns {Promise} 返回Promise
 */
export function deleteRole(id) {
  return request({
    url: `/system/roles/${id}`,
    method: 'delete'
  })
}

/**
 * 获取角色权限
 * @param {String} id 角色ID
 * @returns {Promise} 返回Promise
 */
export function getRolePermissions(id) {
  return request({
    url: `/system/roles/${id}/permissions`,
    method: 'get'
  })
}

/**
 * 更新角色权限
 * @param {String} id 角色ID
 * @param {Object} data 权限数据
 * @returns {Promise} 返回Promise
 */
export function updateRolePermissions(id, data) {
  return request({
    url: `/system/roles/${id}/permissions`,
    method: 'put',
    data
  })
}

/**
 * 获取所有权限列表
 * @returns {Promise} 返回Promise
 */
export function getAllPermissions() {
  return request({
    url: '/system/permissions',
    method: 'get'
  })
}

/**
 * 获取操作日志
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getOperationLogs(params) {
  return request({
    url: '/system/logs/operation',
    method: 'get',
    params
  })
}

/**
 * 获取登录日志
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getLoginLogs(params) {
  return request({
    url: '/system/logs/login',
    method: 'get',
    params
  })
}

/**
 * 获取系统配置
 * @param {String} key 配置键
 * @returns {Promise} 返回Promise
 */
export function getSystemConfig(key) {
  return request({
    url: '/system/config',
    method: 'get',
    params: { key }
  })
}

/**
 * 更新系统配置
 * @param {Object} data 配置数据
 * @returns {Promise} 返回Promise
 */
export function updateSystemConfig(data) {
  return request({
    url: '/system/config',
    method: 'put',
    data
  })
}

/**
 * 获取短信配置
 * @returns {Promise} 返回Promise
 */
export function getSmsConfig() {
  return request({
    url: '/system/sms/config',
    method: 'get'
  })
}

/**
 * 更新短信配置
 * @param {Object} data 配置数据
 * @returns {Promise} 返回Promise
 */
export function updateSmsConfig(data) {
  return request({
    url: '/system/sms/config',
    method: 'put',
    data
  })
}

/**
 * 获取短信模板列表
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getSmsTemplates(params) {
  return request({
    url: '/system/sms/templates',
    method: 'get',
    params
  })
}

/**
 * 添加短信模板
 * @param {Object} data 模板数据
 * @returns {Promise} 返回Promise
 */
export function addSmsTemplate(data) {
  return request({
    url: '/system/sms/templates',
    method: 'post',
    data
  })
}

/**
 * 更新短信模板
 * @param {String} id 模板ID
 * @param {Object} data 更新数据
 * @returns {Promise} 返回Promise
 */
export function updateSmsTemplate(id, data) {
  return request({
    url: `/system/sms/templates/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除短信模板
 * @param {String} id 模板ID
 * @returns {Promise} 返回Promise
 */
export function deleteSmsTemplate(id) {
  return request({
    url: `/system/sms/templates/${id}`,
    method: 'delete'
  })
}

/**
 * 获取支付配置
 * @returns {Promise} 返回Promise
 */
export function getPaymentConfig() {
  return request({
    url: '/system/payment/config',
    method: 'get'
  })
}

/**
 * 更新支付配置
 * @param {Object} data 配置数据
 * @returns {Promise} 返回Promise
 */
export function updatePaymentConfig(data) {
  return request({
    url: '/system/payment/config',
    method: 'put',
    data
  })
}

/**
 * 获取物流公司列表
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getShippingCompanies(params) {
  return request({
    url: '/system/shipping/companies',
    method: 'get',
    params
  })
}

/**
 * 添加物流公司
 * @param {Object} data 物流公司数据
 * @returns {Promise} 返回Promise
 */
export function addShippingCompany(data) {
  return request({
    url: '/system/shipping/companies',
    method: 'post',
    data
  })
}

/**
 * 更新物流公司
 * @param {String} id 物流公司ID
 * @param {Object} data 更新数据
 * @returns {Promise} 返回Promise
 */
export function updateShippingCompany(id, data) {
  return request({
    url: `/system/shipping/companies/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除物流公司
 * @param {String} id 物流公司ID
 * @returns {Promise} 返回Promise
 */
export function deleteShippingCompany(id) {
  return request({
    url: `/system/shipping/companies/${id}`,
    method: 'delete'
  })
}

/**
 * 获取运费模板列表
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getShippingTemplates(params) {
  return request({
    url: '/system/shipping/templates',
    method: 'get',
    params
  })
}

/**
 * 添加运费模板
 * @param {Object} data 运费模板数据
 * @returns {Promise} 返回Promise
 */
export function addShippingTemplate(data) {
  return request({
    url: '/system/shipping/templates',
    method: 'post',
    data
  })
}

/**
 * 更新运费模板
 * @param {String} id 运费模板ID
 * @param {Object} data 更新数据
 * @returns {Promise} 返回Promise
 */
export function updateShippingTemplate(id, data) {
  return request({
    url: `/system/shipping/templates/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除运费模板
 * @param {String} id 运费模板ID
 * @returns {Promise} 返回Promise
 */
export function deleteShippingTemplate(id) {
  return request({
    url: `/system/shipping/templates/${id}`,
    method: 'delete'
  })
} 