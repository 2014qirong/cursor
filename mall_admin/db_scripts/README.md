# 商城数据库管理脚本

这个目录包含了商城后端管理系统的数据库相关脚本，包括数据库初始化、测试及配置文件。

## 文件说明

- `create_tables.sql`: 数据库初始化脚本，创建数据库表结构及初始数据
- `config.js`: 数据库连接配置文件
- `test_api.js`: API测试脚本
- `package.json`: 测试脚本的依赖配置

## 初始化数据库

1. 确保MySQL服务已安装并启动
2. 修改`config.js`中的数据库连接信息（用户名、密码等）
3. 运行SQL脚本初始化数据库：

```bash
mysql -u root -p < create_tables.sql
```

## 运行API测试

1. 确保后端API服务已启动（默认地址：http://localhost:8080）
2. 安装依赖：

```bash
npm install
```

3. 运行测试脚本：

```bash
npm test
```

或者直接运行：

```bash
node test_api.js
```

## 测试说明

测试脚本将尝试执行以下操作：

1. 连接到MySQL数据库
2. 调用API创建一条测试数据（默认为商品分类）
3. 验证数据库中是否成功创建
4. 输出测试结果

如需测试其他API，请修改`test_api.js`文件，取消注释相应的测试函数。 