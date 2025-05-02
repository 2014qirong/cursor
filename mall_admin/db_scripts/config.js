/**
 * 数据库配置文件
 */
module.exports = {
  // 开发环境数据库配置
  development: {
    host: 'localhost',
    port: 3306,
    username: 'root',
    password: 'password',
    database: 'mall_dev',
    dialect: 'mysql',
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  },
  
  // 测试环境数据库配置
  test: {
    host: 'test-db.example.com',
    port: 3306,
    username: 'test_user',
    password: 'test_password',
    database: 'mall_test',
    dialect: 'mysql',
    pool: {
      max: 5,
      min: 0,
      acquire: 30000,
      idle: 10000
    }
  },
  
  // 生产环境数据库配置
  production: {
    host: 'prod-db.example.com',
    port: 3306,
    username: 'prod_user',
    password: 'prod_password',
    database: 'mall_prod',
    dialect: 'mysql',
    pool: {
      max: 10,
      min: 2,
      acquire: 30000,
      idle: 10000
    }
  }
}; 