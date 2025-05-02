const express = require('express');
const mysql = require('mysql2/promise');
const app = express();

// 数据库配置
const dbConfig = {
  host: process.env.DB_HOST || 'localhost',
  port: process.env.DB_PORT || 3306,
  user: process.env.DB_USER || 'dev_user',
  password: process.env.DB_PASSWORD || 'admin123',
  database: process.env.DB_DATABASE || 'mall_dev'
};

// 添加中间件
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 请求日志中间件
app.use((req, res, next) => {
  console.log(`[${new Date().toISOString()}] ${req.method} ${req.url}`);
  next();
});

// 统一响应格式中间件
app.use((req, res, next) => {
  res.success = (data, message = '操作成功') => {
    res.json({ code: 200, message, data });
  };
  res.error = (message = '操作失败', code = 500) => {
    res.status(code).json({ code, message });
  };
  next();
});

// 错误处理中间件
app.use((err, req, res, next) => {
  console.error('服务器错误:', err);
  res.error(err.message || '服务器内部错误');
});

// 商品分类路由
const categoryRouter = express.Router();

// 根路径处理
categoryRouter.get('/', async (req, res) => {
  try {
    const connection = await mysql.createConnection(dbConfig);
    const [rows] = await connection.execute('SELECT * FROM product_categories');
    await connection.end();
    res.success(rows, '获取分类成功');
  } catch (err) {
    console.error('数据库查询失败:', err);
    res.error('数据库查询失败');
  }
});

// 获取分类列表
categoryRouter.get('/list', async (req, res) => {
  try {
    const connection = await mysql.createConnection(dbConfig);
    const [rows] = await connection.execute('SELECT * FROM product_categories');
    await connection.end();
    res.success(rows, '获取分类成功');
  } catch (err) {
    console.error('数据库查询失败:', err);
    res.error('数据库查询失败');
  }
});

// 添加分类
categoryRouter.post('/', async (req, res) => {
  try {
    const { name, parent_id = 0 } = req.body;
    if (!name) {
      return res.error('分类名称不能为空', 400);
    }
    
    const connection = await mysql.createConnection(dbConfig);
    const [result] = await connection.execute(
      'INSERT INTO product_categories (name, parent_id) VALUES (?, ?)',
      [name, parent_id]
    );
    await connection.end();
    
    res.success({ id: result.insertId, name, parent_id }, '添加分类成功');
  } catch (err) {
    console.error('添加分类失败:', err);
    res.error('添加分类失败');
  }
});

// 获取单个分类
categoryRouter.get('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const connection = await mysql.createConnection(dbConfig);
    const [rows] = await connection.execute(
      'SELECT * FROM product_categories WHERE id = ?',
      [id]
    );
    await connection.end();
    
    if (rows.length === 0) {
      return res.error('分类不存在', 404);
    }
    
    res.success(rows[0], '获取分类成功');
  } catch (err) {
    console.error('获取分类失败:', err);
    res.error('获取分类失败');
  }
});

// 删除分类
categoryRouter.delete('/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const connection = await mysql.createConnection(dbConfig);
    
    // 先检查分类是否存在
    const [checkRows] = await connection.execute(
      'SELECT * FROM product_categories WHERE id = ?',
      [id]
    );
    
    if (checkRows.length === 0) {
      await connection.end();
      return res.error('分类不存在', 404);
    }
    
    // 执行删除操作
    await connection.execute(
      'DELETE FROM product_categories WHERE id = ?',
      [id]
    );
    await connection.end();
    
    res.success(null, '删除分类成功');
  } catch (err) {
    console.error('删除分类失败:', err);
    res.error('删除分类失败');
  }
});

// 注册路由
app.use('/api/product/category', categoryRouter);
app.use('/product/category', categoryRouter);

// 测试路由
app.get('/test', (req, res) => {
  res.success(null, '测试成功');
});

// 404 处理
app.use((req, res) => {
  res.error('接口不存在', 404);
});

// 启动服务器
const PORT = process.env.PORT || 3003;
app.listen(PORT, () => {
  console.log(`服务器已启动，端口：${PORT}`);
}); 