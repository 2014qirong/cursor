const axios = require('axios');
const mysql = require('mysql2/promise');
const config = require('./config').development;

/**
 * 测试创建商品分类API
 */
async function testCreateCategory() {
  // 创建数据库连接
  const connection = await mysql.createConnection({
    host: config.host,
    port: config.port,
    user: config.username,
    password: config.password,
    database: config.database
  });
  
  console.log('数据库连接成功');
  
  try {
    // 生成随机分类名称，避免重复
    const categoryName = `测试分类_${new Date().getTime()}`;

    // 调用API创建商品分类
    console.log(`开始调用API创建商品分类: ${categoryName}`);
    const response = await axios.post('http://localhost:8080/api/product/category', {
      name: categoryName,
      parentId: 0,
      sort: 999,
      status: 1
    });
    
    console.log('API响应结果:', response.data);
    
    // 验证数据库中是否创建成功
    const [rows] = await connection.execute(
      'SELECT * FROM product_category WHERE name = ?',
      [categoryName]
    );
    
    if (rows.length > 0) {
      console.log('数据库验证成功，成功创建商品分类:', rows[0]);
    } else {
      console.error('数据库验证失败，未找到创建的商品分类');
    }
  } catch (error) {
    console.error('测试失败:', error.message);
    if (error.response) {
      console.error('API错误响应:', error.response.data);
    }
  } finally {
    // 关闭数据库连接
    await connection.end();
    console.log('数据库连接已关闭');
  }
}

/**
 * 测试创建文章API
 */
async function testCreateArticle() {
  // 创建数据库连接
  const connection = await mysql.createConnection({
    host: config.host,
    port: config.port,
    user: config.username,
    password: config.password,
    database: config.database
  });
  
  console.log('数据库连接成功');
  
  try {
    // 生成随机文章标题，避免重复
    const articleTitle = `测试文章_${new Date().getTime()}`;

    // 调用API创建文章
    console.log(`开始调用API创建文章: ${articleTitle}`);
    const response = await axios.post('http://localhost:8080/api/content/article', {
      title: articleTitle,
      categoryId: 2, // 行业资讯
      author: '测试作者',
      summary: '这是一篇测试文章的摘要',
      content: '<p>这是测试文章的内容</p>',
      coverImage: 'https://via.placeholder.com/400x300',
      isTop: 0,
      status: 1,
      sort: 999
    });
    
    console.log('API响应结果:', response.data);
    
    // 验证数据库中是否创建成功
    const [rows] = await connection.execute(
      'SELECT * FROM article WHERE title = ?',
      [articleTitle]
    );
    
    if (rows.length > 0) {
      console.log('数据库验证成功，成功创建文章:', rows[0]);
    } else {
      console.error('数据库验证失败，未找到创建的文章');
    }
  } catch (error) {
    console.error('测试失败:', error.message);
    if (error.response) {
      console.error('API错误响应:', error.response.data);
    }
  } finally {
    // 关闭数据库连接
    await connection.end();
    console.log('数据库连接已关闭');
  }
}

// 运行测试
console.log('开始API测试...');
// 根据需要选择要测试的API
testCreateCategory()
  .then(() => console.log('商品分类测试完成'))
  .catch(console.error);

// testCreateArticle()
//   .then(() => console.log('文章测试完成'))
//   .catch(console.error); 