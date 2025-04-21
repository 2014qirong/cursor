import request from '@/utils/request'

/**
 * 获取促销活动列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getPromotionList(params) {
  return request({
    url: '/marketing/promotions',
    method: 'get',
    params
  })
}

/**
 * 获取促销活动详情
 * @param {number|string} id - 活动ID
 * @returns {Promise}
 */
export function getPromotionDetail(id) {
  return request({
    url: `/marketing/promotion/${id}`,
    method: 'get'
  })
}

/**
 * 创建促销活动
 * @param {Object} data - 活动数据
 * @returns {Promise}
 */
export function createPromotion(data) {
  return request({
    url: '/marketing/promotion',
    method: 'post',
    data
  })
}

/**
 * 更新促销活动
 * @param {number|string} id - 活动ID
 * @param {Object} data - 活动数据
 * @returns {Promise}
 */
export function updatePromotion(id, data) {
  return request({
    url: `/marketing/promotion/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除促销活动
 * @param {number|string} id - 活动ID
 * @returns {Promise}
 */
export function deletePromotion(id) {
  return request({
    url: `/marketing/promotion/${id}`,
    method: 'delete'
  })
}

/**
 * 更新促销活动状态
 * @param {number|string} id - 活动ID
 * @param {number} status - 状态值(0-禁用，1-启用)
 * @returns {Promise}
 */
export function updatePromotionStatus(id, status) {
  return request({
    url: `/marketing/promotion/${id}/status`,
    method: 'patch',
    data: { status }
  })
}

/**
 * 获取优惠券列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getCouponList(params) {
  return request({
    url: '/marketing/coupon/list',
    method: 'get',
    params
  })
}

/**
 * 获取优惠券详情
 * @param {number|string} id - 优惠券ID
 * @returns {Promise}
 */
export function getCouponDetail(id) {
  return request({
    url: `/marketing/coupon/${id}`,
    method: 'get'
  })
}

/**
 * 创建优惠券
 * @param {Object} data - 优惠券数据
 * @returns {Promise}
 */
export function createCoupon(data) {
  return request({
    url: '/marketing/coupon',
    method: 'post',
    data
  })
}

/**
 * 更新优惠券
 * @param {number|string} id - 优惠券ID
 * @param {Object} data - 优惠券数据
 * @returns {Promise}
 */
export function updateCoupon(id, data) {
  return request({
    url: `/marketing/coupon/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除优惠券
 * @param {number|string} id - 优惠券ID
 * @returns {Promise}
 */
export function deleteCoupon(id) {
  return request({
    url: `/marketing/coupon/${id}`,
    method: 'delete'
  })
}

/**
 * 发放优惠券
 * @param {number|string} id - 优惠券ID
 * @param {Object} data - 发放数据
 * @returns {Promise}
 */
export function issueCoupon(id, data) {
  return request({
    url: `/marketing/coupon/${id}/issue`,
    method: 'post',
    data
  })
}

/**
 * 获取秒杀活动列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getFlashSaleList(params) {
  return request({
    url: '/marketing/flash-sale/list',
    method: 'get',
    params
  })
}

/**
 * 获取秒杀活动详情
 * @param {number|string} id - 活动ID
 * @returns {Promise}
 */
export function getFlashSaleDetail(id) {
  return request({
    url: `/marketing/flash-sale/${id}`,
    method: 'get'
  })
}

/**
 * 创建秒杀活动
 * @param {Object} data - 活动数据
 * @returns {Promise}
 */
export function createFlashSale(data) {
  return request({
    url: '/marketing/flash-sale',
    method: 'post',
    data
  })
}

/**
 * 更新秒杀活动
 * @param {number|string} id - 活动ID
 * @param {Object} data - 活动数据
 * @returns {Promise}
 */
export function updateFlashSale(id, data) {
  return request({
    url: `/marketing/flash-sale/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除秒杀活动
 * @param {number|string} id - 活动ID
 * @returns {Promise}
 */
export function deleteFlashSale(id) {
  return request({
    url: `/marketing/flash-sale/${id}`,
    method: 'delete'
  })
}

/**
 * 获取营销数据统计
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getMarketingStats(params) {
  return request({
    url: '/marketing/stats',
    method: 'get',
    params
  })
} 