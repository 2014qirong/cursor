/**
 * API测试脚本 - 创建一条文章数据
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
 * 创建文章
 * @param {Object} data 文章数据
 */
async function createArticle(data) {
  try {
    const response = await request({
      url: '/api/content/article',
      method: 'post',
      data
    });
    console.log('创建文章成功:', response);
    return response;
  } catch (error) {
    console.error('创建文章失败:', error);
    throw error;
  }
}

// 测试数据
const testArticle = {
  title: '测试文章-' + new Date().toISOString(),
  category_id: 2, // 行业资讯
  author: '测试作者',
  cover_image: 'https://example.com/test-image.jpg',
  content: `<p>这是一篇测试文章，创建于 ${new Date().toLocaleString()}</p>
<p>文章包含<strong>加粗文本</strong>和<em>斜体文本</em>以及<a href="https://example.com">超链接</a>。</p>
<h2>测试标题</h2>
<p>测试段落内容，用于验证API功能是否正常工作。</p>`,
  summary: '这是一篇测试文章，用于验证API功能是否正常工作。',
  is_top: 0,
  status: 1,
  sort: 100
};

// 执行测试
console.log('开始测试创建文章API...');
console.log('测试数据:', testArticle);

createArticle(testArticle)
  .then(result => {
    console.log('测试完成!');
    process.exit(0);
  })
  .catch(error => {
    console.error('测试失败!');
    process.exit(1);
  }); 