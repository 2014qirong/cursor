/**
 * API测试脚本 - 登录并创建一条测试商品数据
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
    console.log('响应状态:', response.status);
    return response.data;
  },
  error => {
    console.error('响应错误:', error.response ? error.response.data : error.message);
    return Promise.reject(error);
  }
);

/**
 * 登录获取token
 */
async function login(username, password) {
  try {
    console.log(`尝试登录，用户名: ${username}`);
    const response = await request({
      url: '/api/auth/login',
      method: 'post',
      data: { username, password }
    });
    console.log('登录成功:', response);
    return response.token || response.data?.token;
  } catch (error) {
    console.error('登录失败:', error);
    throw error;
  }
}

/**
 * 创建一条产品数据
 */
async function createProduct(token, data) {
  try {
    const response = await request({
      url: '/api/product',
      method: 'post',
      headers: {
        'Authorization': `Bearer ${token}`
      },
      data
    });
    console.log('创建产品成功:', response);
    return response;
  } catch (error) {
    console.error('创建产品失败:', error);
    throw error;
  }
}

// 测试数据
const loginData = {
  username: 'admin',
  password: '123456'
};

const productData = {
  name: '测试商品-' + new Date().toISOString().slice(0, 19),
  category_id: 1, // 家电类
  price: 199.99,
  market_price: 299.99,
  stock: 100,
  main_image: 'https://example.com/test-product.jpg',
  description: '这是一个用于测试API的商品',
  detail: '<p>商品详情内容</p>',
  specs: JSON.stringify([
    { name: '颜色', values: ['红色', '蓝色', '黑色'] },
    { name: '尺寸', values: ['S', 'M', 'L'] }
  ]),
  status: 1
};

// 执行测试
async function runTest() {
  try {
    console.log('开始测试登录并创建商品...');
    // 1. 登录获取token
    const token = await login(loginData.username, loginData.password);
    
    if (!token) {
      throw new Error('登录成功但未获取到token');
    }
    
    console.log('获取到token:', token);
    
    // 2. 创建商品
    console.log('测试商品数据:', productData);
    await createProduct(token, productData);
    
    console.log('测试完成!');
    process.exit(0);
  } catch (error) {
    console.error('测试过程中发生错误:', error);
    process.exit(1);
  }
}

runTest(); 