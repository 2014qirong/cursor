import request from '@/utils/request'

/**
 * 获取销售统计数据
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getSalesStatistics(params) {
  return request({
    url: '/statistics/sales',
    method: 'get',
    params
  })
}

/**
 * 获取用户数据统计
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getUserStatistics(params) {
  return request({
    url: '/statistics/users',
    method: 'get',
    params
  })
}

/**
 * 获取商品数据统计
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getProductStatistics(params) {
  return request({
    url: '/statistics/products',
    method: 'get',
    params
  })
}

/**
 * 导出销售数据
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function exportSalesData(params) {
  return request({
    url: '/statistics/sales/export',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

/**
 * 获取数据总览
 * @returns {Promise} 返回Promise
 */
export function getDashboardData() {
  return request({
    url: '/statistics/dashboard',
    method: 'get'
  })
} 