const express = require('express');
const app = express();
const PORT = 3010;

// 添加 body-parser 中间件解析 JSON 请求体
app.use(express.json());

app.get('/test', (req, res) => {
  console.log('收到测试请求');
  res.json({ code: 200, message: '测试成功' });
});

app.get('/api/test', (req, res) => {
  console.log('收到 API 测试请求');
  res.json({ code: 200, message: 'API 测试成功' });
});

app.get('/api/product/category/list', (req, res) => {
  console.log('收到分类列表请求');
  res.json({ 
    code: 200, 
    message: '获取分类成功', 
    data: [
      { id: 1, name: '测试分类1', parent_id: 0 },
      { id: 2, name: '测试分类2', parent_id: 0 }
    ] 
  });
});

app.post('/api/product/category', (req, res) => {
  console.log('收到添加分类请求', req.body);
  // 模拟生成id
  const newId = Date.now();
  const newCategory = {
    id: newId,
    ...req.body
  };
  res.json({
    code: 200,
    message: '添加分类成功',
    data: newCategory
  });
});

app.get('/product/category/list', (req, res) => {
  console.log('收到无前缀分类列表请求');
  res.json({ 
    code: 200, 
    message: '获取分类成功', 
    data: [
      { id: 1, name: '测试分类1', parent_id: 0 },
      { id: 2, name: '测试分类2', parent_id: 0 }
    ] 
  });
});

app.post('/product/category', (req, res) => {
  console.log('收到无前缀添加分类请求', req.body);
  const newId = Date.now();
  const newCategory = {
    id: newId,
    ...req.body
  };
  res.json({
    code: 200,
    message: '添加分类成功',
    data: newCategory
  });
});

app.listen(PORT, () => {
  console.log(`测试服务已启动，端口：${PORT}`);
}); 