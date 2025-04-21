import request from '@/utils/request'

/**
 * 获取轮播图列表
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getBannerList(params) {
  return request({
    url: '/content/banner/list',
    method: 'get',
    params
  })
}

/**
 * 获取轮播图详情
 * @param {String} id 轮播图ID
 * @returns {Promise} 返回Promise
 */
export function getBannerDetail(id) {
  return request({
    url: `/content/banner/${id}`,
    method: 'get'
  })
}

/**
 * 添加轮播图
 * @param {Object} data 轮播图数据
 * @returns {Promise} 返回Promise
 */
export function addBanner(data) {
  return request({
    url: '/content/banner',
    method: 'post',
    data
  })
}

/**
 * 更新轮播图
 * @param {String} id 轮播图ID
 * @param {Object} data 更新数据
 * @returns {Promise} 返回Promise
 */
export function updateBanner(id, data) {
  return request({
    url: `/content/banner/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除轮播图
 * @param {String} id 轮播图ID
 * @returns {Promise} 返回Promise
 */
export function deleteBanner(id) {
  return request({
    url: `/content/banner/${id}`,
    method: 'delete'
  })
}

/**
 * 获取公告列表
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getNoticeList(params) {
  return request({
    url: '/content/notice/list',
    method: 'get',
    params
  })
}

/**
 * 获取公告详情
 * @param {String} id 公告ID
 * @returns {Promise} 返回Promise
 */
export function getNoticeDetail(id) {
  return request({
    url: `/content/notice/${id}`,
    method: 'get'
  })
}

/**
 * 添加公告
 * @param {Object} data 公告数据
 * @returns {Promise} 返回Promise
 */
export function addNotice(data) {
  return request({
    url: '/content/notice',
    method: 'post',
    data
  })
}

/**
 * 更新公告
 * @param {String} id 公告ID
 * @param {Object} data 更新数据
 * @returns {Promise} 返回Promise
 */
export function updateNotice(id, data) {
  return request({
    url: `/content/notice/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除公告
 * @param {String} id 公告ID
 * @returns {Promise} 返回Promise
 */
export function deleteNotice(id) {
  return request({
    url: `/content/notice/${id}`,
    method: 'delete'
  })
}

/**
 * 获取推荐位列表
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getRecommendList(params) {
  return request({
    url: '/content/recommends',
    method: 'get',
    params
  })
}

/**
 * 添加推荐位
 * @param {Object} data 推荐位数据
 * @returns {Promise} 返回Promise
 */
export function addRecommend(data) {
  return request({
    url: '/content/recommends',
    method: 'post',
    data
  })
}

/**
 * 更新推荐位
 * @param {String} id 推荐位ID
 * @param {Object} data 更新数据
 * @returns {Promise} 返回Promise
 */
export function updateRecommend(id, data) {
  return request({
    url: `/content/recommends/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除推荐位
 * @param {String} id 推荐位ID
 * @returns {Promise} 返回Promise
 */
export function deleteRecommend(id) {
  return request({
    url: `/content/recommends/${id}`,
    method: 'delete'
  })
}

/**
 * 获取专题页面列表
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getTopicList(params) {
  return request({
    url: '/content/topics',
    method: 'get',
    params
  })
}

/**
 * 添加专题页面
 * @param {Object} data 专题页面数据
 * @returns {Promise} 返回Promise
 */
export function addTopic(data) {
  return request({
    url: '/content/topics',
    method: 'post',
    data
  })
}

/**
 * 更新专题页面
 * @param {String} id 专题页面ID
 * @param {Object} data 更新数据
 * @returns {Promise} 返回Promise
 */
export function updateTopic(id, data) {
  return request({
    url: `/content/topics/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除专题页面
 * @param {String} id 专题页面ID
 * @returns {Promise} 返回Promise
 */
export function deleteTopic(id) {
  return request({
    url: `/content/topics/${id}`,
    method: 'delete'
  })
}

/**
 * 获取文章分类列表
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getArticleCategoryList(params) {
  return request({
    url: '/content/article-categories',
    method: 'get',
    params
  })
}

/**
 * 添加文章分类
 * @param {Object} data 文章分类数据
 * @returns {Promise} 返回Promise
 */
export function addArticleCategory(data) {
  return request({
    url: '/content/article-categories',
    method: 'post',
    data
  })
}

/**
 * 更新文章分类
 * @param {String} id 文章分类ID
 * @param {Object} data 更新数据
 * @returns {Promise} 返回Promise
 */
export function updateArticleCategory(id, data) {
  return request({
    url: `/content/article-categories/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除文章分类
 * @param {String} id 文章分类ID
 * @returns {Promise} 返回Promise
 */
export function deleteArticleCategory(id) {
  return request({
    url: `/content/article-categories/${id}`,
    method: 'delete'
  })
}

/**
 * 获取文章列表
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getArticleList(params) {
  return request({
    url: '/content/articles',
    method: 'get',
    params
  })
}

/**
 * 获取文章详情
 * @param {String} id 文章ID
 * @returns {Promise} 返回Promise
 */
export function getArticleDetail(id) {
  return request({
    url: `/content/articles/${id}`,
    method: 'get'
  })
}

/**
 * 添加文章
 * @param {Object} data 文章数据
 * @returns {Promise} 返回Promise
 */
export function addArticle(data) {
  return request({
    url: '/content/articles',
    method: 'post',
    data
  })
}

/**
 * 更新文章
 * @param {String} id 文章ID
 * @param {Object} data 更新数据
 * @returns {Promise} 返回Promise
 */
export function updateArticle(id, data) {
  return request({
    url: `/content/articles/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除文章
 * @param {String} id 文章ID
 * @returns {Promise} 返回Promise
 */
export function deleteArticle(id) {
  return request({
    url: `/content/articles/${id}`,
    method: 'delete'
  })
}

/**
 * 上传图片
 * @param {FormData} data 图片数据
 * @returns {Promise} 返回Promise
 */
export function uploadImage(data) {
  return request({
    url: '/content/upload',
    method: 'post',
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    data
  })
}

/**
 * 获取帮助中心分类列表
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getHelpCategoryList(params) {
  return request({
    url: '/content/help/category/list',
    method: 'get',
    params
  })
}

/**
 * 获取帮助中心分类详情
 * @param {String} id 分类ID
 * @returns {Promise} 返回Promise
 */
export function getHelpCategoryDetail(id) {
  return request({
    url: `/content/help/category/${id}`,
    method: 'get'
  })
}

/**
 * 添加帮助中心分类
 * @param {Object} data 分类数据
 * @returns {Promise} 返回Promise
 */
export function addHelpCategory(data) {
  return request({
    url: '/content/help/category',
    method: 'post',
    data
  })
}

/**
 * 更新帮助中心分类
 * @param {String} id 分类ID
 * @param {Object} data 更新数据
 * @returns {Promise} 返回Promise
 */
export function updateHelpCategory(id, data) {
  return request({
    url: `/content/help/category/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除帮助中心分类
 * @param {String} id 分类ID
 * @returns {Promise} 返回Promise
 */
export function deleteHelpCategory(id) {
  return request({
    url: `/content/help/category/${id}`,
    method: 'delete'
  })
}

/**
 * 获取帮助中心文章列表
 * @param {Object} params 查询参数
 * @returns {Promise} 返回Promise
 */
export function getHelpArticleList(params) {
  return request({
    url: '/content/help/article/list',
    method: 'get',
    params
  })
}

/**
 * 获取帮助中心文章详情
 * @param {String} id 文章ID
 * @returns {Promise} 返回Promise
 */
export function getHelpArticleDetail(id) {
  return request({
    url: `/content/help/article/${id}`,
    method: 'get'
  })
}

/**
 * 添加帮助中心文章
 * @param {Object} data 文章数据
 * @returns {Promise} 返回Promise
 */
export function addHelpArticle(data) {
  return request({
    url: '/content/help/article',
    method: 'post',
    data
  })
}

/**
 * 更新帮助中心文章
 * @param {String} id 文章ID
 * @param {Object} data 更新数据
 * @returns {Promise} 返回Promise
 */
export function updateHelpArticle(id, data) {
  return request({
    url: `/content/help/article/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除帮助中心文章
 * @param {String} id 文章ID
 * @returns {Promise} 返回Promise
 */
export function deleteHelpArticle(id) {
  return request({
    url: `/content/help/article/${id}`,
    method: 'delete'
  })
} 