/**
 * API测试脚本 - 创建一条商品分类数据
 */

const axios = require('axios');

// API基础URL
const baseURL = 'http://localhost:8080';

// 创建axios实例
const request = axios.create({
  baseURL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 添加请求拦截器
request.interceptors.request.use(
  config => {
    // 如果有token，可以在这里添加
    // const token = '...';
    // if (token) {
    //   config.headers['Authorization'] = `Bearer ${token}`;
    // }
    console.log(`发送${config.method.toUpperCase()}请求到: ${config.url}`);
    return config;
  },
  error => {
    console.error('请求错误:', error);
    return Promise.reject(error);
  }
);

// 添加响应拦截器
request.interceptors.response.use(
  response => {
    console.log('响应数据:', response.data);
    return response.data;
  },
  error => {
    console.error('响应错误:', error.response ? error.response.data : error.message);
    return Promise.reject(error);
  }
);

/**
 * 创建商品分类
 * @param {Object} data 分类数据
 */
async function createCategory(data) {
  try {
    const response = await request({
      url: '/api/product/category',
      method: 'post',
      data
    });
    console.log('创建商品分类成功:', response);
    return response;
  } catch (error) {
    console.error('创建商品分类失败:', error);
    throw error;
  }
}

// 测试数据
const testCategory = {
  name: '测试分类-' + new Date().toISOString().slice(0, 10),
  parent_id: 0,
  icon: 'https://example.com/icon.png',
  sort: 99,
  status: 1
};

// 执行测试
console.log('开始测试创建商品分类API...');
console.log('测试数据:', testCategory);

createCategory(testCategory)
  .then(result => {
    console.log('测试完成!');
    process.exit(0);
  })
  .catch(error => {
    console.error('测试失败!');
    process.exit(1);
  }); 