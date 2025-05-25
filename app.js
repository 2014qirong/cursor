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

// 确保表存在
async function ensureTablesExist() {
  console.log('开始检查数据库表...');
  try {
    const connection = await mysql.createConnection(dbConfig);
    
    // 检查并创建用户表
    await connection.execute(`
      CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        avatar VARCHAR(255),
        role VARCHAR(50) DEFAULT 'admin',
        status TINYINT DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
      )
    `);
    console.log('用户表检查/创建完成');
    
    // 检查用户表是否为空，如果为空则添加默认管理员用户
    const [userRows] = await connection.execute('SELECT COUNT(*) as count FROM users');
    if (userRows[0].count === 0) {
      console.log('添加默认管理员用户...');
      // 密码: admin123
      await connection.execute(`
        INSERT INTO users (username, password, name, role) VALUES 
        ('admin', '123456', '管理员', 'admin')
      `);
      console.log('默认管理员用户添加完成');
    }
    
    // 检查并创建商品分类表
    await connection.execute(`
      CREATE TABLE IF NOT EXISTS product_categories (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        parent_id INT DEFAULT 0,
        icon VARCHAR(255),
        banner VARCHAR(255),
        sort_order INT DEFAULT 0,
        is_visible TINYINT DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
      )
    `);
    console.log('商品分类表检查/创建完成');
    
    // 检查并创建商品表
    await connection.execute(`
      CREATE TABLE IF NOT EXISTS products (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        category_id INT,
        price DECIMAL(10, 2) DEFAULT 0,
        stock INT DEFAULT 0,
        status TINYINT DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
      )
    `);
    console.log('商品表检查/创建完成');
    
    // 检查商品分类表是否为空，如果为空则添加一些默认数据
    const [rows] = await connection.execute('SELECT COUNT(*) as count FROM product_categories');
    if (rows[0].count === 0) {
      console.log('添加默认商品分类...');
      await connection.execute(`
        INSERT INTO product_categories (name, parent_id) VALUES 
        ('服装', 0),
        ('电子', 0),
        ('食品', 0),
        ('男装', 1),
        ('女装', 1),
        ('手机', 2),
        ('电脑', 2)
      `);
      console.log('默认商品分类添加完成');
    }
    
    await connection.end();
    console.log('数据库表检查完成');
  } catch (err) {
    console.error('数据库表检查/创建失败:', err);
    throw err;
  }
}

// 获取分类列表
categoryRouter.get('/list', async (req, res) => {
  try {
    console.log('[DEBUG] 开始获取商品分类列表');
    const connection = await mysql.createConnection(dbConfig);
    const [rows] = await connection.execute('SELECT * FROM product_categories');
    console.log('[DEBUG] 获取到商品分类数据:', rows);
    await connection.end();
    res.success(rows, '获取分类成功');
  } catch (err) {
    console.error('[ERROR] 数据库查询失败:', err);
    res.error('数据库查询失败: ' + err.message);
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

// 商品路由
const productRouter = express.Router();

// 获取商品列表
productRouter.get('/list', async (req, res) => {
  try {
    const connection = await mysql.createConnection(dbConfig);
    const [rows] = await connection.execute('SELECT * FROM products');
    await connection.end();
    res.success(rows, '获取商品列表成功');
  } catch (err) {
    console.error('获取商品列表失败:', err);
    res.error('获取商品列表失败');
  }
});

// 注册路由
app.use('/api/product', productRouter);
app.use('/product', productRouter);

// 用户路由
const userRouter = express.Router();

// 用户登录
userRouter.post('/login', async (req, res) => {
  try {
    console.log('[DEBUG] 登录请求:', req.body);
    const { username, password } = req.body;
    
    if (!username || !password) {
      return res.error('用户名和密码不能为空', 400);
    }
    
    const connection = await mysql.createConnection(dbConfig);
    const [rows] = await connection.execute(
      'SELECT * FROM users WHERE username = ?',
      [username]
    );
    await connection.end();
    
    if (rows.length === 0) {
      return res.error('用户不存在', 401);
    }
    
    const user = rows[0];
    if (user.password !== password) {
      return res.error('密码错误', 401);
    }
    
    // 简单的 token 生成
    const token = `token_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    res.success({
      token,
      user: {
        id: user.id,
        username: user.username,
        name: user.name,
        avatar: user.avatar,
        role: user.role
      }
    }, '登录成功');
  } catch (err) {
    console.error('[ERROR] 登录失败:', err);
    res.error('登录失败: ' + err.message);
  }
});

// 获取用户信息
userRouter.get('/info', async (req, res) => {
  try {
    // 这里简化处理，实际应该解析 token 获取用户
    const username = req.query.username || 'admin';
    
    const connection = await mysql.createConnection(dbConfig);
    const [rows] = await connection.execute(
      'SELECT id, username, name, avatar, role FROM users WHERE username = ?',
      [username]
    );
    await connection.end();
    
    if (rows.length === 0) {
      return res.error('用户不存在', 404);
    }
    
    res.success(rows[0], '获取用户信息成功');
  } catch (err) {
    console.error('[ERROR] 获取用户信息失败:', err);
    res.error('获取用户信息失败: ' + err.message);
  }
});

// 注册用户路由
app.use('/api/user', userRouter);
app.use('/user', userRouter);

// 测试路由
app.get('/test', (req, res) => {
  res.success(null, '测试成功');
});

// 根路径处理
app.get('/', (req, res) => {
  res.success({
    name: '商城管理系统 API',
    version: '1.0.0',
    endpoints: [
      { path: '/api/product/category', description: '商品分类相关接口' },
      { path: '/api/product', description: '商品相关接口' },
      { path: '/test', description: '测试接口' }
    ]
  }, 'API 服务运行正常');
});

// 404 处理
app.use((req, res) => {
  res.error('接口不存在', 404);
});

// 启动服务器
const PORT = process.env.PORT || 3000;
app.listen(PORT, async () => {
  try {
    await ensureTablesExist();
    console.log(`服务器已启动，端口：${PORT}`);
  } catch (err) {
    console.error('服务器启动失败:', err);
    process.exit(1);
  }
}); 