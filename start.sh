#!/bin/bash

# 设置环境变量
export DB_HOST=localhost
export DB_PORT=3306
export DB_USER=dev_user
export DB_PASSWORD=admin123
export DB_DATABASE=mall_dev

# 启动服务器
node app.js 