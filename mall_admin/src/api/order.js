import request from '@/utils/request'

/**
 * 获取订单列表
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getOrderList(params) {
  return request({
    url: '/orders',
    method: 'get',
    params
  })
}

/**
 * 获取订单详情
 * @param {String} id 订单ID
 * @returns {Promise} 返回Promise
 */
export function getOrderDetail(id) {
  return request({
    url: `/orders/${id}`,
    method: 'get'
  })
}

/**
 * 更新订单状态
 * @param {String} id 订单ID
 * @param {Object} data 更新数据
 * @returns {Promise} 返回Promise
 */
export function updateOrderStatus(id, data) {
  return request({
    url: `/orders/${id}/status`,
    method: 'put',
    data
  })
}

/**
 * 确认发货
 * @param {String} id 订单ID
 * @param {Object} data 发货信息
 * @returns {Promise} 返回Promise
 */
export function shipOrder(id, data) {
  return request({
    url: `/orders/${id}/ship`,
    method: 'post',
    data
  })
}

/**
 * 取消订单
 * @param {String} id 订单ID
 * @param {Object} data 取消原因
 * @returns {Promise} 返回Promise
 */
export function cancelOrder(id, data) {
  return request({
    url: `/orders/${id}/cancel`,
    method: 'post',
    data
  })
}

/**
 * 获取退款/售后列表
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getRefundList(params) {
  return request({
    url: '/orders/refunds',
    method: 'get',
    params
  })
}

/**
 * 获取退款详情
 * @param {String} id 退款ID
 * @returns {Promise} 返回Promise
 */
export function getRefundDetail(id) {
  return request({
    url: `/orders/refunds/${id}`,
    method: 'get'
  })
}

/**
 * 处理退款申请
 * @param {String} id 退款ID
 * @param {Object} data 处理结果
 * @returns {Promise} 返回Promise
 */
export function processRefund(id, data) {
  return request({
    url: `/orders/refunds/${id}/process`,
    method: 'post',
    data
  })
}

/**
 * 批量发货
 * @param {Array} data 批量发货数据
 * @returns {Promise} 返回Promise
 */
export function batchShipOrders(data) {
  return request({
    url: '/orders/batch-ship',
    method: 'post',
    data
  })
}

/**
 * 导出订单数据
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function exportOrders(params) {
  return request({
    url: '/orders/export',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

/**
 * 添加订单备注
 * @param {String} id 订单ID
 * @param {Object} data 备注信息
 * @returns {Promise} 返回Promise
 */
export function addOrderRemark(id, data) {
  return request({
    url: `/orders/${id}/remark`,
    method: 'post',
    data
  })
}

/**
 * 获取物流公司列表
 * @returns {Promise} 返回Promise
 */
export function getShippingCompanies() {
  return request({
    url: '/shipping/companies',
    method: 'get'
  })
}

/**
 * 获取物流信息
 * @param {String} id 订单ID
 * @returns {Promise} 返回Promise
 */
export function getShippingInfo(id) {
  return request({
    url: `/orders/${id}/shipping`,
    method: 'get'
  })
}

/**
 * 获取退款原因统计
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getRefundReasonStats(params) {
  return request({
    url: '/orders/refunds/reasons/stats',
    method: 'get',
    params
  })
} 