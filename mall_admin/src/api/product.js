import request from '@/utils/request'

/**
 * 获取商品列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getProductList(params) {
  return request({
    url: '/product/list',
    method: 'get',
    params
  })
}

/**
 * 获取商品详情
 * @param {number|string} id - 商品ID
 * @returns {Promise}
 */
export function getProductDetail(id) {
  return request({
    url: `/product/${id}`,
    method: 'get'
  })
}

/**
 * 创建商品
 * @param {Object} data - 商品数据
 * @returns {Promise}
 */
export function createProduct(data) {
  return request({
    url: '/product',
    method: 'post',
    data
  })
}

/**
 * 更新商品
 * @param {number|string} id - 商品ID
 * @param {Object} data - 商品数据
 * @returns {Promise}
 */
export function updateProduct(id, data) {
  return request({
    url: `/product/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除商品
 * @param {number|string} id - 商品ID
 * @returns {Promise}
 */
export function deleteProduct(id) {
  return request({
    url: `/product/${id}`,
    method: 'delete'
  })
}

/**
 * 批量删除商品
 * @param {Array} ids - 商品ID数组
 * @returns {Promise}
 */
export function batchDeleteProducts(ids) {
  return request({
    url: '/product/batch',
    method: 'delete',
    data: { ids }
  })
}

/**
 * 更新商品状态
 * @param {number|string} id - 商品ID
 * @param {number} status - 状态值(0-下架，1-上架)
 * @returns {Promise}
 */
export function updateProductStatus(id, status) {
  return request({
    url: `/product/${id}/status`,
    method: 'patch',
    data: { status }
  })
}

/**
 * 获取商品分类列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getCategoryList(params) {
  return request({
    url: '/product/category/list',
    method: 'get',
    params
  })
}

/**
 * 创建商品分类
 * @param {Object} data - 分类数据
 * @returns {Promise}
 */
export function createCategory(data) {
  return request({
    url: '/product/category',
    method: 'post',
    data
  })
}

/**
 * 更新商品分类
 * @param {number|string} id - 分类ID
 * @param {Object} data - 分类数据
 * @returns {Promise}
 */
export function updateCategory(id, data) {
  return request({
    url: `/product/category/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除商品分类
 * @param {number|string} id - 分类ID
 * @returns {Promise}
 */
export function deleteCategory(id) {
  return request({
    url: `/product/category/${id}`,
    method: 'delete'
  })
}

/**
 * 获取商品属性列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getAttributeList(params) {
  return request({
    url: '/product/attribute/list',
    method: 'get',
    params
  })
}

/**
 * 创建商品属性
 * @param {Object} data - 属性数据
 * @returns {Promise}
 */
export function createAttribute(data) {
  return request({
    url: '/product/attribute',
    method: 'post',
    data
  })
}

/**
 * 更新商品属性
 * @param {number|string} id - 属性ID
 * @param {Object} data - 属性数据
 * @returns {Promise}
 */
export function updateAttribute(id, data) {
  return request({
    url: `/product/attribute/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除商品属性
 * @param {number|string} id - 属性ID
 * @returns {Promise}
 */
export function deleteAttribute(id) {
  return request({
    url: `/product/attribute/${id}`,
    method: 'delete'
  })
}

/**
 * 获取商品品牌列表
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function getBrandList(params) {
  return request({
    url: '/product/brand/list',
    method: 'get',
    params
  })
}

/**
 * 导出商品数据
 * @param {Object} params - 查询参数
 * @returns {Promise}
 */
export function exportProductData(params) {
  return request({
    url: '/product/export',
    method: 'get',
    params,
    responseType: 'blob'
  })
} 