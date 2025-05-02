const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const mysql = require('mysql2/promise');

const app = express();
const PORT = 3002;

const dbConfig = {
  host: 'localhost',
  user: 'dev_user',
  password: 'admin123',
  database: 'mall_dev',
  port: 3306
};

app.use(cors());
app.use(bodyParser.json());

// mock: 登录
app.post('/api/auth/login', (req, res) => {
  res.json({ code: 200, message: '登录成功', token: 'mock-token' });
});

// mock: 用户相关
app.get('/api/user/info', (req, res) => {
  res.json({ code: 200, message: '获取用户信息成功', data: { id: 1, username: 'admin', role: 'admin' } });
});

// 获取商品分类列表
app.get('/api/product/category', async (req, res) => {
  try {
    const connection = await mysql.createConnection(dbConfig);
    const [rows] = await connection.execute('SELECT * FROM product_categories');
    await connection.end();
    res.json({ code: 200, message: '获取分类成功', data: rows });
  } catch (err) {
    res.status(500).json({ code: 500, message: '数据库查询失败', error: err.message });
  }
});

// 为兼容前端API，添加 /list 路由
app.get('/api/product/category/list', async (req, res) => {
  try {
    const connection = await mysql.createConnection(dbConfig);
    const [rows] = await connection.execute('SELECT * FROM product_categories');
    await connection.end();
    res.json({ code: 200, message: '获取分类成功', data: rows });
  } catch (err) {
    res.status(500).json({ code: 500, message: '数据库查询失败', error: err.message });
  }
});

// 添加不带 /api 前缀的路由，保持与前端API定义一致
app.get('/product/category/list', async (req, res) => {
  try {
    const connection = await mysql.createConnection(dbConfig);
    const [rows] = await connection.execute('SELECT * FROM product_categories');
    await connection.end();
    res.json({ code: 200, message: '获取分类成功', data: rows });
  } catch (err) {
    res.status(500).json({ code: 500, message: '数据库查询失败', error: err.message });
  }
});

// 添加商品分类
app.post('/api/product/category', async (req, res) => {
  const { name, parent_id, icon, banner, sort_order, is_visible } = req.body;
  if (!name) {
    return res.status(400).json({ code: 400, message: '分类名称不能为空' });
  }
  try {
    const connection = await mysql.createConnection(dbConfig);
    const [result] = await connection.execute(
      'INSERT INTO product_categories (name, parent_id, icon, banner, sort_order, is_visible) VALUES (?, ?, ?, ?, ?, ?)',
      [name, parent_id || 0, icon || '', banner || '', sort_order || 0, is_visible !== undefined ? is_visible : 1]
    );
    await connection.end();
    res.json({ code: 200, message: '添加分类成功', data: { id: result.insertId, name, parent_id, icon, banner, sort_order, is_visible } });
  } catch (err) {
    res.status(500).json({ code: 500, message: '数据库插入失败', error: err.message });
  }
});

// mock: 商品
app.get('/product', (req, res) => {
  res.json({ code: 200, message: '获取商品列表成功', data: [{ id: 1, name: '电视', price: 1000 }] });
});
app.post('/product', (req, res) => {
  res.json({ code: 200, message: '添加商品成功', data: req.body });
});

// mock: 订单
app.get('/order', (req, res) => {
  res.json({ code: 200, message: '获取订单列表成功', data: [{ id: 1, user_id: 1, total: 2000 }] });
});
app.post('/order', (req, res) => {
  res.json({ code: 200, message: '创建订单成功', data: req.body });
});

// 为兼容前端API，添加 orders 路由（处理单复数不一致）
app.get('/orders', (req, res) => {
  res.json({ code: 200, message: '获取订单列表成功', data: [{ id: 1, user_id: 1, total: 2000 }] });
});
app.post('/orders', (req, res) => {
  res.json({ code: 200, message: '创建订单成功', data: req.body });
});

// mock: 内容
app.get('/content/article', (req, res) => {
  res.json({ code: 200, message: '获取文章列表成功', data: [{ id: 1, title: '测试文章' }] });
});
app.post('/content/article', (req, res) => {
  res.json({ code: 200, message: '添加文章成功', data: req.body });
});

// mock: 营销
app.get('/marketing/coupon', (req, res) => {
  res.json({ code: 200, message: '获取优惠券列表成功', data: [{ id: 1, name: '满100减10' }] });
});
app.post('/marketing/coupon', (req, res) => {
  res.json({ code: 200, message: '添加优惠券成功', data: req.body });
});

// mock: 系统
app.get('/system/role', (req, res) => {
  res.json({ code: 200, message: '获取角色列表成功', data: [{ id: 1, name: '管理员' }] });
});
app.post('/system/role', (req, res) => {
  res.json({ code: 200, message: '添加角色成功', data: req.body });
});

// mock: 统计
app.get('/statistics/overview', (req, res) => {
  res.json({ code: 200, message: '获取统计概览成功', data: { userCount: 100, orderCount: 50 } });
});

app.listen(PORT, () => {
  console.log(`API服务已启动，端口：${PORT}`);
}); 